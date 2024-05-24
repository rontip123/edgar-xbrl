import json
import pandas as pd
import boto3
from datetime import datetime
from dateutil.relativedelta import relativedelta

s3 = boto3.client('s3')

taxonomy_mapping_tmpl = {
    "ticker": {
        "revenue" : {"label" : "Revenue", "taxonomy_key" : ""},
        "net_income" : {"label" : "Net Income", "taxonomy_key" : ""},
        "interest_expense" : {"label" : "Interest Expense", "taxonomy_key" : ""},
        "interest_income": {"label" : "Interest Income", "taxonomy_key" : ""},
        "net_interest_expense": {"label" : "Net Interest Expense", "taxonomy_key" : "calc:{interest_expense-interest_income}"},
        "tax_expense": {"label" : "Tax Expense", "taxonomy_key" : ""},
        "depreciation_amortization_expense": {"label" : "Depreciation & Amortization Expense", "taxonomy_key" : ""},
        "ebitda": {"label" : "EBITDA", "taxonomy_key" : "calc:{net_income+interest_expense+tax_expense+depreciation_amortization_expense}"},
        "ebitda_margin": {"label" : "EBITDA Margin", "taxonomy_key" : "calc:{(ebitda/revenue)*100}"},
        "adjusted_ebitda": {"label" : "Adjusted EBITDA", "taxonomy_key" : ""},
        "adjusted_ebitda_margin": {"label" : "Adjusted EBITDA Margin", "taxonomy_key" : ""},        
        "debt_long_term": {"label" : "Long Term Debt (Non-Current)", "taxonomy_key" : ""},
        "debt_long_term_current_portion" : {"label" : "Long Term Debt (Current)", "taxonomy_key" : ""},
        "debt_commercial_paper" : {"label" : "Commercial Paper", "taxonomy_key" : ""},
        #"debt_current_portion": {"label" : "Current Portion", "taxonomy_key" : ""},
        "debt": {"label" : "Total Debt", "taxonomy_key" : "calc:debt_long_term+debt_long_term_current_portion"},
    }
}

ticker = "cmcsa"

use_local_mapping = False
if (use_local_mapping): 
    #xbrl_keys = taxonomy_mapping[ticker]
    with open("./taxonomies/" + ticker.upper() + ".json", 'r') as file:
        xbrl_keys = json.load(file)
else:
    taxonomies_bucket = 'street-smart-taxonomies'
    taxonomies_key = ticker.upper() + ".json"
    taxonomy_response = s3.get_object(Bucket=taxonomies_bucket, Key=taxonomies_key)
    xbrl_keys = json.loads(taxonomy_response['Body'].read().decode('utf-8'))  

#print(xbrl_keys)

# Load JSON data from file
json_file_path = './json/'

json_files = {
    "aapl": "aapl-20230930.json",
    "amcx": "amcx-20231231.json",
    "chtr": "chtr-20231231.json",
    "cmcsa": "cmcsa-20231231.json",
    "dis": "dis-20230930.json",
    "msft": "msft-20230630.json",
    "nvda": "nvda-20240128.json",
    "para": "para-20231231.json",
    "sats": "tmb-20231231x10k.json",
    "t": "t-20231231.json",
    "tmus": "tmus-20231231.json",
    "vz": "vz-20231231.json",
    "wbd": "wbd-20231231.json"
}

json_file = json_files[ticker]

with open(json_file_path + json_file, 'r') as file:
    data = json.load(file)


