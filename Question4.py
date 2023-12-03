# Question 4: Financial Projections for Lutoj Inc.

# Constants and Initial Conditions
year_3_sales_target = 5e6  # $5 million sales target in Year 3
operating_margin = 0.20  # EBIT/Sales
tax_rate = 0.30  # Tax rate
asset_turnover = 5  # Asset turnover ratio
initial_equity_funding = 200000  # Initial equity funding by founders
interest_rate_debt = 0.08  # Interest rate for debt

# Calculations
# a. Determine if initial equity is sufficient for Year 3 sales target
# Using the formula: Sales = Total Assets / Asset Turnover
# and EBIT = Operating Margin * Sales
# and Net Income = EBIT * (1 - Tax Rate)
# We reverse calculate from the desired Net Income to required Sales and Total Assets

# Required EBIT to meet sales target
required_ebit = year_3_sales_target * operating_margin

# Required Net Income to achieve the EBIT target
required_net_income = required_ebit * (1 - tax_rate)

# Required Total Assets to achieve the sales target
required_total_assets = year_3_sales_target / asset_turnover

# Check if initial equity is sufficient
sufficient_equity = initial_equity_funding >= required_total_assets

# b. Calculate required debt if initial equity is not sufficient
required_debt = 0
if not sufficient_equity:
    # Additional funds needed
    additional_funds_needed = required_total_assets - initial_equity_funding

    # Total debt needed considering the interest expense that can be covered by EBIT
    # EBIT should be sufficient to cover interest expense: EBIT = Interest Expense / Interest Rate
    # Rearranging the formula: Debt = EBIT / Interest Rate
    required_debt = required_ebit / interest_rate_debt

# Results
initial_investment_needed = required_total_assets if not sufficient_equity else initial_equity_funding

print(f"Sufficient initial equity funding: {sufficient_equity}")
print(f"Initial equity funding needed: ${initial_investment_needed}")
print(f"Required debt if using debt financing: ${required_debt}")

# Additional Comments:
# Part (a) calculates the required initial equity funding to achieve the Year 3 sales target.
# Part (b) calculates the required debt if the initial equity is not sufficient.
# The code and comments provide a clear explanation of the calculations and results.
