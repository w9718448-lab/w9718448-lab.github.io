# 作品集网站 AI 交接说明

## 接手入口
- 仓库：https://github.com/w9718448-lab/w9718448-lab.github.io
- 网站：https://w9718448-lab.github.io/
- 以远程 main 最新版本为准；先读取本文件、source/README.md、AGENTS.md（如有）、config.json、pages/pages.json、.github/workflows/publish.yml、.github/scripts/build_pages.py。
- 保持账号、仓库名、网站网址及既有二维码入口。

## 更新流程
1. 确认用户指定的是准备公开的 PDF，读取每页实际宽高。PDF 页数不等于传统幻灯片数：一个项目可以导出为一张长页。
2. 将原始 PDF 放在 source/portfolio.pdf。按实际项目起始页更新 config.json；同页项目令 start=end。
3. 运行 python3 .github/scripts/build_pages.py，生成 pages/page-NN.jpg、pages/pages.json 和封面缓存版本。转换器会删除旧的多余页。
4. 运行 python3 .github/scripts/smoke_test.py；核对每页完整比例、首尾页、长页顶部/底部和清晰度。
5. 提交并推送 main。PDF 变更触发“更新作品集”工作流，自动转换并请求 Pages 发布。Pages 应使用 main / (root) 分支发布。
6. 必须等待工作流和 Pages 发布成功，再检查线上 manifest 版本、总页数、目录、首尾页及全部图片请求，最后记录提交和结果。

这是 PDF 转图片网站，页面正文不是可编辑网页文字。图片保留原比例，允许浏览器缩放。不要因 PDF 标题元数据与内容不符，或页数减少，就判断缺少作品。

## 长页展示维护
长页高度远大于 16:9，作品 figure 不使用固定 56.25vw 的 content-visibility 占位，避免目录跳转时估算高度错误。图片仍采用懒加载。封面缓存替换仅匹配静态属性中的版本字符串，不可修改 JavaScript 的动态版本模板。

## 本次更新：2026-10-26
用户明确指定 /Users/mac/Desktop/秋招/作品集.pdf 替换整个作品集。原件 43,895,345 字节，共 9 页；第 3–8 页各为一个完整项目长页。

目录：理石 3、嘉禾 4、宠味食刻 5、龙略略 6、寻宝奇遇记 7、AI Agent 探索 8。第 1 页封面、第 2 页个人介绍、第 9 页结束。

本地转换：9 页，图片合计约 10.6 MB，manifest 版本 c2455a1d8c。已检查九页缩略总览，现有转换回归检查通过（包括缩页清理和无效 PDF 不破坏旧页）。

发布状态：已成功上线。
- 内容提交：fa695b096f23f334f0ba9432d1c874e5150bb5cf。
- 自动转换提交：501ae23（远程 main 的自动更新作品集页面提交）。
- 自动流程：https://github.com/w9718448-lab/w9718448-lab.github.io/actions/runs/40274334407 ，结果 success。
- 线上 manifest 版本：2eff01adf7，共 9 页，六个项目目录起始页为 3–8。
- 已核验线上九张 JPEG 返回成功且可解码、尺寸与清单一致，首尾页正常；封面静态版本与 manifest 一致，动态版本表达式保持正确。网站和二维码入口保持不变。
- Linux 自动转换与 macOS 本地转换的 JPEG 字节略有差异，线上以上述最终版本为准。
- 未完成事项：无发布阻塞；本次未进行微信与 Safari 真机手势测试。


## 更新：2026-10-28
用户指定 `/Users/mac/Desktop/秋招/邵文佳 作品集.pdf` 更新整个作品集，优先保留画质。
- 原 PDF 49,556,136 字节，原样保存于 source/portfolio.pdf，未压缩；SHA256：9d0a62d0ef0372ef712132659bc91e9c1f1a85e8833d32b88e1a7f5afd8fbe58。
- 仍为 9 页，六个项目起始页仍为 3–8；按实际长页比例展示。
- 网页转换宽度由 1600 提高到 1920，JPEG 质量由 82 提高到 95；原 PDF 与网页预览分别保留。
- smoke_test.py 宽度断言跟随 config.json，避免配置提高后被旧的固定 1600 断言阻断。
- 发布结果以 GitHub Actions 和线上 pages/pages.json 核验为准。

用户随后指定最终替换文件：`/Users/mac/Desktop/秋招/邵文佳-设计-作品集-17396129952.pdf`，此前同日文件作废。
原件 53,347,972 字节，SHA256 e4b2fda871758563fdffff0653d76e2f0e088074186e7e7c12242e16884d0ba7，原样保留。9 页，目录不变；本地预览 fb242d031a，约 28.3 MB。转换回归检查通过。


## 宠味食刻修正：2026-10-28
用户重新指定同名桌面原始 PDF，修正宠味食刻项目。原件 53,341,069 字节，SHA256 5249de7ffae27f9e165b7867542d7aa5ab1ef02ef3f737a01711f9ed21ea7d70，原样保存、未压缩。仍为 9 页，宠味食刻为第 5 页；转换配置保持 1920 / JPEG 95。回归检查通过。发布结果待最终线上核验。
