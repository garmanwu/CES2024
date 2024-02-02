import os
import json
import time
from openai import OpenAI  # 假设这是有效的导入方式

# 初始化OpenAI客户端
client = OpenAI(api_key='API_KEY')  # 使用您的API密钥

def translate_with_openai(summary):
    try:
        # 使用客户端实例进行翻译请求
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 或其他适合的模型名称
            messages=[
                {"role": "system", "content": "You are a translation expert who translates the following English content into Chinese.Directly translate the prompt content, no other words."},
                {"role": "user", "content": summary}
            ]
        )
        translated_summary = response.choices[0].message.content
        print(summary)
        print(translated_summary)
        return translated_summary
    except Exception as e:
        print(f"Error during translation: {e}")
        raise

def update_json_file(file_path, summary_cn):
    with open(file_path, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        data['Summary_cn'] = summary_cn
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.truncate()

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        summary = data.get('Summary', '').strip()
        if summary.lower() == 'no information.':
            update_json_file(file_path, '无相关信息')
        else:
            for attempt in range(10):
                try:
                    translated_summary = translate_with_openai(summary)
                    update_json_file(file_path, translated_summary)
                    break
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {e}, retrying in 30 seconds...")
                    time.sleep(30)
            else:
                print(f"Failed to translate after 10 attempts: {file_path}")

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            process_file(file_path)

directory_path = 'Summary'  # 请根据实际情况调整
process_files(directory_path)
