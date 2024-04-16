import json
import pandas as pd

# Load JSON data from file
json_file_path = './json/'
json_file = 'para-20230930.json'
with open(json_file_path + json_file, 'r') as file:
    data = json.load(file)

# Replace with your array of xbrl_keys
#xbrl_keys = ["DebtInstrumentCarryingAmount"] 

chtr_keys = ["Revenues",
           "ProfitLoss",
           "InterestIncomeExpenseNet",
           "IncomeTaxExpenseBenefit",
           "DepreciationAmortizationAndAccretionNet",
           "NetCashProvidedByUsedInOperatingActivities",
           "PaymentsToAcquirePropertyPlantAndEquipment",           
        ]

para_keys = ["RevenueFromContractWithCustomerExcludingAssessedTax",
             "ProfitLoss",
             "InterestExpense",
             "InterestIncomeOther"
             "IncomeTaxExpenseBenefit",
             "DepreciationAndAmortization",
             "PaymentsToAcquirePropertyPlantAndEquipment"
             ]

t_keys = ["Revenues",
           "ProfitLoss",
           "InterestExpense",
           "InterestIncomeOther",
           "IncomeTaxExpenseBenefit",
           "DepreciationDepletionAndAmortization",
           "EarningsBeforeInterestTaxesDepreciationAndAmortization",
           "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
           "PaymentsToAcquireProductiveAssets"
        ]

tmus_keys = ["RevenueFromContractWithCustomerExcludingAssessedTax",
           "NetIncomeLoss",
           "InterestIncomeExpenseNonoperatingNet",
           "IncomeTaxExpenseBenefit",
           "DepreciationDepletionAndAmortization",
           "NetCashProvidedByUsedInOperatingActivities",
           "PaymentsToAcquirePropertyPlantAndEquipment",
           "PaymentsToAcquireIntangibleAssets"
        ]

vz_keys = ["Revenues",
           "ProfitLoss",
           "InterestExpense",
           "IncomeTaxExpenseBenefit",
           "DepreciationAndAmortization",
           "NetCashProvidedByUsedInOperatingActivities",
           "PaymentsToAcquireOtherProductiveAssets",
           "PaymentsToAcquireIntangibleAssets"
        ]

xbrl_keys = para_keys
# Extracting data based on conditions
# Create DataFrame for each xbrl_key
dataframes = []
df_list = []
for xbrl_key in xbrl_keys:
    filtered_data = []
    for fact, item in data["facts"].items():
        if item["dimensions"]["concept"] == xbrl_key:
            dimensions = item["dimensions"]
            new_item = {"fact": fact, "value": int(item["value"]), "concept": xbrl_key}
            for key, value in dimensions.items():
                if key not in ['unit', 'entity']:
                    new_item[key] = value
            filtered_data.append(new_item)
    df = pd.DataFrame(filtered_data)
    df_list.append(df)

final_df = pd.concat(df_list, ignore_index=True)
#print(final_df)

# Write to CSV
csv_file = json_file.replace('.json', '.csv')
final_df.to_csv(json_file_path+csv_file, index=False)

