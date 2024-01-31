import os
import json
import time
from openai import OpenAI  # Replace with actual OpenAI import

def read_json_files(directory):
    """ Read all JSON files in the specified directory, sorted by time. """
    files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def summarize_file(file_path, client):
    """ Summarize file content using GPT model (in Chinese). """
    with open(file_path, 'r') as file:
        data = json.load(file)

    question = data.get("question", "Unknown")
    filtered_words = [word for word in question.split()[:3] if word.lower() not in ['ces', '2024','and','the','co.,','ltd.','technology','inc.','ltd','co.,ltd','co.,ltd.','electronics','limited','electronic','inc','technologies','llc','corporation','international','tech','group','gmbh','industrial','company','corp.']]
    print(filtered_words)
    # Combine raw_content that contains any of the filtered question words
    raw_contents = [item['raw_content'] for item in data.get("response", {}).get("results", [])
                    if 'raw_content' in item and any(word.lower() in item['raw_content'].lower() for word in filtered_words)]
    combined_content = ' '.join(raw_contents)
    
    # Truncate combined_content to 10k words
    words = combined_content.split()
    if len(words) > 8000:
        combined_content = ' '.join(words[:8000])

    # GPT model call (replace with actual API call)
    prompt = f"Based on raw content as below, structurally and briefly summarize {question}. Summary content is strictly limited in 150 words. \n\nIf raw content is empty, just reply no infomation. \nIf there is no information about the brand mentioned in front, just reply no infomation. CES is a exhibition event, not a company name or brand. The key words before the CES is the company name.\n\nOutput reference format:\n\nBrand or Company name\n\nProduct 1\n\n -feature 1\n\n -feature 2\n\n -feature 3\n\n and so on\n\n Raw Content: {combined_content}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",  # Replace with your model name
        messages=[{"role": "system", "content": "You are a product expert who summarizes the specifications and features of products based on the raw content, ignoring irrelevant content from other brand. The summary should be limited to 150 words."}, {"role": "user", "content": prompt}],
        temperature=0.5
    )
    summary = response.choices[0].message.content
    print(summary)    
    return question, summary

def save_summary(directory, file_name, question, summary):
    """ Save summary to the specified directory. """
    output_path = os.path.join(directory, file_name)
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump({"Question": question, "Summary": summary}, file, indent=2, ensure_ascii=False)

def main():
    crawler_directory = 'Crawler'
    summary_directory = 'Summary'
    openai_api_key = 'OPEN_API_KEY'  # Replace with your OpenAI API key
    client = OpenAI(api_key=openai_api_key)

    json_files = read_json_files(crawler_directory)
    for file_path in json_files:
        question, summary = summarize_file(file_path, client)        
        file_name = os.path.basename(file_path)
        save_summary(summary_directory, file_name, question, summary)

        time.sleep(5)  # Run every 10 seconds

if __name__ == "__main__":
    main()
