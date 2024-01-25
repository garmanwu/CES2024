import openpyxl
import json
import time
from datetime import datetime, timedelta
from tavily import TavilyClient

# Function to read questions from an XLSX file
def read_xlsx(file_path):
    questions = []
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip the header row
        questions.append(row[0])
    return questions

# Function to get search context for each question using Tavily API
def get_search_contexts(questions, api_key, max_requests=97):
    tavily_client = TavilyClient(api_key=api_key)
    for index, question in enumerate(questions):
        if index % max_requests == 0 and index > 0:
            resume_time = datetime.now() + timedelta(minutes=30)
            print(f"Pausing for 30 minutes. Resuming at {resume_time.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(800)  # Sleep for 30 minutes

        response = tavily_client.search(query=question, max_results=10, include_raw_content=1)
        print(f"Question: {question}\nResponse: {response}\n")
        
        # Save to a separate JSON file
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"Crawler/result_{timestamp}.json"
        with open(file_name, 'w') as file:
            json.dump({"question": question, "response": response}, file, indent=2)

# Main script execution
def main():
    input_file = 'Query_list.xlsx'  # Replace with your XLSX file path
    api_key = 'API_KEY'  # Replace with your actual Tavily API key

    questions = read_xlsx(input_file)
    get_search_contexts(questions, api_key)

# Run the script
if __name__ == "__main__":
    main()
