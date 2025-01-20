# Auto-i18n-Plus：使用 ChatGPT 的自动多语言翻译工具

[English](./README.md) | [中文](./README-ZH.md)

Auto-i18n-Plus 是一个使用 ChatGPT 自动将 Markdown 文件和 JSON 文件批量翻译为多语言的工具。它实现了博客文章和网站内容的国际化（i18n）。你仅需将需要翻译的 将 Markdown 文件 或 JSON 文件推送至 GitHub 仓库，即可借助 GitHub Actions 实现自动转译为多种语言。

## Markdown 文件翻译

Auto-i18n-Plus 支持 Markdown 文件翻译：

- **支持更多语种翻译**：Auto-i18n-Plus 支持几乎所有语种的翻译，目前预设语种已达到 30 种，如果想要增加更多翻译语种，只要修改配置文件`env.py`增加即可。
- **批量多语言翻译**：Auto-i18n-Plus 提供了批量翻译的功能，使你能够将一整个路径下的所有 Markdown 和 JSON 文件一次性翻译多语言，极大地提高了多语言化项目的效率。
- **兼容 Front Matter**：Auto-i18n-Plus 兼容 Markdown Front Matter 语法，你可以自定义不同字段的翻译或替换规则。
- **固定内容替换**：Auto-i18n-Plus 还支持固定内容替换。如果你希望文档中一些重复字段的译文保持不变，这个功能可以帮助你实现文档的一致性。
- **自动化工作流**：你可以使用 GitHub Actions 实现自动化的翻译流程，无需手动干预，翻译工作会自动进行并更新文档，使你能够更专注于内容。

### 快速上手

1. 将仓库克隆到本地，把 `env_template.py` 重命名为 `env.py`，并提供你的 ChatGPT API。

> 如果你没有自己的 API，可以到 [GPT_API_free](https://github.com/chatanywhere/GPT_API_free) 申请到一个免费的；
> 也可以借助 [go-chatgpt-api](https://github.com/linweiyuan/go-chatgpt-api) 把网页版 ChatGPT 转 API 使用。

2. 安装必需的模块：`pip install -r requirements.txt` 。

3. 执行命令 `python auto-translater-md.py` 运行程序，它将会自动处理测试目录 `testdir/to-translate` 下的所有 Markdown 文件，执行翻译。

## JSON 文件翻译

Auto-i18n 也可以批量翻译 JSON 文件。对于 JSON 文件翻译，程序具有以下特点：

- **自动化翻译 JSON 内容**：程序会自动读取 JSON 文件中的文本，并将其翻译为目标语言。通过递归遍历 JSON 数据，所有字符串字段都会被翻译。
- **保留动态字段**：在 JSON 文件中，如果文本内容包含像 `{title}` 这样的占位符，程序会确保这些占位符不会被翻译，保留原始格式。翻译时，程序会尊重语言的语序差异，确保占位符的位置正确。
- **处理 JSON 数组和嵌套结构**：无论 JSON 数据是平铺的键值对还是嵌套的数组或字典，Auto-i18n 都能递归处理，确保每个文本字段都被翻译。
- **翻译特定字段**：如果你希望某些字段不被翻译（例如 API URL、日期等），可以在配置文件中指定需要跳过的字段，保持一致性。

### 快速上手

执行命令 `python auto-translater-json.py` 运行程序，它将会自动处理测试目录 `testdir/to-translate` 下的所有 JSON 文件，执行翻译。

## GitHub Actions 自动化指南

你可以在自己项目仓库下创建 `.github/workflows/ci.yml`，当检测到 GitHub 仓库更新后，可以使用 GitHub Actions 自动进行翻译处理，并自动 commit 回原仓库。

`ci.yml` 的内容可参考模板：[ci_template.yml](./ci_template.yml)

你需要在仓库的 `Settings` - `Secrets and variables` - `Repository secrets` 中添加两个 secrets：`CHATGPT_API_BASE` 和 `CHATGPT_API_KEY`，并在程序 `auto-translater.py` 中将 `import env` 语句注释掉。

## 版权和许可

本项目采用 [MIT 许可证](./LICENSE)。

## 致谢

- 感谢[Auto-i18n](https://github.com/linyuxuanlin/Auto-i18n) 提供的 MarkDown AI 翻译方法。
- 感谢 [chatanywhere/GPT_API_free](https://github.com/chatanywhere/GPT_API_free) 提供的免费 ChatGPT API key。
- 感谢 [linweiyuan/go-chatgpt-api](https://github.com/linweiyuan/go-chatgpt-api) 提供的把网页版 ChatGPT 转 API 的方法。

[![Star History Chart](https://api.star-history.com/svg?repos=AshinTop/Auto-i18n-Plus&type=Date)](https://star-history.com/#AshinTop/Auto-i18n-Plus&Date)
