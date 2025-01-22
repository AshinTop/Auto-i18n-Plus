# -*- coding: utf-8 -*-
import os
import openai
import sys
import json
from concurrent.futures import ThreadPoolExecutor, as_completed  # 并行化处理
from tqdm import tqdm  # 导入 tqdm 用于显示进度条
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

# 设置最大输入字段，超出会拆分输入，防止超出输入字数限制
max_length = 1800

# 设置翻译的路径
dir_to_translate = "testdir/to-translate"
dir_out_translate = 'testdir/docs/json'

# 即使在已处理的列表中，仍需要重新翻译的标记
marker_force_translate = "\n[translate]\n"

# 定义调用 ChatGPT API 翻译的函数
def translate_text(text, lang):
    target_lang = lang_dict.get(lang)
    
    # 翻译 JSON 字符串
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional translator and localization expert. Your task is to translate the JSON content of a website, focusing on accuracy and fluency for the target language. Pay special attention to the meaning of individual words based on context. For example, the word \"home\" should be translated as \"主页\" (Home page) in the context of a website, not simply as \"家\" (house). Similarly, make sure to translate UI-related terms and content to be user-friendly and culturally appropriate.  If the text contains placeholders like \"{title}\" or \"{username}\", you must keep them unchanged and ensure they retain their original format. The placeholders should not be translated, but ensure that the sentence structure and word order in the target language still make sense with the placeholders in place. Be aware of differences in sentence structure between languages (e.g., placing the subject before the verb in English vs. other languages). You must only translate the text content, never interpret it.  If the text is not translatable or doesn't contain any meaningful content, just return the original text as is, without any changes."},
            {"role": "user", "content": f"Translate into {target_lang}:\n\n{text}\n"},
        ],
    )
    # 获取翻译结果
    return completion.choices[0].message.content

# 递归翻译 JSON 数据中的字符串
def translate_json(data, lang, progress_bar):
    if isinstance(data, dict):
        # 如果是字典，递归翻译其中的每个字段
        for key, value in data.items():
            # 在翻译每个键值时，更新进度条
            data[key] = translate_json(value, lang, progress_bar)
            progress_bar.update(1)  # 每翻译一个键就更新进度条
        return data
    elif isinstance(data, list):
        # 如果是列表，递归翻译其中的每个元素
        return [translate_json(item, lang, progress_bar) for item in data]
    elif isinstance(data, str):
        # 如果是字符串，翻译该字符串
        return translate_text(data, lang)
    else:
        # 如果既不是字符串也不是需要翻译的数据类型，直接返回
        return data

# 定义翻译 JSON 文件的函数
def translate_file(input_file, filename, lang, progress_bar):
    print(f"Translating JSON into {lang}: {filename}")
    sys.stdout.flush()

    # 定义输出文件
    output_dir = dir_out_translate
    outout_name = lang + ('.json' if filename == 'en.json' else f'_{lang}_{filename}')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, outout_name)

    # 读取输入 JSON 文件内容
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            input_data = json.load(f)

        # 计算总字段数（用于进度条）
        total_fields = sum(1 for _ in flatten_json(input_data))
        progress_bar.total = total_fields  # 设置进度条的总数量

        # 翻译 JSON 数据
        translated_data = translate_json(input_data, lang, progress_bar)

        # 写入翻译后的 JSON 文件
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"Error processing {filename} for language {lang}: {e}")
        sys.stdout.flush()

# 递归扁平化 JSON 数据，计算字段数量
def flatten_json(data, prefix=''):
    if isinstance(data, dict):
        for key, value in data.items():
            yield from flatten_json(value, prefix + key + '.')
    elif isinstance(data, list):
        for i, item in enumerate(data):
            yield from flatten_json(item, prefix + str(i) + '.')
    else:
        yield prefix[:-1]  # 返回键路径，去除末尾的点

# 按文件名称顺序排序
file_list = os.listdir(dir_to_translate)
sorted_file_list = sorted(file_list)

# 使用线程池进行并行处理
def process_files():
    total_tasks = len(sorted_file_list) * len(languages)  # 计算总任务数
    with ThreadPoolExecutor() as executor:
        with tqdm(total=total_tasks, desc="Translation Progress", unit="key") as progress_bar:  # 使用 tqdm 显示进度条
            futures = []  # 用于存储每个线程的 futures
            try:
                # 遍历目录下的所有 JSON 文件
                for filename in sorted_file_list:
                    if filename.endswith(".json"):
                        input_file = os.path.join(dir_to_translate, filename)

                        # 为每种语言提交翻译任务
                        for lang in languages:
                            future = executor.submit(translate_file, input_file, filename, lang, progress_bar)
                            futures.append(future)

                # 等待所有任务完成并更新进度条
                for future in as_completed(futures):
                    future.result()  # 获取每个线程的结果（虽然我们不需要这个值）
                    progress_bar.update(1)  # 更新进度条

                # 所有任务完成的提示
                print("Congratulations! All files processed done.")
                sys.stdout.flush()

            except Exception as e:
                print(f"An error has occurred: {e}")
                sys.stdout.flush()
                raise SystemExit(1)

if __name__ == '__main__':
    process_files()
