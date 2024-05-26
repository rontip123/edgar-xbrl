import csv
import json

ticker = "WDAY"

# Path to the CSV file
csv_file_path = 'mappings/mapping_wday.csv'
# Path to the output JSON file
json_file_path = 'taxonomies/' + ticker.upper() + '.json'

def process_taxonomy_key(key):
    """Extract the part of the taxonomy_key after the colon, if present."""
    if ':' in key:
        return key.split(':', 1)[1]
    return key

data = {}
with open(csv_file_path, mode='r', newline='') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    
    for row in csv_reader:
        fact = row['fact']
        if fact:  # Only process rows with a fact value
            # Prepare the JSON object for the current fact
            fact_data = {
                "label": row['label'] if row['label'] else "",
                "taxonomy_key": process_taxonomy_key(row['taxonomy_key']) if row['taxonomy_key'] else ""
            }
            
            # Process member_axis
            if row['member_axis']:
                member_axis_values = row['member_axis'].split(',')
                processed_member_axis = [process_taxonomy_key(value) for value in member_axis_values]
                fact_data["member_axis"] = processed_member_axis
            else:
                fact_data["member_axis"] = []
            
            data[fact] = fact_data

with open(json_file_path, 'w') as jsonfile:
    json.dump(data, jsonfile, indent=4)


