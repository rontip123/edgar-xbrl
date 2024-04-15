import json
import pandas as pd

# Load JSON data from file
json_file_path = './json/'
json_file = 'cmcsa-20231231.json'
with open(json_file_path + json_file, 'r') as file:
    data = json.load(file)

# Replace with your array of xbrl_keys
xbrl_keys = ["LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities",
             "DebtCurrent",
             "LongTermDebtAndCapitalLeaseObligations",
             "DebtInstrumentCarryingAmount"]  

# Extracting data based on conditions
# Create DataFrame for each xbrl_key
dataframes = []
for xbrl_key in xbrl_keys:
    filtered_data = []
    for key, value in data["facts"].items():
        if value["dimensions"]["concept"] == xbrl_key:
            filtered_data.append({
                "fact": key,
                #"zvalue": value["dimensions"]
                "zvalue": value
            })
    df = pd.DataFrame(filtered_data)
    dataframes.append(df)

# Concatenate all dataframes
final_df = pd.concat(dataframes, ignore_index=True)

# Write to CSV
csv_file = json_file.replace('.json', '.csv')
final_df.to_csv(json_file_path+csv_file, index=False)

