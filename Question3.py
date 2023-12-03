import pandas as pd
import numpy as np

# Constants based on the assumptions
initial_investment = 300000  # Entrepreneur's investment
family_investment = 150000  # Family investment
borrowed_amount = 200000  # Long-term debt
total_investment = initial_investment + family_investment + borrowed_amount
straight_line_depreciation = (
    initial_investment + family_investment + borrowed_amount) / 5
interest_rate = 0.09
tax_rate = 0.35
total_equity = initial_investment + family_investment  # Total equity

# Constants for the sales figures
initial_sales = 250000  # Initial sales figure for Period 1
sales_growth_rates = [2, 2, 1.5, 1.2]  # Growth rates for periods 2 to 5
etc_sales_projection = 2592000  # Projected sales for ETC period

# Generate the sales figures based on the growth rates
sales = [initial_sales]
for growth_rate in sales_growth_rates:
    sales.append(sales[-1] * growth_rate)

# Add a beginning value (0 or your initial value) and the ETC projection
sales_forecast = [0] + sales + [etc_sales_projection]

periods = ['Beginning', 'Period 1', 'Period 2',
           'Period 3', 'Period 4', 'Period 5', 'ETC']
assert len(periods) == len(
    sales_forecast), "Periods and sales forecast lists must be of the same length."

# Create the DataFrame
pro_forma = pd.DataFrame({
    'Period': periods,
    'Sales Forecast': sales_forecast
})

# Income Statement calculations
pro_forma['COGS'] = pro_forma['Sales Forecast'] * 0.25
pro_forma['Selling Expenses'] = pro_forma['Sales Forecast'] * 0.12
pro_forma['G&A Expenses'] = 100000 + (pro_forma['Sales Forecast'] * 0.07)
pro_forma['Depreciation'] = straight_line_depreciation
pro_forma['Total Operating Expenses'] = pro_forma['COGS'] + \
    pro_forma['Selling Expenses'] + \
    pro_forma['G&A Expenses'] + pro_forma['Depreciation']
pro_forma['EBIT'] = pro_forma['Sales Forecast'] - \
    pro_forma['Total Operating Expenses']
pro_forma['Interest Expense'] = borrowed_amount * interest_rate
pro_forma['Pre-Tax Income'] = pro_forma['EBIT'] - pro_forma['Interest Expense']
pro_forma['Tax'] = pro_forma['Pre-Tax Income'].apply(
    lambda x: max(0, x) * tax_rate)
pro_forma['Net Income'] = pro_forma['Pre-Tax Income'] - pro_forma['Tax']

# Balance Sheet calculations
pro_forma['Accounts Receivable'] = pro_forma['Sales Forecast'] * 0.2
pro_forma['Inventory'] = pro_forma['COGS'] * 0.15
pro_forma['Accounts Payable'] = pro_forma['COGS'] * 0.08
pro_forma['Wages Payable'] = pro_forma['COGS'] * 0.05
pro_forma['Cash'] = pro_forma['Sales Forecast'].apply(
    lambda x: min(x * 0.20, 50000))
pro_forma['Total Current Assets'] = pro_forma['Cash'] + \
    pro_forma['Accounts Receivable'] + pro_forma['Inventory']
pro_forma['Fixed Assets'] = total_investment - \
    (pro_forma.index * straight_line_depreciation)
pro_forma['Total Assets'] = pro_forma['Total Current Assets'] + \
    pro_forma['Fixed Assets']

# Calculate additional capital investments needed to maintain net fixed assets at 1.2 times the expected sales for the subsequent year
pro_forma['Additional Capital Investments'] = pro_forma['Sales Forecast'].shift(
    -1) * 1.2 - pro_forma['Fixed Assets']
pro_forma['Additional Capital Investments'] = pro_forma['Additional Capital Investments'].clip(
    lower=0)
pro_forma['Fixed Assets'] += pro_forma['Additional Capital Investments']

# Long-term debt calculations
pro_forma['Long-Term Debt'] = borrowed_amount - \
    (pro_forma.index * straight_line_depreciation) + \
    pro_forma['Additional Capital Investments']
pro_forma['Total Liabilities'] = pro_forma['Long-Term Debt'] + \
    pro_forma['Accounts Payable'] + pro_forma['Wages Payable']
pro_forma['Equity'] = total_equity + pro_forma['Net Income'].cumsum()
pro_forma['Total Liabilities & Equity'] = pro_forma['Total Liabilities'] + \
    pro_forma['Equity']

# Cash Flow Statement calculations
pro_forma['Change in Accounts Receivable'] = pro_forma['Accounts Receivable'].diff().fillna(0)
pro_forma['Change in Inventory'] = pro_forma['Inventory'].diff().fillna(0)
pro_forma['Change in Accounts Payable'] = pro_forma['Accounts Payable'].diff().fillna(0)
pro_forma['Change in Wages Payable'] = pro_forma['Wages Payable'].diff().fillna(0)
pro_forma['Change in Cash'] = pro_forma['Cash'].diff().fillna(0)
pro_forma['Operating Cash Flow'] = pro_forma['Net Income'] + pro_forma['Depreciation'] - pro_forma['Change in Accounts Receivable'] - \
    pro_forma['Change in Inventory'] + pro_forma['Change in Accounts Payable'] + \
    pro_forma['Change in Wages Payable']
pro_forma['Capital Expenditures'] = pro_forma['Additional Capital Investments']
pro_forma['Financing Cash Flow'] = borrowed_amount - \
    pro_forma['Long-Term Debt'].diff().fillna(0) + \
    pro_forma['Equity'].diff().fillna(0)
pro_forma['Beginning Cash'] = 0  # You can set the initial cash balance here
pro_forma['Ending Cash'] = pro_forma['Beginning Cash'] + pro_forma['Operating Cash Flow'] - \
    pro_forma['Capital Expenditures'] + \
    pro_forma['Financing Cash Flow'] + pro_forma['Change in Cash']


# Export to Excel
excel_file_path = '/Users/kubraaksu/Desktop/Solutions/Pro_Forma_Financial_Statements.xlsx'
pro_forma.to_excel(excel_file_path, index=False)

# Print the pro forma DataFrame
print(pro_forma)

# Transpose the DataFrame
pro_forma_transposed = pro_forma.transpose()

# Print the transposed DataFrame
print(pro_forma_transposed)

# Optionally, you can also export the transposed DataFrame to Excel
transposed_excel_file_path = '/Users/kubraaksu/Desktop/Solutions/transposed_file.xlsx'
pro_forma_transposed.to_excel(transposed_excel_file_path, index=True)
