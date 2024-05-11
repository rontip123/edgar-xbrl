import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

taxonomy_mapping_tmpl = {
    "ticker": {
        "revenue" : {"label" : "Revenue", "taxonomy_key" : ""},
        "net_income" : {"label" : "Net Income", "taxonomy_key" : ""},
        "interest_expense" : {"label" : "Interest Expense", "taxonomy_key" : ""},
        "interest_income": {"label" : "Interest Income", "taxonomy_key" : ""},
        "net_interest_expense": {"label" : "Net Interest Expense", "taxonomy_key" : "calc:{interest_expense+interest_income}"},
        "tax_expense": {"label" : "Tax Expense", "taxonomy_key" : ""},
        "depreciation_amortization_expense": {"label" : "Depreciation & Amortization Expense", "taxonomy_key" : ""},
        "ebitda": {"label" : "EBITDA", "taxonomy_key" : "calc:{net_income+interest_expense+tax_expense+depreciation_amortization_expense}"},
        "ebitda_margin": {"label" : "EBITDA Margin", "taxonomy_key" : "calc:{(ebitda/revenue)*100}"},
        "adjusted_ebitda": {"label" : "Adjusted EBITDA", "taxonomy_key" : ""},
        "adjusted_ebitda_margin": {"label" : "Adjusted EBITDA Margin", "taxonomy_key" : ""}
    }
}

taxonomy_mapping = {   
    "para": {
        "revenue" : {"label" : "Revenue", "taxonomy_key" : "RevenueFromContractWithCustomerExcludingAssessedTax"},
        "net_income" : {"label" : "Net Income", "taxonomy_key" : "NetIncomeLoss"},
        "interest_expense" : {"label" : "Interest Expense", "taxonomy_key" : "InterestExpense"},
        "interest_income": {"label" : "Interest Income", "taxonomy_key" : "InterestIncomeOther"},
        "net_interest_expense": {"label" : "Net Interest Expense", "taxonomy_key" : "calc:{interest_expense+interest_income}"},
        "tax_expense": {"label" : "Tax Expense", "taxonomy_key" : "IncomeTaxExpenseBenefit"},
        "depreciation_amortization_expense": {"label" : "Depreciation & Amortization Expense", "taxonomy_key" : "DepreciationAndAmortization"},
        "ebitda": {"label" : "EBITDA", "taxonomy_key" : "calc:{net_income+interest_expense+tax_expense+depreciation_amortization_expense}"},
        "ebitda_margin": {"label" : "EBITDA Margin", "taxonomy_key" : "calc:{(ebitda/revenue)*100}"},
    }, 
    "dis": {
        "revenue" : {"label" : "Revenue", "taxonomy_key" : "Revenues"},
        "net_income" : {"label" : "Net Income", "taxonomy_key" : "NetIncomeLoss"},
        "interest_expense" : {"label" : "Interest Expense", "taxonomy_key" : ""},
        "interest_income": {"label" : "Interest Income", "taxonomy_key" : ""},
        "net_interest_expense": {"label" : "Net Interest Expense", "taxonomy_key" : "InterestIncomeExpenseNonoperatingNet"},
        "tax_expense": {"label" : "Tax Expense", "taxonomy_key" : "IncomeTaxExpenseBenefit"},
        "depreciation_amortization_expense": {"label" : "Depreciation & Amortization Expense", "taxonomy_key" : "DepreciationDepletionAndAmortization"},
        "ebitda": {"label" : "EBITDA", "taxonomy_key" : "calc:{net_income+interest_expense+tax_expense+depreciation_amortization_expense}"},
        "ebitda_margin": {"label" : "EBITDA Margin", "taxonomy_key" : "calc:{(ebitda/revenue)*100}"},        
    },
    "t": {
        "revenue" : {"label" : "Revenue", "taxonomy_key" : "Revenues"},
        "net_income" : {"label" : "Net Income", "taxonomy_key" : "ProfitLoss"},
        "interest_expense" : {"label" : "Interest Expense", "taxonomy_key" : "InterestExpense"},
        "interest_income": {"label" : "Interest Income", "taxonomy_key" : "InterestIncomeOther"},
        "net_interest_expense": {"label" : "Net Interest Expense", "taxonomy_key" : "calc:{interest_expense+interest_income}"},
        "tax_expense": {"label" : "Tax Expense", "taxonomy_key" : "IncomeTaxExpenseBenefit"},
        "depreciation_amortization_expense": {"label" : "Depreciation & Amortization Expense", "taxonomy_key" : "DepreciationDepletionAndAmortization"},
        "ebitda": {"label" : "EBITDA", "taxonomy_key" : "calc:{net_income+interest_expense+tax_expense+depreciation_amortization_expense}"},
        "ebitda_margin": {"label" : "EBITDA Margin", "taxonomy_key" : "calc:{(ebitda/revenue)*100}"},
        "adjusted_ebitda": {"label" : "Adjusted EBITDA", "taxonomy_key" : ""},
        "adjusted_ebitda_margin": {"label" : "Adjusted EBITDA Margin", "taxonomy_key" : ""}
    },
    "tmus": {
        "revenue" : {"label" : "Revenue", "taxonomy_key" : "RevenueFromContractWithCustomerExcludingAssessedTax"},
        "net_income" : {"label" : "Net Income", "taxonomy_key" : "NetIncomeLoss"},
        "interest_expense" : {"label" : "Interest Expense", "taxonomy_key" : ""},
        "interest_income": {"label" : "Interest Income", "taxonomy_key" : ""},
        "net_interest_expense": {"label" : "Net Interest Expense", "taxonomy_key" : "InterestIncomeExpenseNonoperatingNet"},
        "tax_expense": {"label" : "Tax Expense", "taxonomy_key" : "IncomeTaxExpenseBenefit"},
        "depreciation_amortization_expense": {"label" : "Depreciation & Amortization Expense", "taxonomy_key" : "DepreciationDepletionAndAmortization"},
        "ebitda": {"label" : "EBITDA", "taxonomy_key" : "calc:{net_income+interest_expense+tax_expense+depreciation_amortization_expense}"},
        "ebitda_margin": {"label" : "EBITDA Margin", "taxonomy_key" : "calc:{(ebitda/revenue)*100}"},
        "adjusted_ebitda": {"label" : "Adjusted EBITDA", "taxonomy_key" : ""},
        "adjusted_ebitda_margin": {"label" : "Adjusted EBITDA Margin", "taxonomy_key" : ""}
    }    
}

