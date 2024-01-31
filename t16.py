import os
import json
import string
from docx import Document

def clean_text(text):
    """Clean the text by removing non-printable characters and known garbage characters."""
    printable = set(string.printable)
    return ''.join(filter(lambda x: x in printable, text))

def extract_raw_contents_from_results(results):
    """Extract 'raw_content' from the 'results' list in the JSON file."""
    raw_contents = []
    for result in results:
        if 'raw_content' in result and isinstance(result['raw_content'], str):
            raw_contents.append(clean_text(result['raw_content']))
    return raw_contents

def extract_raw_content(json_file):
    """Extract raw_content from a given JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if 'response' in data and isinstance(data['response'], dict) and 'results' in data['response']:
            return extract_raw_contents_from_results(data['response']['results'])
        else:
            print(f"No 'results' in 'response' or not a dict in {json_file}")
            return []
    except json.JSONDecodeError:
        print(f"Error reading {json_file}")
        return []

def read_json_files(directory):
    """Read all JSON files in the given directory and extract raw_content."""
    all_contents = set()
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            raw_contents = extract_raw_content(file_path)
            all_contents.update(raw_contents)
            print(f"Total unique contents so far: {len(all_contents)}")
    return all_contents

def create_docx(contents, output_file):
    """Create a DOCX file with the given contents."""
    doc = Document()
    for content in contents:
        doc.add_paragraph(content)
        doc.add_page_break()
    doc.save(output_file)
    print(f"DOCX file saved with {len(contents)} unique contents.")

# Directory containing the JSON files
directory = 'Crawler'  # Replace with the path to your 'crawler' directory

# Output DOCX file
output_file = 'document.docx'  # Replace with your desired output file path

# Extracting and saving the content
unique_contents = read_json_files(directory)
create_docx(unique_contents, output_file)
