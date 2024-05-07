import json
import pandas as pd

# Load JSON data from file
json_file_path = './json/'
json_file = 'para-20231231.json'
with open(json_file_path + json_file, 'r') as file:
    data = json.load(file)

# Replace with your array of xbrl_keys
#xbrl_keys = ["DebtInstrumentCarryingAmount"] 

taxonomy_mapping = {
    "amcx": [
        {"taxonomy_key" : "RevenueFromContractWithCustomerExcludingAssessedTax","label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestExpense", "label" : "Interest Expense"},
        {"taxonomy_key" : "InterestIncomeOther", "label" : "Interest Income"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationAndAmortization", "label" : "Depreciation & Amortization Expense"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities", "label" : "Cash Flow From Operating Activities"},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment", "label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "LongTermDebt", "label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtNoncurrent", "label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "LongTermDebtCurrent", "label" : "Current Portion of long-term"}
    ],
    "chtr": [
        {"taxonomy_key" : "Revenues", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestIncomeExpenseNet", "label" : "Net Interest Expense"},
        {"taxonomy_key" : "InterestTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationAmortizationAndAccretionNet", "label" : "Depreciation & Amortization Expense"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities", "label" : "Net Cash Flow from Operating Activities"},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment", "label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "DebtInstrumentFaceAmount", "label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtMaturitiesRepaymentsOfPrincipalInNextTwelveMonths", "label" : "Current Portion of long-term"}
    ],
    "cmcsa": [
        {"taxonomy_key" : "Revenues", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestExpense", "label" : "Interest Expense"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "Depreciation", "label" : "Depreciation"},
        {"taxonomy_key" : "AmortizationOfIntangibleAssets", "label" : "AmortizationOfIntangibleAssets"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities", "label" : "Net Cash Flow from Operating Activities"},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment", "label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "PaymentsToAcquireIntangibleAssets", "label" : "Capital Expenditure On Intangible Assets"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities", "label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligations", "label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "DebtCurrent", "label" : "Current Portion of long-term"},
        {"taxonomy_key" : "DebtInstrumentCarryingAmount","label" : "Commercial Paper"}
    ],
    "para": [
        {"taxonomy_key" : "RevenueFromContractWithCustomerExcludingAssessedTax", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestExpense", "label" : "Interest Expense"},
        {"taxonomy_key" : "InterestIncomeOther", "label" : "Interest Income"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationAndAmortization", "label" : "Depreciation & Amortization Expense (millions)"},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment", "label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "DebtAndCapitalLeaseObligations", "label" : "Debt"},
        {"taxonomy_key" : "DebtAndCapitalLeaseObligations-FIXME", "label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligationsCurrent", "label" : "Current Portion of long-term"},
    ],
    "t": [
        {"taxonomy_key" : "Revenues", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestExpense", "label" : "Interest Expense"},
        {"taxonomy_key" : "InterestIncomeOther", "label" : "Interest Income"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationDepletionAndAmortization", "label" : "Depreciation & Amortization Expense"},
        {"taxonomy_key" : "EarningsBeforeInterestTaxesDepreciationAndAmortization", "label" : "Adjusted EBITDA reported by the company"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations", "label" : "Net Cash Flow from Operating Activities"},
        {"taxonomy_key" : "PaymentsToAcquireProductiveAssets", "label" : "Cash Flow from Capital Expenditures"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities", "label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligations", "label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligationsCurrent", "label" : "Current Portion of long-term"},
        {"taxonomy_key" : "CommercialPaper", "label" : "Commercial Paper"}
    ],
    "sats": [
        {"taxonomy_key" : "RevenueFromContractWithCustomerExcludingAssessedTax", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLossAvailableToCommonStockholdersBasic", "label" : "Net Income"},
        {"taxonomy_key" : "InterestExpenseNetOfAmountCapitalized", "label" : "Interest Expense"},
        {"taxonomy_key" : "InvestmentIncomeNet", "label" : "Interest Income"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationDepletionAndAmortization", "label" : "Depreciation & Amortization Expense"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities", "label" : "Net Cash Flow from Operating Activities "},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment", "label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "ProceedsFromRefundOfPropertyAndEquipment", "label" : "Refunds on Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "DebtAndCapitalLeaseObligations", "label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtAndFinanceLeaseObligationsNetOfCurrentPortion", "label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligationsCurrent", "label" : "Current Portion of long-term"}
    ],
    "tmus": [
        {"taxonomy_key" : "RevenueFromContractWithCustomerExcludingAssessedTax", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestIncomeExpenseNonoperatingNet", "label" : "TNet Interest Expense"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationDepletionAndAmortization", "label" : "Depreciation & Amortization Expense (millions)"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities", "label" : "Net Cash Flow from Operating Activities (millions)"},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment", "label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "PaymentsToAcquireIntangibleAssets", "label" : "Capital Expenditure On Intangible Assets"},
        {"taxonomy_key" : "LongTermDebt", "label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtNoncurrent", "label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "LongTermDebtCurrent", "label" : "Current Portion of long-term (3rd party)"},
        {"taxonomy_key" : "LongTermDebtCurrent-FIXME", "label" : "Current Portion of long-term (Affiliates)"}
    ],
    "vz": [
        {"taxonomy_key" : "Revenues", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestExpense", "label" : "Interest Expense"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationAndAmortization", "label" : "Depreciation & Amortization Expense (millions)"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities", "label" : "Net Cash Flow from Operating Activities (millions)"},
        {"taxonomy_key" : "PaymentsToAcquireOtherProductiveAssets", "label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "PaymentsToAcquireIntangibleAssets", "label" : "Capital Expenditure On Intangible Assets"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities", "label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligations", "label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligationsCurrent", "label" : "Current Portion of long-term"},
        {"taxonomy_key" : "ShortTermBorrowings", "label" : "Commercial Paper"}
    ],
    "wbd": [
        {"taxonomy_key" : "RevenueFromContractWithCustomerExcludingAssessedTax","label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss","label" : "Net Income"},
        {"taxonomy_key" : "InterestExpense","label" : "Net Interest Expense"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit","label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationAndAmortization","label" : "Depreciation & Amortization Expense (millions)"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities","label" : "Net Cash Flow from Operating Activities (millions)"},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment","label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "LongTermDebt","label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligations","label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "LongTermDebtCurrent","label" : "Current Portion of long-term"}
    ]
}


xbrl_keys = taxonomy_mapping["para"]

#xbrl_keys = para_keys
# Extracting data based on conditions
# Create DataFrame for each xbrl_key
dataframes = []
df_list = []
for xbrl_key in xbrl_keys:    
    filtered_data = []
    for fact, item in data["facts"].items():
        if item["dimensions"]["concept"] == xbrl_key["taxonomy_key"]:
            dimensions = item["dimensions"]
            #new_item = {"fact": fact, "label": xbrl_key["label"], "value": int(item["value"]), 
            new_item = {"label": xbrl_key["label"], "value": int(item["value"]), "concept": xbrl_key["taxonomy_key"], "period": item["dimensions"]["period"]}
            if len(dimensions.items()) == 4:
                #print(fact, len(dimensions.items()))
                for key, value in dimensions.items():
                    #print(key, value)
                    if key not in ['unit', 'entity', 'period']:
                        new_item[key] = value
                        filtered_data.append(new_item)
    df = pd.DataFrame(filtered_data)
    df_list.append(df)

final_df = pd.concat(df_list, ignore_index=True).drop_duplicates()
#final_df = final_df.drop_duplicates(subset=list(final_df.columns)[:-2])
#print(final_df)

# Write to CSV
csv_file = json_file.replace('.json', '.csv')
final_df.to_csv(json_file_path+csv_file, index=False)

