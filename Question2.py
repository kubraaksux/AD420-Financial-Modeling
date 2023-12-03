import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Parameters for the sensitivity analysis
initial_sales_options = np.arange(2500, 7501, 500)
growth_rate_options = np.arange(0.09, 0.22, 0.02)
price_per_download = 2.99  # Price per app download

# Create a DataFrame to store Month 18 revenue results
month_18_revenues = pd.DataFrame(
    index=initial_sales_options, columns=growth_rate_options)

# Perform calculations for each combination of initial sales and growth rate
for initial_sales in initial_sales_options:
    for growth_rate in growth_rate_options:
        sales = initial_sales
        # Apply the growth rate for months 6 through 12
        for month in range(6, 13):
            sales *= (1 + growth_rate)
        # Calculate revenue for month 18 using the final sales figure
        revenue = sales * price_per_download
        # Assign the revenue to the corresponding cell in the DataFrame
        month_18_revenues.at[initial_sales, growth_rate] = revenue

# Define a function to style the DataFrame like an Excel table


def style_table(df):
    return (df.style.set_table_styles([
        {'selector': 'th',
         'props': [('font-size', '12pt'), ('text-align', 'center'), ('background-color', '#4f81bd'), ('color', 'white')]},
        {'selector': 'td',
         'props': [('text-align', 'center'), ('font-size', '10pt')]}
    ])
        .background_gradient(cmap='BuGn', subset=pd.IndexSlice[:, growth_rate_options])
        .format("${0:,.2f}"))


# Apply the styling function to the DataFrame
styled_df = style_table(month_18_revenues)

# Save the styled DataFrame to an HTML file
html = styled_df.to_html()  # Correct method to save the styled DataFrame as HTML
with open('sensitivity_analysis.html', 'w') as f:
    f.write(html)


# Generate and save a heatmap for the sensitivity analysis
plt.figure(figsize=(12, 8))
sns.heatmap(month_18_revenues.astype(float),
            annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Month 18 Revenue Sensitivity Analysis")
plt.xlabel("Growth Rate Options")
plt.ylabel("Initial Sales Options")
plt.tight_layout()  # Adjust the layout to fit all elements
# Save the heatmap as a PNG image
plt.savefig('sensitivity_analysis_heatmap.png')

# Export the sensitivity analysis results to Excel
excel_filename = 'sensitivity_analysis.xlsx'
month_18_revenues.to_excel(excel_filename, engine='openpyxl')

print(f'Sensitivity analysis results saved to {excel_filename}.')
