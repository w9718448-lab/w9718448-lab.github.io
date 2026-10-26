#!/usr/bin/env python3
"""把 source/portfolio.pdf 转成 pages/page-NN.jpg，并生成 pages/pages.json。

在仓库根目录运行：python3 .github/scripts/build_pages.py
依赖：poppler-utils（pdftoppm）、Pillow。
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image

MAX_PAGES = 300


def fail(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    summary(f"### 更新失败\n\n{msg}\n")
    sys.exit(1)


def summary(text):
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default="source/portfolio.pdf")
    ap.add_argument("--out", default="pages")
    ap.add_argument("--config", default="config.json")
    ap.add_argument("--index", default="index.html")
    a = ap.parse_args()

    pdf, out, index = Path(a.pdf), Path(a.out), Path(a.index)
    if not pdf.is_file():
        fail(f"没有找到 {pdf}。请把导出的 PDF 命名为 portfolio.pdf 并放进 source 文件夹。")
    with pdf.open("rb") as f:
        header = f.read(5)
    if header != b"%PDF-":
        fail(f"{pdf} 不是有效的 PDF 文件。")

    cfg = json.loads(Path(a.config).read_text(encoding="utf-8")) if Path(a.config).is_file() else {}
    width = int(cfg.get("image_width", 1600))
    quality = int(cfg.get("jpeg_quality", 82))

    if not 320 <= width <= 3200 or not 1 <= quality <= 95:
        fail("image_width 必须为 320–3200，jpeg_quality 必须为 1–95。")
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=30, env={**os.environ, "LC_ALL": "C"})
    count = re.search(r"^Pages:\s+(\d+)", info.stdout, re.MULTILINE)
    if info.returncode or not count:
        fail("无法读取 PDF 页数，请检查文件是否损坏或加密。")
    if not 1 <= int(count.group(1)) <= MAX_PAGES:
        fail(f"PDF 页数必须为 1–{MAX_PAGES}。")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        raw = tmp / "raw"
        raw.mkdir()
        run = subprocess.run(
            ["pdftoppm", "-png", "-scale-to-x", str(width), "-scale-to-y", "-1", str(pdf), str(raw / "p")],
            capture_output=True, text=True, timeout=1500,
        )
        if run.returncode != 0:
            fail("PDF 转图片失败：" + run.stderr.strip()[:500])
        pngs = sorted(raw.glob("p-*.png"), key=lambda p: int(re.search(r"-(\d+)\.png$", p.name).group(1)))
        if not pngs:
            fail("PDF 里没有读取到任何页面。")
        if len(pngs) > MAX_PAGES:
            fail(f"PDF 有 {len(pngs)} 页，超过上限 {MAX_PAGES}，请检查是否导出了错误的文件。")

        new = tmp / "new"
        new.mkdir()
        sizes, digest = [], hashlib.sha1()
        for i, png in enumerate(pngs, 1):
            with Image.open(png) as im:
                im = im.convert("RGB")
                dest = new / f"page-{i:02d}.jpg"
                im.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)
                sizes.append([im.width, im.height])
            digest.update(dest.read_bytes())
            png.unlink()
        version = digest.hexdigest()[:10]

        out.mkdir(exist_ok=True)
        for old in out.glob("page-*.jpg"):
            old.unlink()
        for jpg in new.glob("page-*.jpg"):
            shutil.move(str(jpg), out / jpg.name)

    meta = {"version": version, "count": len(sizes), "pages": sizes}
    (out / "pages.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")

    # 封面图加版本号，避免浏览器继续显示旧封面
    if index.is_file():
        html = index.read_text(encoding="utf-8")
        html2 = re.sub(r"(/pages/page-01\.jpg\?v=)[0-9A-Za-z]+(?=[\"\'])", r"\g<1>" + version, html)
        if html2 != html:
            index.write_text(html2, encoding="utf-8")

    # 检查目录配置
    warnings = []
    for s in cfg.get("sections", []):
        if s.get("start", 0) > len(sizes):
            warnings.append(f"目录「{s.get('title')}」起始页 {s.get('start')} 超过总页数 {len(sizes)}，该项不会显示。请修改 config.json。")
        elif s.get("end", 0) > len(sizes):
            warnings.append(f"目录「{s.get('title')}」结束页 {s.get('end')} 超过总页数 {len(sizes)}，已按总页数显示。")
    if sizes and max(abs(w / h - 16 / 9) for w, h in sizes) > 0.02:
        warnings.append("有页面不是 16:9 比例，网页会按各页实际比例显示。")

    total_mb = sum(p.stat().st_size for p in out.glob("page-*.jpg")) / 1e6
    print(f"OK: {len(sizes)} pages, {total_mb:.1f} MB, version {version}")
    for w in warnings:
        print("WARNING:", w)
    summary(
        f"### 作品集已更新\n\n- 页数：{len(sizes)}\n- 图片总大小：{total_mb:.1f} MB\n- 版本号：{version}\n"
        + "".join(f"- ⚠️ {w}\n" for w in warnings)
    )


if __name__ == "__main__":
    main()
