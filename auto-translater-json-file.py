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

    preText = (f'这是{site_game_name}游戏网站的配置文件' if site_game_name  else '')
    
    # 翻译 JSON 字符串
    completion = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4o-mini",
        messages=[{
            "role": "system", 
            "content": """你是一个语言翻译专家，一个网站seo专家，擅长数据处理和多语言翻译的AI专家，具备高效处理JSON数据和灵活应对多种语言需求的能力。 
                        - 翻译考虑到专业术语和正式风格，适用于正式文档和官方交流。翻译做一些去AI味处理，更贴近人工书写表达。
                        - 翻译的结果输出为JSON内容key保持不变，直接输出json内容不要加\`\`\`json\`\`\`标签。，不要做任何解释 
                        - 保证json格式准确性，确保key与内容成对出现。
                        - 翻译考虑使用当地的习惯用语，而不是简单的文字翻译，了解原始文字的意境找到当地的表达方式进行翻译
                        - 不要做任何解释，直接输出json内容，也不要输出\`\`\`json\`\`\`标签
                        - 一些缩写单词不做翻译。
                        - 需要特别注意的是：文本中带有大括号包裹的占位符（如 {username}）需要保留原样，不可翻译。
                        """
        }, {
            "role": "user", 
            "content": preText + f"翻译目标语言为： {target_lang} \n\n 输入JSON数据：\n\n{text}\n"
        }]
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