taxonomy_mapping_old = {
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
    "dis": [
        {"taxonomy_key" : "Revenues", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestIncomeExpenseNonoperatingNet", "label" : "Net Interest Expense"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense "},
        {"taxonomy_key" : "DepreciationDepletionAndAmortization", "label" : "Depreciation & Amortization Expense"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities", "label" : "Net Cash Flow from Operating Activities"},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment", "label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "LongTermDebtNoncurrent", "label" : "Long-term (net of current portion)"},
    ],
    "para": [
        {"taxonomy_key" : "RevenueFromContractWithCustomerExcludingAssessedTax", "label" : "Revenue"},
        {"taxonomy_key" : "NetIncomeLoss", "label" : "Net Income"},
        {"taxonomy_key" : "InterestExpense", "label" : "Interest Expense"},
        {"taxonomy_key" : "InterestIncomeOther", "label" : "Interest Income"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationAndAmortization", "label" : "Depreciation & Amortization Expense"},
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
        {"taxonomy_key" : "InterestIncomeExpenseNonoperatingNet", "label" : "Net Interest Expense"},
        {"taxonomy_key" : "IncomeTaxExpenseBenefit", "label" : "Tax Expense"},
        {"taxonomy_key" : "DepreciationDepletionAndAmortization", "label" : "Depreciation & Amortization Expense"},
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
        {"taxonomy_key" : "DepreciationAndAmortization", "label" : "Depreciation & Amortization Expense"},
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
        {"taxonomy_key" : "DepreciationAndAmortization","label" : "Depreciation & Amortization Expense"},
        {"taxonomy_key" : "NetCashProvidedByUsedInOperatingActivities","label" : "Net Cash Flow from Operating Activities (millions)"},
        {"taxonomy_key" : "PaymentsToAcquirePropertyPlantAndEquipment","label" : "Capital Expenditure On Tangible Assets"},
        {"taxonomy_key" : "LongTermDebt","label" : "Debt"},
        {"taxonomy_key" : "LongTermDebtAndCapitalLeaseObligations","label" : "Long-term (net of current portion)"},
        {"taxonomy_key" : "LongTermDebtCurrent","label" : "Current Portion of long-term"}
    ]
}

ticker = "t"
xbrl_keys = taxonomy_mapping[ticker]
# Load JSON data from file
json_file_path = './json/'

#json_file = 'chtr-20231231.json'
#json_file = 'dis-20230930.json'
#json_file = 'para-20231231.json'
json_file = 't-20231231.json'
#json_file = 'tmus-20231231.json'
#json_file = 'vz-20231231.json'


with open(json_file_path + json_file, 'r') as file:
    data = json.load(file)

'''
  "f2615": {
            "value": "10-K",
            "dimensions": {
                "concept": "DocumentType",
                "entity": "0001744489",
                "period": "2022-10-02/2023-09-30"
            }
        },
'''
# get the document type
doc_type = None
for key, value in data["facts"].items():
    if value.get("dimensions", {}).get("concept") == "DocumentType":
        doc_type = value.get("value")
        break

print('doc_type', doc_type)

'''        "f2617": {
            "value": "2023-09-30",
            "dimensions": {
                "concept": "DocumentPeriodEndDate",
                "entity": "0001744489",
                "period": "2022-10-02/2023-09-30"
            }
        },
'''
# get the document period
doc_period = None
for key, value in data["facts"].items():
    if value.get("dimensions", {}).get("concept") == "DocumentPeriodEndDate":
        doc_period = value.get("dimensions", {}).get("period")
        break
period_parts = doc_period.split("/")
period_start = period_parts[0]
period_end = period_parts[1]
#print(period_start, period_end)

# get the fiscal year start and end from the document period
fy_start_date = datetime.strptime(period_start, "%Y-%m-%d")
fy_start = fy_start_date.strftime("%m-%d")

fy_end_date = datetime.strptime(period_end, "%Y-%m-%d")
fy_end = fy_end_date.strftime("%m-%d")

print("fiscal year", fy_start_date, fy_end_date)

#xbrl_keys = para_keys
# Extracting data based on conditions
# Create DataFrame for each xbrl_key
dataframes = []
df_list = []
for next_key in xbrl_keys:    
    filtered_data = []
    for fact, item in data["facts"].items():
        #if item["dimensions"]["concept"] == xbrl_key["taxonomy_key"]:
        xbrl_key = xbrl_keys[next_key]
        if item["dimensions"]["concept"] == xbrl_key["taxonomy_key"]:
            dimensions = item["dimensions"]
            if len(dimensions.items()) == 4:
            #if (True):
                for key, value in dimensions.items():
                    dimension_period = item["dimensions"]["period"]
                    new_item = None

                    if "/" in dimension_period:
                        dimension_period_parts = dimension_period.split("/")
                    
                        # Assuming dimension_period_start and dimension_period_end are in the format "%Y-%m-%d"
                        start_date = datetime.strptime(dimension_period_parts[0], "%Y-%m-%d")
                        end_date = datetime.strptime(dimension_period_parts[1], "%Y-%m-%d")
                        months_diff = relativedelta(end_date, start_date).months

                        if (months_diff == 11):
                            new_item = {"fact" : next_key, "label": xbrl_key["label"], "value": int(item["value"]), "concept": xbrl_key["taxonomy_key"], "year" : end_date.year, "reported_period": dimension_period}
                        else:
                            continue
                    else:
                        dimension_year = datetime.strptime(dimension_period, "%Y-%m-%d").year
                        new_item = {"fact" : next_key, "label": xbrl_key["label"], "value": int(item["value"]), "concept": xbrl_key["taxonomy_key"], "year" : dimension_year, "reported_period": dimension_period}
                    
                    filtered_data.append(new_item)
                    '''
                    if key not in ['unit', 'entity', 'period']:
                        new_item[key] = value
                        filtered_data.append(new_item)
                    '''
            df = pd.DataFrame(filtered_data)
            df_list.append(df)
                        
# transform to json object
final_df = pd.concat(df_list, ignore_index=True).drop_duplicates()
json_data = final_df.groupby('year').apply(lambda x: x.drop('year', axis=1).to_dict(orient='records')).to_dict()
#print(json_data)
for year in json_data.keys():
    net_interest_expense = None # "calc:{interest_expense+interest_income}"}
    interest_expense = None
    interest_income = None
    net_interest_expense = None
    for year_data in json_data[year]:
        if year_data['fact'] == 'interest_expense':
            interest_expense = year_data['value']
        if year_data['fact'] == 'interest_income':
            interest_income= year_data['value']
        if year_data['fact'] == 'net_interest_expense':
            net_interest_expense = year_data['value']
    
    if net_interest_expense is None:
        net_interest_expense = interest_expense + interest_income
        new_item = {"fact" : 'net_interest_expense', "label": "Net Interest Expense", "value": int(net_interest_expense), "concept": "calc:{interest_expense+interest_income}", "year" : year, "reported_period": ""}
        new_df = pd.DataFrame([new_item])
        final_df = pd.concat([final_df, new_df], ignore_index=True)
        json_data[year].append(new_item)
    
    #print(final_df)
    #print(json_data[year])

    '''
    if not('net_interest_expense' in json_data[year]):
        net_interest_expense = 0

    '''
    '''
    #net_interest_expense = year_data['net_interest_expense']
    #print(net_interest_expense)
    if year_data['fact'] == 'net_interest_expense':
        net_interest_expense = year_data['value']
        print(net_interest_expense)
    '''
    
'''
# Check and calculate Net Interest Expense for each period ending in 12-31
for period in json_data.keys():
    if period.endswith("12-31"):
        if "Net Interest Expense" not in [item["label"] for item in json_data[period]]:
            interest_expense = 0
            interest_income = 0
            for item in json_data[period]:
                if item["label"] == "Interest Expense":
                    interest_expense = item["value"]
                    interest_expense_concept = item["concept"]
                elif item["label"] == "Interest Income":
                    interest_income = item["value"]
                    interest_income_concept = item["concept"]
            net_interest_expense = interest_expense + interest_income
            net_interest_expense_concept = "calc: Interest Expense + Interest Income"
            json_data[period].append({"label": "Net Interest Expense", "value": net_interest_expense, "concept": net_interest_expense_concept})
'''

'''
# Check and calculate EBITDA for each period ending in 12-31
for period in json_data.keys():
    if period.endswith("12-31"):
        if "EBITDA" not in [item["label"] for item in json_data[period]]:
            net_income = 0
            interest_expense = 0
            tax_expense = 0
            depreciation_amortization_expense = 0
            for item in json_data[period]:
                if item["label"] == "Net Interest Expense":
                    net_interest_expense = item["value"]
                    net_interest_expense_concept = item["concept"]
                elif item["label"] == "Net Income":
                    net_income = item["value"]
                    net_income_concept = item["concept"]
                elif item["label"] == "Tax Expense":
                    tax_expense = item["value"]
                    tax_expense_concept = item["concept"]
                elif item["label"] == "Depreciation & Amortization Expense":
                    depreciation_amortization_expense = item["value"]
                    depreciation_amortization_expense_concept = item["concept"]
                
            ebitda = net_interest_expense + net_income + tax_expense + depreciation_amortization_expense
            
            ebitda_concept = "calc: Net Income + Interest Expense + Tax Expense + Depreciation & Amortization Expense"

            json_data[period].append({"label": "EBITDA", "value": ebitda, "concept": ebitda_concept})
'''            

'''
# Check and calculate EBITDA Margin for each period ending in 12-31
for period in json_data.keys():
    if period.endswith("12-31"):
        if "EBITDA Margin" not in [item["label"] for item in json_data[period]]:
            ebitda = 0
            revenue = 0            
            for item in json_data[period]:
                if item["label"] == "Revenue":
                    revenue = item["value"]
                    revenue_concept = item["concept"]
                elif item["label"] == "EBITDA":
                    ebitda = item["value"]
                    ebitda_concept = item["concept"]
                
            ebitda_margin = (ebitda / revenue) * 100

            #ebitda_margin_concept = "calc: " + ebitda_concept + "/" + revenue_concept
            ebitda_margin_concept = "calc: EBITDA / Revenue * 100"

            json_data[period].append({"label": "EBITDA Margin", "value": ebitda_margin, "concept": ebitda_margin_concept})
'''

# Write to sorted and calculate JSON
processed_json = json_file.replace('.json', '-processed.json')
with open(json_file_path+processed_json, 'w') as formatted_file: 
    json.dump(json_data, formatted_file, indent=4)
    
# Convert JSON to DataFrame
#final_df = pd.DataFrame([item for year in json_data.values() for item in year])
#final_df = df.rename(columns={'label': 'Metric', 'value': 'Value', 'concept': 'Concept'})
#final_df = pd.concat({k: pd.DataFrame(v) for k, v in json_data.items()}, names=['Year']).reset_index(level=1, drop=True).reset_index()
final_df = pd.concat({k: pd.DataFrame(v) for k, v in json_data.items()}).reset_index(level=1, drop=True).reset_index()


# Write to CSV
csv_file = json_file.replace('.json', '.csv')
final_df.to_csv(json_file_path+csv_file, index=False)

