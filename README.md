# Auto-i18n-Plus: Auto Multi-language Translation Tool Using ChatGPT

[English](./README.md) | [中文](./README-ZH.md)

Auto-i18n-Plus is a tool that uses ChatGPT to automatically batch translate Markdown and JSON files into multiple languages. It enables internationalization (i18n) for blog posts and website content. All you need to do is push the Markdown or JSON files that need to be translated to your GitHub repository, and GitHub Actions will automatically translate them into multiple languages.

## Markdown File Translation

Auto-i18n-Plus supports Markdown file translation:

- **Supports More Languages**: Auto-i18n-Plus supports translation in almost all languages. Currently, it includes 30 preset languages. To add more languages, simply modify the `env.yaml` configuration file.
- **Batch Multi-language Translation**: Auto-i18n-Plus provides batch translation functionality, allowing you to translate all Markdown and JSON files in a given directory to multiple languages at once, greatly improving efficiency for multilingual projects.
- **Compatible with Front Matter**: Auto-i18n-Plus is compatible with Markdown Front Matter syntax. You can customize the translation or replacement rules for different fields.
- **Fixed Content Replacement**: Auto-i18n-Plus also supports fixed content replacement. If you want certain repeated fields in your documents to remain consistent in translation, this feature will help maintain uniformity.
- **Automated Workflow**: You can use GitHub Actions to automate the translation process. No manual intervention is required, and the translation work will be automatically processed and updated, allowing you to focus more on content.

### Quick Start

1. Clone the repository to your local machine, rename `env_template.yaml` to `env.yaml`, and provide your ChatGPT API.

> If you do not have your own API, you can get a free one at [GPT_API_free](https://github.com/chatanywhere/GPT_API_free);  
> Alternatively, you can use [go-chatgpt-api](https://github.com/linweiyuan/go-chatgpt-api) to convert the web-based ChatGPT into an API.

2. Install the required modules: `pip install -r requirements.txt`.

3. Run the command `python auto-translater-md.py`. The program will automatically process all Markdown files in the test directory `testdir/to-translate` and translate them.

## JSON File Translation

Auto-i18n can also batch translate JSON files. The program has the following features for translating JSON files:

- **Automatic Translation of JSON Content**: The program will automatically read the text in JSON files and translate it into the target language. All string fields will be translated by recursively traversing the JSON data.
- **Preserve Dynamic Fields**: In JSON files, if the text contains placeholders like `{title}`, the program will ensure that these placeholders are not translated and will preserve the original format. It will respect the language syntax and ensure that placeholders remain correctly placed.
- **Handle JSON Arrays and Nested Structures**: Whether the JSON data consists of flat key-value pairs or nested arrays or dictionaries, Auto-i18n can recursively handle them and ensure that every text field is translated.
- **Translate Specific Fields**: If you want certain fields (such as API URLs, dates, etc.) not to be translated, you can specify the fields to skip in the configuration file to maintain consistency.

### Quick Start

Run the command `python auto-translater-json.py`. The program will automatically process all JSON files in the test directory `testdir/to-translate` and translate them.

## Supported Languages

Here are the languages currently supported for translation output:

| Language Code | Language Name        |
| ------------- | -------------------- |
| ar            | Arabic               |
| bg            | Bulgarian            |
| cs            | Czech                |
| da            | Danish               |
| de            | German               |
| es            | Spanish              |
| fi            | Finnish              |
| fr            | French               |
| hi            | Hindi                |
| hu            | Hungarian            |
| id            | Indonesian           |
| it            | Italian              |
| ja            | Japanese             |
| ko            | Korean               |
| ms            | Malay                |
| nl            | Dutch                |
| no            | Norwegian            |
| pl            | Polish               |
| pt            | Portuguese           |
| ro            | Romanian             |
| ru            | Russian              |
| sv            | Swedish              |
| sk            | Slovak               |
| sr            | Serbian              |
| tl            | Tagalog              |
| tr            | Turkish              |
| uz            | Uzbek                |
| vi            | Vietnamese           |
| zh-CN         | Chinese (Simplified) |

> You can modify the `env.yaml` file to add or remove language configurations.

## GitHub Actions Automation Guide

You can create `.github/workflows/ci.yml` in your project repository. When updates are detected in the GitHub repository, GitHub Actions will automatically handle the translation process and commit the changes back to the repository.

The content of `ci.yml` can be referenced from the template: [ci_template.yml](./ci_template.yml).

In the GitHub repository's `Settings` - `Secrets and variables` - `Repository secrets`, you need to add two secrets: `CHATGPT_API_BASE` and `CHATGPT_API_KEY`. Then, comment out the `import env` statement in the program `auto-translater.py`.

## Copyright and License

This project is licensed under the [MIT License](./LICENSE).

## Acknowledgements

- Thanks to [Auto-i18n](https://github.com/linyuxuanlin/Auto-i18n) for providing the Markdown AI translation method.
- Thanks to [chatanywhere/GPT_API_free](https://github.com/chatanywhere/GPT_API_free) for providing free ChatGPT API keys.
- Thanks to [linweiyuan/go-chatgpt-api](https://github.com/linweiyuan/go-chatgpt-api) for providing the method to convert the web-based ChatGPT into an API.

[![Star History Chart](https://api.star-history.com/svg?repos=AshinTop/Auto-i18n-Plus&type=Date)](https://star-history.com/#AshinTop/Auto-i18n-Plus&Date)
