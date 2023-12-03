import pandas as pd
import matplotlib.pyplot as plt

# Initialize variables
months = range(1, 19)
initial_downloads = 5000.0  # Ensure this is a float
price_per_download = 2.99
growth_rate = 0.15  # 15% monthly growth

# Create DataFrame
df = pd.DataFrame({'Month': months, 'Downloads': [
                  0.0]*18, 'Revenue': [0.0]*18})

# Revenue calculation
for month in months:
    if month == 5:  # First month of sales
        df.loc[month-1, 'Downloads'] = initial_downloads
        df.loc[month-1, 'Revenue'] = initial_downloads * price_per_download
    elif 6 <= month <= 12:  # Growth phase
        df.loc[month-1, 'Downloads'] = df.loc[month -
                                              2, 'Downloads'] * (1 + growth_rate)
        df.loc[month-1, 'Revenue'] = df.loc[month -
                                            1, 'Downloads'] * price_per_download
    elif month > 12:  # Flat sales
        # Month 12 downloads carried forward
        df.loc[month-1, 'Downloads'] = df.loc[11, 'Downloads']
        df.loc[month-1, 'Revenue'] = df.loc[month -
                                            1, 'Downloads'] * price_per_download

# Export to Excel
df.to_excel('revenue_report1.xlsx', index=False)

# Other parts of the script remain unchanged

# Plotting the DataFrame as a table and saving as PNG
fig, ax = plt.subplots(figsize=(12, 4))  # Adjust the figure size as needed
ax.axis('tight')
ax.axis('off')
# Make sure 'colColours' has the same number of colors as the number of columns
tbl = ax.table(cellText=df.values, colLabels=df.columns, loc='center',
               cellLoc='center', colColours=["palegreen"]*len(df.columns))
tbl.auto_set_font_size(False)
tbl.set_fontsize(12)
tbl.scale(1, 1.5)  # Adjust the scaling as needed for your display
plt.savefig('revenue_table.png', bbox_inches='tight', pad_inches=0.05, dpi=300)


# If Visual Studio Code terminal does not show the image,
# It will still be saved in the current directory as 'revenue_table.png'
