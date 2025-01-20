# Auto-i18n-Plus: An Automated Multilingual Translation Tool Using ChatGPT

Auto-i18n-Plus is a tool that uses ChatGPT to automatically translate Markdown and JSON files into multiple languages. It enables the internationalization (i18n) of blog articles and website content. Simply push the Markdown or JSON files that need translation to a GitHub repository, and with the help of GitHub Actions, the files will be automatically translated into multiple languages.

## Markdown File Translation

Auto-i18n-Plus supports Markdown file translation:

- **Support for More Languages**: Auto-i18n-Plus supports translation into almost all languages. Currently, 30 languages are pre-configured, and if you want to add more, just modify the `env.py` configuration file.
- **Batch Translation**: Auto-i18n-Plus provides batch translation capabilities, allowing you to translate all Markdown and JSON files in a specified directory into multiple languages at once, greatly improving efficiency for multilingual projects.
- **Front Matter Compatibility**: Auto-i18n-Plus is compatible with Markdown Front Matter syntax, allowing you to customize translation or replacement rules for different fields.
- **Fixed Content Replacement**: Auto-i18n-Plus also supports fixed content replacement. If you want certain repeated fields in the document to have consistent translations, this feature helps maintain document consistency.
- **Automated Workflow**: You can use GitHub Actions to automate the translation process, so no manual intervention is required. Translations will automatically take place and the documents will be updated, allowing you to focus more on content creation.

### Quick Start

1. Clone the repository to your local machine, rename `env_template.py` to `env.py`, and provide your ChatGPT API.

> If you don't have your own API, you can apply for a free one from [GPT_API_free](https://github.com/chatanywhere/GPT_API_free);  
> Alternatively, you can use [go-chatgpt-api](https://github.com/linweiyuan/go-chatgpt-api) to turn the web version of ChatGPT into an API.

2. Install the required dependencies: `pip install -r requirements.txt`.

3. Run the program with the command `python auto-translater-md.py`, and it will automatically process all the Markdown files in the test directory `testdir/to-translate` and perform translation.

## JSON File Translation

Auto-i18n-Plus can also batch translate JSON files. For JSON file translation, the program has the following features:

- **Automatic Translation of JSON Content**: The program automatically reads the text within the JSON file and translates it into the target language. By recursively traversing the JSON data, all string fields will be translated.
- **Preserve Dynamic Fields**: In JSON files, if text content contains placeholders like `{title}`, the program ensures that these placeholders are not translated and maintain their original format. During translation, the program respects the language syntax differences and ensures the correct placement of placeholders.
- **Handles JSON Arrays and Nested Structures**: Whether the JSON data consists of flat key-value pairs or nested arrays or dictionaries, Auto-i18n-Plus can recursively process it to ensure every text field gets translated.
- **Translate Specific Fields**: If you want certain fields to be skipped from translation (e.g., API URLs, dates), you can specify these fields in the configuration file to maintain consistency.

### Quick Start

Run the command `python auto-translater-json.py`, and it will automatically process all the JSON files in the test directory `testdir/to-translate` and perform translation.

## GitHub Actions Automation Guide

You can create a `.github/workflows/ci.yml` file in your project repository. Once an update is detected in the GitHub repository, you can use GitHub Actions to automatically trigger the translation process and commit the changes back to the original repository.

The content of `ci.yml` can be referenced from the template: [ci_template.yml](./ci_template.yml)

In the repository's `Settings` - `Secrets and variables` - `Repository secrets`, you need to add two secrets: `CHATGPT_API_BASE` and `CHATGPT_API_KEY`. Then, comment out the `import env` statement in the `auto-translater.py` script.

## License

This project is licensed under the [MIT License](./LICENSE).

## Acknowledgements

- Thanks to [Auto-i18n](https://github.com/linyuxuanlin/Auto-i18n) for providing the Markdown AI translation method.
- Thanks to [chatanywhere/GPT_API_free](https://github.com/chatanywhere/GPT_API_free) for providing free ChatGPT API keys.
- Thanks to [linweiyuan/go-chatgpt-api](https://github.com/linweiyuan/go-chatgpt-api) for providing the method to turn the web version of ChatGPT into an API.

[![Star History Chart](https://api.star-history.com/svg?repos=AshinTop/Auto-i18n-Plus&type=Date)](https://star-history.com/#AshinTop/Auto-i18n-Plus&Date)
