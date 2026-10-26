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

发布状态：待推送及线上核验，不得据此宣称已经上线。