def do_it():
    # get the document type
    doc_type = None
    for key, value in data["facts"].items():
        if value.get("dimensions", {}).get("concept") == "DocumentType":
            doc_type = value.get("value")
            break

    print('doc_type', doc_type)

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

    # Extracting data based on conditions
    # Create DataFrame for each xbrl_key
    dataframes = []
    df_list = []
    for next_key in xbrl_keys:    
        filtered_data = []
        for fact, item in data["facts"].items():        
            xbrl_key = xbrl_keys[next_key]
            if item["dimensions"]["concept"] == xbrl_key["taxonomy_key"]:
                dimensions = item["dimensions"]
                dim_len = len(dimensions.items())

                # handle member in dimensions
                # TMUS ex: "debt_long_term_current_portion" : {"label" : "Long Term Debt (Current)", "taxonomy_key" : "LongTermDebtCurrent", "member_axis" : ["SeniorNotesMember", "NonrelatedPartyMember"]},
                member_axis = xbrl_key.get("member_axis")
                member_len = 0
                if member_axis is not None:
                    member_len = len(member_axis)                    
                
                if dim_len == (4 + member_len):
                    for key, value in dimensions.items():
                        dimension_period = item["dimensions"]["period"]
                        new_item = None
                        
                        # check if item["dimension"] has values that match all the elements in member_axis
                        if member_axis is not None and not set(member_axis).issubset(set(item["dimensions"].values())):
                            continue
                        
                        if "/" in dimension_period:
                            dimension_period_parts = dimension_period.split("/")
                        
                            # Assuming dimension_period_start and dimension_period_end are in the format "%Y-%m-%d"
                            start_date = datetime.strptime(dimension_period_parts[0], "%Y-%m-%d")
                            end_date = datetime.strptime(dimension_period_parts[1], "%Y-%m-%d")
                            months_diff = relativedelta(end_date, start_date).months
                            years_diff = relativedelta(end_date, start_date).years

                            if (years_diff == 1 or months_diff == 11):
                                new_item = {"fact" : next_key, "label": xbrl_key["label"], "value": float(item["value"]), "concept": xbrl_key["taxonomy_key"], "year" : end_date.year, "reported_period": dimension_period}
                            else:
                                continue
                        else:
                            dimension_year = datetime.strptime(dimension_period, "%Y-%m-%d").year
                            new_item = {"fact" : next_key, "label": xbrl_key["label"], "value": float(item["value"]), "concept": xbrl_key["taxonomy_key"], "year" : dimension_year, "reported_period": dimension_period}
                        
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

    # compare significant figure
    # for each record in duplicates df, find other records with the same fact and year and find the record with the most precise value
    duplicates_df = final_df[final_df.duplicated(subset=['fact', 'year'], keep=False)]
    for index, row in duplicates_df.iterrows():
        fact = row['fact']
        year = row['year']
        filtered_df = final_df[(final_df['fact'] == fact) & (final_df['year'] == year)]
        #TODO: find the value with the most significant figure
        max_value = filtered_df['value'].max()
        most_precise_value = filtered_df[filtered_df['value'] == max_value]
        #final_df = final_df.drop(most_precise_value.index)
        
        print(filtered_df)
        print(most_precise_value)
        #max_value = filtered_df['value'].max()
        #most_precise_value =  
        #filtered_df = filtered_df[filtered_df['value'] == max_value]
        #final_df = final_df.drop(filtered_df.index)

    #print(duplicates_df)


    # handle net_interest_expense
    for year in final_df['year'].unique():
        year_data_df = final_df[final_df['year'] == year]
            
        interest_expense = 0
        interest_income = 0
        net_interest_expense = None
        is_net_interest_expense_calced = True
        
        for index, year_data in year_data_df.iterrows():
            if year_data['fact'] == 'interest_expense':
                interest_expense = year_data['value']
                is_net_interest_expense_calced = False
            if year_data['fact'] == 'interest_income':
                interest_income= year_data['value']
            if year_data['fact'] == 'net_interest_expense':
                net_interest_expense = year_data['value']
        
        if net_interest_expense is None:
            net_interest_expense = interest_expense - interest_income
            new_item = {"fact" : 'net_interest_expense', "label": "Net Interest Expense", "value": int(net_interest_expense), "concept": "calc:{interest_expense+interest_income}", "year" : year, "reported_period": "calculated"}
            new_df = pd.DataFrame([new_item])
            final_df = pd.concat([final_df, new_df], ignore_index=True)

        # handle depreciaton & amortization expense
        depreciation_amortization_expense = None
        depreciation = 0
        amortization = 0
        
        for index, year_data in year_data_df.iterrows():
            if year_data['fact'] == 'depreciation_amortization_expense':
                depreciation_amortization_expense = year_data['value']
            if year_data['fact'] == 'depreciation':
                depreciation = year_data['value']
            if year_data['fact'] == 'amortization':
                amortization = year_data['value']
        
        if depreciation_amortization_expense is None:
            depreciation_amortization_expense = depreciation + amortization
            new_item = {"fact" : 'depreciation_amortization_expense', "label": "Depreciation & Amortization Expense", "value": depreciation_amortization_expense, "concept": "calc:{(depreciation + amoritization)}", "year" : year, "reported_period": "calculated"}
            new_df = pd.DataFrame([new_item])
            final_df = pd.concat([final_df, new_df], ignore_index=True)       

        # handle ebitda
        net_income = None        
        tax_expense = None        
        ebitda = None #calc:{net_income+interest_expense+tax_expense+depreciation_amortization_expense}
        
        for index, year_data in year_data_df.iterrows():
            if year_data['fact'] == 'net_income':
                net_income = year_data['value']
            if year_data['fact'] == 'net_interest_expense':
                net_interest_expense= year_data['value']
            if year_data['fact'] == 'tax_expense':
                tax_expense = year_data['value']
            if year_data['fact'] == 'depreciation_amortization_expense':
                depreciation_amortization_expense = year_data['value']
            if year_data['fact'] == 'ebitda':
                ebitda = year_data['value']
        
        # if net_interest_expese in negative then multiply by -1 (make positive)
        if net_interest_expense is not None and net_interest_expense < 0:
            net_interest_expense = net_interest_expense * -1

            if (abs(interest_expense) < abs(interest_income)):
                net_interest_expense = net_interest_expense * -1            

        if ebitda is None and net_income is not None and net_interest_expense is not None and tax_expense is not None and depreciation_amortization_expense is not None:
            ebitda = net_income + net_interest_expense + tax_expense + depreciation_amortization_expense
            new_item = {"fact" : 'ebitda', "label": "EBITDA", "value": int(ebitda), "concept": "calc:{net_income+interest_expense+tax_expense+depreciation_amortization_expense}", "year" : year, "reported_period": "calculated"}
            new_df = pd.DataFrame([new_item])
            final_df = pd.concat([final_df, new_df], ignore_index=True)

        # handle ebitda_margin
        ebitda = None
        revenue = None
        ebitda_margin = None #calc:{(ebitda/revenue)*100}

        year_data_df = final_df[final_df['year'] == year]
        for index, year_data in year_data_df.iterrows():
            if year_data['fact'] == 'ebitda':
                ebitda = year_data['value']
            if year_data['fact'] == 'revenue':
                revenue= year_data['value']
        
        if ebitda_margin is None and ebitda is not None and revenue is not None:
            ebitda_margin = (ebitda / revenue) * 100
            new_item = {"fact" : 'ebitda_margin', "label": "EBITDA Margin", "value": ebitda_margin, "concept": "calc:{(ebitda/revenue)*100}", "year" : year, "reported_period": "calculated"}
            new_df = pd.DataFrame([new_item])
            final_df = pd.concat([final_df, new_df], ignore_index=True)

        # handle cash_flow_capex and free_cash_flow
        cash_flow_capex = None #calc:{capex_tangible_assets-refunds_capex+capex_intangible_assets}"
        free_cash_flow = None #calc:{net_cash_flow_from_operating_activities-cash_flow_capex}"
        capex_tangible_assets = 0
        refunds_capex = 0
        capex_intangible_assets = 0
        net_cash_flow_from_operating_activities = 0
        
        year_data_df = final_df[final_df['year'] == year]
        for index, year_data in year_data_df.iterrows():
            if year_data['fact'] == 'capex_tangible_assets':
                capex_tangible_assets = year_data['value']
            if year_data['fact'] == 'refunds_capex':
                refunds_capex= year_data['value']
            if year_data['fact'] == 'capex_intangible_assets':
                capex_intangible_assets= year_data['value']
            if year_data['fact'] == 'net_cash_flow_from_operating_activities':
                net_cash_flow_from_operating_activities = year_data['value']
            if year_data['fact'] == 'cash_flow_capex':
                cash_flow_capex = year_data['value']
            if year_data['fact'] == 'free_cash_flow':
                free_cash_flow = year_data['value']
        
        if cash_flow_capex is None and capex_tangible_assets is not None and refunds_capex is not None and capex_intangible_assets is not None:
            cash_flow_capex = capex_tangible_assets-refunds_capex+capex_intangible_assets
            new_item = {"fact" : 'cash_flow_capex', "label": "Cash Flow from Capital Expenditures", "value": cash_flow_capex, "concept": "calc:{capex_tangible_assets-refunds_capex+capex_intangible_assets}", "year" : year, "reported_period": "calculated"}
            new_df = pd.DataFrame([new_item])
            final_df = pd.concat([final_df, new_df], ignore_index=True)
        
        #calc:{net_cash_flow_from_operating_activities-cash_flow_capex}"
        if free_cash_flow is None and cash_flow_capex is not None and net_cash_flow_from_operating_activities is not None:
            free_cash_flow = net_cash_flow_from_operating_activities-cash_flow_capex
            new_item = {"fact" : 'free_cash_flow', "label": "Free Cash Flow", "value": free_cash_flow, "concept": "calc:{net_cash_flow_from_operating_activities-cash_flow_capex}", "year" : year, "reported_period": "calculated"}
            new_df = pd.DataFrame([new_item])
            final_df = pd.concat([final_df, new_df], ignore_index=True)

        # handle debt and debt_current_portion
        debt = None #calc:debt_long_term+debt_long_term_current_portion
        debt_current_portion = None #calc:debt_long_term_current_portion+debt_commercial_paper        
        debt_current = None
        debt_long_term = 0
        debt_long_term_current_portion = 0
        debt_commercial_paper = 0
            
        year_data_df = final_df[final_df['year'] == year]
        for index, year_data in year_data_df.iterrows():
            if year_data['fact'] == 'debt':
                debt = year_data['value']
            if year_data['fact'] == 'debt_current_portion':
                debt_current_portion= year_data['value']
            if year_data['fact'] == 'debt_long_term':
                debt_long_term= year_data['value']
            if year_data['fact'] == 'debt_long_term_current_portion':
                debt_long_term_current_portion = year_data['value']
            if year_data['fact'] == 'debt_commercial_paper':
                debt_commercial_paper = year_data['value']
            
        
        if debt_current_portion is None and debt_long_term_current_portion is not None and debt_commercial_paper is not None:
            debt_current_portion = debt_long_term_current_portion+debt_commercial_paper
            
            if debt_current_portion != 0 and debt_current_portion != 0.0:
                new_item = {"fact" : 'debt_current_portion', "label": "Current Portion", "value": debt_current_portion, "concept": "calc:{debt_long_term_current_portion+debt_commercial_paper}", "year" : year, "reported_period": "calculated"}
                new_df = pd.DataFrame([new_item])
                final_df = pd.concat([final_df, new_df], ignore_index=True)

        #debt_current = debt_long_term_current_portion + debt_commercial_paper
        if debt_current is None and debt_long_term_current_portion is not None and debt_commercial_paper is not None:
            debt_current = debt_long_term_current_portion + debt_commercial_paper
            if debt_current != 0 and debt_current != 0.0:
                new_item = {"fact" : 'debt_current', "label": "Debt Current", "value": debt_current, "concept": "calc:{debt_long_term_current_portion + debt_commercial_paper}", "year" : year, "reported_period": "calculated"}
                new_df = pd.DataFrame([new_item])
                final_df = pd.concat([final_df, new_df], ignore_index=True)

        #debt_long_term+current_debt
        #calc:debt_long_term+debt_long_term_current_portion
        if debt is None and debt_long_term is not None and debt_current is not None:
            debt = debt_long_term+debt_current
            if debt != 0 and debt != 0.0:
                new_item = {"fact" : 'debt', "label": "Debt", "value": debt, "concept": "calc:{debt_long_term+current_debt}", "year" : year, "reported_period": "calculated"}
                new_df = pd.DataFrame([new_item])
                final_df = pd.concat([final_df, new_df], ignore_index=True)            

    # Write to sorted and calculate JSON
    json_data = final_df.groupby('year').apply(lambda x: x.drop('year', axis=1).to_dict(orient='records')).to_dict()
    processed_json = json_file.replace('.json', '-processed.json')
    with open(json_file_path+processed_json, 'w') as formatted_file: 
        #for year in json_data.keys():
            #sorted_items = sorted(json_data[year], key=lambda item: taxonomy_mapping[ticker][item['fact']]['taxonomy_key'])
            #json_data[year] = sorted_items
        json.dump(json_data, formatted_file, indent=4)

    # Write to CSV
    csv_file = json_file.replace('.json', '.csv')
    final_df.to_csv(json_file_path+csv_file, index=False)


do_it()