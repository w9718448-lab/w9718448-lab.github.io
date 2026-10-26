"""Run converter using disposable PDFs; never change repository page assets."""
from pathlib import Path
from PIL import Image
import tempfile, subprocess, sys, json, shutil, hashlib, os
env = dict(os.environ)
env.pop("GITHUB_STEP_SUMMARY", None)
root=Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory() as directory:
    tmp=Path(directory)
    shutil.copy(root/'config.json',tmp/'config.json')
    shutil.copy(root/'index.html',tmp/'index.html')
    images=[Image.open(root/'pages'/'page-01.jpg').convert('RGB') for _ in range(2)]
    pdf=tmp/'test.pdf'
    def convert():
        return subprocess.run([sys.executable,str(root/'.github/scripts/build_pages.py'),'--pdf',str(pdf)],cwd=tmp,env=env,check=True)
    images[0].save(pdf,save_all=True,append_images=images[1:])
    convert()
    meta=json.loads((tmp/'pages/pages.json').read_text())
    assert meta['count']==2 and len(meta['pages'])==2
    assert all(w==1600 for w,h in meta['pages'])
    assert f"?v={meta['version']}" in (tmp/'index.html').read_text()
    assert "v=${encodeURIComponent(meta.version)}" in (tmp/'index.html').read_text()
    images[0].save(pdf)
    convert()
    assert json.loads((tmp/'pages/pages.json').read_text())['count']==1
    assert not (tmp/'pages/page-02.jpg').exists()
    before={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (tmp/'pages').iterdir()}
    pdf.write_bytes(b'not a PDF')
    result=subprocess.run([sys.executable,str(root/'.github/scripts/build_pages.py'),'--pdf',str(pdf)],cwd=tmp,env=env)
    assert result.returncode != 0
    assert before=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (tmp/'pages').iterdir()}
print('PASS: conversion, dimensions, cover version, shrink cleanup, invalid PDF preserves pages')
