import os
import json

os.environ["CHATGPT_API_KEY"] = "sk-xxxx" 
os.environ["CHATGPT_API_BASE"] = "xxx" # e.g. 官方API地址：https://api.openai.com/v1/

# 将列表转换为 JSON 字符串
languages_list = [
    "ar", "bg", "cs", "da", "de", "es", "fi", "fr", "hi", "hu", "id", "it", "ja", "ko", 
    "ms", "nl", "no", "pl", "pt", "ro", "ru", "sv", "sk", "sr", "tl", "tr", "uz", "vi", "zh-CN"
]
os.environ["LANGUAGE_LIST"] = json.dumps(languages_list)

# 将字典转换为 JSON 字符串
languages_dict = {
    "ar": "Arabic", "bg": "Bulgarian", "cs": "Czech", "da": "Danish", "de": "German", 
    "es": "Spanish", "fi": "Finnish", "fr": "French", "hi": "Hindi", "hu": "Hungarian", 
    "id": "Indonesian", "it": "Italian", "ja": "Japanese", "ko": "Korean", "ms": "Malay", 
    "nl": "Dutch", "no": "Norwegian", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", 
    "ru": "Russian", "sv": "Swedish", "sk": "Slovak", "sr": "Serbian", "tl": "Tagalog", 
    "tr": "Turkish", "uz": "Uzbek", "vi": "Vietnamese", "zh-CN": "Chinese (Simplified)"
}
os.environ["LANGUAGE_DICT"] = json.dumps(languages_dict)

