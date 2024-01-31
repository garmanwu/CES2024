import os
import json
import requests
from openai import OpenAI

# Load your API keys from environment variables or config files
azure_subscription_key = "API_KEY"
openai_api_key = "API_KEY"

# Initialize OpenAI client
openai_client = OpenAI(api_key=openai_api_key)

# Directory containing JSON files
json_dir = "Summary"

# Function to search using Bing
def bing_search(query):
    headers = {"Ocp-Apim-Subscription-Key": azure_subscription_key}
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params)
    return response.json()

# Function to summarize using GPT-3.5
def summarize_with_gpt(filtered_results, question):
    if not filtered_results:
        return "No relevant brand information found."

    prompt = f"Based on raw content as below, structurally and briefly summarize {question}. Summary content is strictly limited to 150 words.\nIf raw content is empty, just reply no information. \nIf there is no information about the brand mentioned in front, just reply no information. CES is an exhibition event, not a company name or brand. The key words before the CES is the company name.\n\nOutput reference format:\n\nBrand or Company name\n\nProduct 1\n\n -feature 1\n\n -feature 2\n\n -feature 3\n\n and so on\n\n Raw Content:\n\n"
    prompt += " ".join(filtered_results)
    print(prompt)
    response = openai_client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "system", "content": "You are a product expert who summarizes the specifications and features of products based on the raw content, ignoring irrelevant content from other brand. The summary should be limited to 150 words."}, {"role": "user", "content": prompt}],
        max_tokens=180,
        temperature=0.5)
    print(response.choices[0].message.content)
    return response.choices[0].message.content

# Process each JSON file in the directory
for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        file_path = os.path.join(json_dir, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        summary = data.get("Summary")
        if summary:
            summary_lower = summary.lower()  # Convert summary to lowercase for case-insensitive comparison
            keywords = ["rabbit", "samsung", "transparent", "asus", "resolution","nvdia","no information","not mentioned"]
            if any(keyword in summary_lower for keyword in keywords):
                question = data.get("Question", "Unknown")
                filtered_words = [word for word in question.split()[:3] if word.lower() not in ['ces', '2024', 'and', 'the', 'co.,', 'ltd.', 'technology', 'inc.', 'ltd', 'co.,ltd', 'co.,ltd.', 'electronics', 'limited', 'electronic', 'inc', 'technologies', 'llc', 'corporation', 'international', 'tech', 'group', 'gmbh', 'industrial', 'company', 'corp.']]
                print(filtered_words)

                search_results = bing_search(question)
                filtered_results = [snippet["snippet"] for snippet in search_results["webPages"]["value"]
                                    if any(word.lower() in snippet["snippet"].lower() for word in filtered_words)]

                new_summary = summarize_with_gpt(filtered_results, question)

                # Update the Summary field
                data["Summary"] = new_summary

                # Save the updated JSON file
                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)
