''' Analyze the data points in the CSV file'''

import pandas as pd

def analyzeCSV(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Calculate the number of data points for each field
    field_counts = {}
    for column in df.columns:
        non_null_count = df[column].count()
        field_counts[column] = non_null_count

    # Print the results
    print("\nNumber of data points for each field:")
    for field, count in field_counts.items():
        print(f"{field}: {count}")

    # Optionally, save the field counts to a separate CSV
    field_counts_df = pd.DataFrame.from_dict(field_counts, orient='index', columns=['Count'])
    field_counts_df.index.name = 'Field'
    field_counts_df.to_csv('field_counts.csv')
    print("\nField counts saved to field_counts.csv")

# Path to your CSV file
csv_file_path = 'cwl_documents/raw_data/cwl_documents.csv'

# Analyze the CSV file
analyzeCSV(csv_file_path)