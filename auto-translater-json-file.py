import os
import openai
import sys
import json
from concurrent.futures import ThreadPoolExecutor, as_completed  # 并行化处理
import yaml  # pip install PyYAML

# 读取 ENV YAML 文件
with open("env.yaml", "r", encoding="utf-8") as file:
    env_data = yaml.safe_load(file)

# 设置 OpenAI API Key 和 API Base 参数，通过 env.yaml 传入
openai.api_key = env_data["CHATGPT_API_KEY"]
openai.api_base = env_data["CHATGPT_API_BASE"]
# 目标语言列表
languages = env_data["LANGUAGE_LIST"]
# 语言映射字典
lang_dict = env_data["LANGUAGE_DIST"]

# 设置翻译的路径
dir_to_translate = "testdir/from"
dir_out_translate = 'testdir/docs/json'

# 游戏网站名称
site_game_name = env_data['GAME_NAME']

# def remove_newline_and_tab(input_string):
#     # 替换 \n 和 \t 为 ''
#     result = input_string.replace('\n', '').replace('\t', '')
#     return result

# 定义调用 ChatGPT API 翻译的函数
def translate_text(text, lang):
    target_lang = lang_dict.get(lang)

    preText = f"This is the configuration file for the {site_game_name} game website." if site_game_name else ''
    
    # 翻译 JSON 字符串
    completion = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4o-mini",
        messages=[
        {
            "role": "system",
            "content": """🚫 Do NOT include any code block markers such as ```json, ```, or <code>. Output a clean and valid JSON string only, without any explanations, comments, or extra formatting.

                        You are an expert in website SEO, language localization, and multilingual translation, with advanced skills in processing JSON data accurately. Please translate only the **values** in the provided JSON input. Keep all **keys unchanged**, and ensure the output is a structurally valid JSON object.

                        Instructions for translation:

                        - Use natural, expressive, and native-level language in the target language, reflecting the tone of game bloggers or gaming communities.
                        - The value of the "name" key represents the game title. It should NEVER be translated.
                        - If the exact text of the "name" value appears in other fields (such as description), do NOT translate it there either. Keep the game title intact wherever it appears.
                        - Do not translate game names, abbreviations (e.g., RPG, PvP), or placeholder variables enclosed in curly brackets (e.g., {username}).
                        - Do not perform literal word-for-word translation; instead, convey the original meaning using locally common phrases or idioms.
                        - The writing style should reflect **high Perplexity** (rich, diverse vocabulary) and **high Burstiness** (variation in sentence length and structure).
                        - Avoid rigid, templated, or robotic AI-sounding phrasing.
                        - Output should be valid JSON with keys unchanged and only the values translated. No additional text or formatting.
                        """
        },
        {
            "role": "user",
            "content": f"{preText}\nTarget language: {target_lang}\nTranslate the following JSON (only values, keep keys unchanged):\n{text}"
        }
    ]
    )

    # 获取翻译结果
    translated_text = completion.choices[0].message.content
    
    # 假设翻译的内容是有效的 JSON 字符串，返回解析后的 JSON 对象
    # translated_text = remove_newline_and_tab(translated_text)
    try:
        translated_json = json.loads(translated_text)
        return translated_json
    except json.JSONDecodeError:
        print("Error: The translated content is not a valid JSON. Returning raw text.")
        return translated_text

# 定义翻译 JSON 文件的函数
def translate_file(input_file, filename, lang, progress_counter):
    print(f"Translating JSON into {lang}: {filename}")
    sys.stdout.flush()

    # 定义输出文件
    output_dir = dir_out_translate
    output_name = lang + ('.json' if filename == 'en.json' else f'_{lang}_{filename}')

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, output_name)

    # 读取输入 JSON 文件内容
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            input_data = json.load(f)

        # 翻译 JSON 数据
        translated_data = translate_text(input_data, lang)

        # 如果翻译成功并且返回了有效的 JSON 数据
        if translated_data is not None:
            # 写入翻译后的 JSON 文件
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(translated_data, f, ensure_ascii=False, indent=4)

        # 增加任务完成计数
        progress_counter[0] += 1  # 这里进度计数器作为列表的第一个元素传递

    except Exception as e:
        print(f"Error processing {filename} for language {lang}: {e}")
        sys.stdout.flush()


# 按文件名称顺序排序
file_list = os.listdir(dir_to_translate)
sorted_file_list = sorted(file_list)

# 使用线程池进行并行处理
def process_files():
    total_tasks = len(sorted_file_list) * len(languages)  # 计算总任务数
    progress_counter = [0]  # 使用列表存储任务完成的计数
    with ThreadPoolExecutor() as executor:
        try:
            futures = []
            # 遍历目录下的所有 JSON 文件
            for filename in sorted_file_list:
                if filename.endswith(".json"):
                    input_file = os.path.join(dir_to_translate, filename)

                    # 为每种语言提交翻译任务
                    for lang in languages:
                        future = executor.submit(translate_file, input_file, filename, lang, progress_counter)
                        futures.append(future)

            # 等待所有任务完成
            for future in as_completed(futures):
                future.result()  # 让每个线程完成并返回（尽管不需要返回值）

            # 检查任务完成并打印消息
            if progress_counter[0] == total_tasks:
                print("Congratulations! All files processed done.")
                sys.stdout.flush()

        except Exception as e:
            print(f"An error has occurred: {e}")
            sys.stdout.flush()
            raise SystemExit(1)

if __name__ == '__main__':
    process_files()
