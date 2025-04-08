import os
import sys
import re
import yaml
import openai
import multiprocessing
from functools import partial

# === 读取配置 ===
with open("env.yaml", "r", encoding="utf-8") as file:
    env_data = yaml.safe_load(file)

openai.api_key = env_data["CHATGPT_API_KEY"]
openai.api_base = env_data["CHATGPT_API_BASE"]
languages = env_data.get("LANGUAGE_LIST", [])
lang_dict = env_data.get("LANGUAGE_DIST", {})

# === 参数定义 ===
max_length = 1800
dir_to_translate = "testdir/from"
dir_out_translate = 'testdir/docs/md'
exclude_list = ["index.md", "Contact-and-Subscribe.md", "WeChat.md"]
processed_list = "processed_list.txt"
marker_written_in_en = "\n> This post was originally written in English.\n"
marker_force_translate = "\n[translate]\n"

replace_rules = [
    {
        "orginal_text": "](https://wiki-power.com/",
        "replaced_text": {
            "en": "](https://wiki-power.com/en/",
            "es": "](https://wiki-power.com/es/",
            "ar": "](https://wiki-power.com/ar/",
        }
    }
]

# === 翻译核心 ===
def translate_text(text, lang, type, retries=3):
    target_lang = lang_dict.get(lang)
    for attempt in range(retries):
        try:
            if type == "front-matter":
                completion = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional translation engine, please translate..."},
                        {"role": "user", "content": f"Translate into {target_lang}:\n\n{text}"}
                    ]
                )
            else:
                completion = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": """你是一个语言翻译专家，一个网站seo专家..."""},
                        {"role": "user", "content": f"Translate into {target_lang}:\n\n{text}"}
                    ]
                )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"[Retry {attempt+1}] Failed to translate: {e}")
            if attempt == retries - 1:
                raise

# 替换 <a href="/..."> → <a href="lang/...">
def replace_a_href_with_lang(text, lang):
    pattern = r'(<a\s+[^>]*href="/)([^"]*)(".*?>)'
    replacement = r'\1' + lang + r'/\2\3'
    return re.sub(pattern, replacement, text)

# 翻译文件的单个语言版本（进程任务）
def translate_file(input_file, filename, lang, _=None):
    sys.stdout.flush()

    relative_path = os.path.relpath(input_file, dir_to_translate)
    output_dir = os.path.join(dir_out_translate, os.path.dirname(relative_path))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_name = (
        lang + '.md' if filename == 'en.md' 
        else filename.replace('en.md', f'{lang}.md') if filename == 'index.en.md'
        else f'{lang}_{filename}'
    )

    output_file = os.path.join(output_dir, output_name)

    # ✅ 如果已存在翻译后的文件，则跳过
    if os.path.exists(output_file):
        print(f"⏩ Skipped (already exists): {output_file}")
        return relative_path

    with open(input_file, "r", encoding="utf-8") as f:
        input_text = f.read()

    placeholder_dict = {}
    for i, rule in enumerate(replace_rules):
        replacement = rule["replaced_text"].get(lang, rule["replaced_text"].get('en'))
        placeholder = f"[to_be_replace[{i + 1}]]"
        input_text = input_text.replace(rule["orginal_text"], placeholder)
        placeholder_dict[placeholder] = replacement

    input_text = replace_a_href_with_lang(input_text, lang)
    input_text = input_text.replace(marker_force_translate, "")
    if lang != "en":
        input_text = input_text.replace(marker_written_in_en, "")

    paragraphs = input_text.split("\n\n")
    current_paragraph = ""
    output_paragraphs = []

    for paragraph in paragraphs:
        if len(current_paragraph) + len(paragraph) + 2 <= max_length:
            current_paragraph += "\n\n" + paragraph
        else:
            output_paragraphs.append(translate_text(current_paragraph, lang, "main-body"))
            current_paragraph = paragraph
    if current_paragraph:
        output_paragraphs.append(translate_text(current_paragraph, lang, "main-body"))

    output_text = "\n\n".join(output_paragraphs)
    for placeholder, replacement in placeholder_dict.items():
        output_text = output_text.replace(placeholder, replacement)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)

    print(f"✅ Translated: {filename} → {lang} : {relative_path}")
    return relative_path

# 构造任务列表
def collect_translation_tasks(file_list, processed_list_content):
    tasks = []
    for input_file in file_list:
        filename = os.path.basename(input_file)
        relative_path = os.path.relpath(input_file, dir_to_translate)
        force_flag = marker_force_translate in open(input_file, "r", encoding="utf-8").read()

        if relative_path in processed_list_content and not force_flag:
            print(f"🚫 Skipped (already processed): {relative_path}")
            continue
        if filename in exclude_list:
            print(f"🚫 Skipped (in exclude list): {filename}")
            continue

        for lang in languages:
            tasks.append((input_file, filename, lang))
    return tasks

# 多进程 worker
def process_translation_task(task):
    input_file, filename, lang = task
    try:
        return translate_file(input_file, filename, lang)
    except Exception as e:
        print(f"❌ Error: {filename} → {lang} | {e}")
        return None

# 主程序
def main():
    file_list = []
    for root, dirs, files in os.walk(dir_to_translate):
        for filename in files:
            if filename.endswith(".md"):
                file_list.append(os.path.join(root, filename))

    sorted_file_list = sorted(file_list)

    if not os.path.exists(processed_list):
        with open(processed_list, "w", encoding="utf-8") as f:
            print("📄 processed_list.txt created")

    with open(processed_list, "r", encoding="utf-8") as f:
        processed_list_content = f.read().splitlines()

    tasks = collect_translation_tasks(sorted_file_list, processed_list_content)
    num_processes = multiprocessing.cpu_count()

    print(f"🚀 Starting {len(tasks)} translation tasks with {num_processes} workers...")

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(process_translation_task, tasks)

    translated_paths = set(filter(None, results))

    with open(processed_list, "a", encoding="utf-8") as f:
        for path in translated_paths:
            f.write(path + "\n")

    print("🎉 All translations done!")

if __name__ == "__main__":
    main()
