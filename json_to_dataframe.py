import json
import pandas as pd

# Load JSON data from file
json_file_path = './json/'
json_file = 'para-20231231.json'
with open(json_file_path + json_file, 'r') as file:
    data = json.load(file)

# Replace with your array of xbrl_keys
xbrl_keys = ["RevenueFromContractWithCustomerExcludingAssessedTax", 
             "CostsAndExpenses",
             "OperatingIncomeLoss",
             "NetIncomeLoss",             
             ]  

# Extracting data based on conditions
# Create DataFrame for each xbrl_key
dataframes = []
for xbrl_key in xbrl_keys:
    filtered_data = []
    for key, value in data["facts"].items():
        if value["dimensions"]["concept"] == xbrl_key and \
           set(value["dimensions"].keys()) == {"unit", "concept", "entity", "period"}:
            filtered_data.append({
                "fact": key,
                "concept": value["dimensions"]["concept"],
                "period": value["dimensions"]["period"],
                "value": int(value["value"])  # Convert value to integer
            })
    df = pd.DataFrame(filtered_data)
    df = df.drop_duplicates(subset=["concept", "period", "value"])
    dataframes.append(df)

# Print DataFrame for each xbrl_key
for i, df in enumerate(dataframes):
    print(f"DataFrame for xbrl_key: {xbrl_keys[i]}")
    print(df)
