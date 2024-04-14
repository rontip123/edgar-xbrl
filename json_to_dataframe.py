import json
import pandas as pd

# Load JSON data from file
json_file_path = './json/'
json_file = 'para-20231231.json'
with open(json_file_path + json_file, 'r') as file:
    data = json.load(file)

# Extracting data based on conditions
filtered_data = []
for key, value in data["facts"].items():
    if value["dimensions"]["concept"] == "ProfitLoss" and \
       set(value["dimensions"].keys()) == {"unit", "concept", "entity", "period"}:
        filtered_data.append({
            "fact": key,
            "concept": value["dimensions"]["concept"],
            "period": value["dimensions"]["period"],
            "value": int(value["value"])  # Convert value to integer
        })

# Creating DataFrame
df = pd.DataFrame(filtered_data)
df = df.drop_duplicates(subset=["concept", "period", "value"])

print(df)
