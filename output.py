import pandas as pd
import json
import os

# Read Excel file
def read_excel(file_path):
    return pd.read_excel(file_path)

# Match company names to questions
def match_company_questions(field_df, index_df):
    return pd.merge(field_df, index_df, on="company")

# Get summary from JSON file
def get_summary(question, json_folder_path):
    for file_name in os.listdir(json_folder_path):
        if file_name.endswith('.json'):
            with open(os.path.join(json_folder_path, file_name)) as f:
                data = json.load(f)
                if data['Question'] == question:
                    # Check if 'summary' key exists
                    return data.get('Summary', 'No summary available')
    return 'Summary not found'

# Main function
def main():
    field_df = read_excel('field.xlsx')
    index_df = read_excel('index.xlsx')
    json_folder_path = 'Summary'  # Replace with your JSON folder path

    matched_df = match_company_questions(field_df, index_df)

    # Ensure 'Question' column exists
    if 'Question' not in matched_df.columns:
        raise ValueError("Column 'Question' not found after merging DataFrames")

    # Get summary
    matched_df['Summary'] = matched_df['Question'].apply(lambda x: get_summary(x, json_folder_path))

    # Save to different sheets based on field
    with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
        for field in matched_df['field'].unique():
            # Replace invalid characters and truncate sheet name to 31 characters
            valid_sheet_name = field.translate({ord(c): "_" for c in '[]:*?/\\'})[:31]
            df = matched_df[matched_df['field'] == field]
            df.to_excel(writer, sheet_name=valid_sheet_name, index=False)

if __name__ == "__main__":
    main()
