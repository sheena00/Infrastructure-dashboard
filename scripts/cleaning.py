import pandas as pd
import os

folder_path = r"C:\Users\LENOVO\OneDrive - Apata Africa Limited\Desktop\python-dashboard"

# Adding category column to file
# List of your Excel files and the category you want to assign
files = {
    "Water.xlsx": "Water",
    "Electricity.xlsx": "Electricity",
    "Climate.xlsx": "Climate",
    "Internet.xlsx": "Internet",
    "Transport.xlsx": "Transport"
}

# Indicator renaming dictionary
indicator_names = {
    "[B-READY] Percent of firms experiencing water insufficiencies": "Firms with water shortages (%)",
    "Average number of water insufficiencies in a typical month": "Average water shortages per month",
    "Average duration, in hours, of a typical water shortage": "Water shortage duration (hrs)",
    "[B-READY] Days to obtain a water connection [median]": "Days to get water connection(median)",
    "[B-READY] Days to obtain a water connection": "Days to get water connection",
    "Percent of firms identifying transportation as a major or very severe constraint":"Firms with transport as major constraint(%)",
    "[B-READY] Average perceptions index of transportation as a constraint":"Transport constraint perception index",
    "[B-READY] Percent of firms experiencing internet disruptions":"Firms facing internet disruption(%)",
    "[B-READY] Days to obtain internet connection [median]": "Days to obtain internet(median)",
    "Percent of firms experiencing electrical outages": "Firms facing electrical outages(%)",
    "[B-READY] Average number of electrical outages in a typical month":"Average electrical outages per month",
    "[B-READY] Duration, in hours, of a typical electrical outage [median]":"Hours for electrical outage(median)",
    "[B-READY] Losses due to electrical outages (% of annual sales) [median]":"Loss due to electrical outage(median)",
    "[B-READY] Percent of firms owning or sharing a generator":"Firms with generator(%)",
    "[B-READY] Days to obtain an electrical connection, upon application [median]":"Days to get electricity after application(median)",
    "[B-READY] Days to obtain an electrical connection, upon application":"Days to get electricity after application",
    "Percent of firms identifying electricity as a major or very severe constraint":"Firms with electricity as major constraint(%)",
    "Percent of firms experiencing damage of physical assets due to extreme weather":"Firms with damage of assets due to extreme weather(%)",
    "Percent of firms monitoring own CO2 emissions over last 3 years":"Firms monitoring CO2 emissions(%)",
    "Percent of firms adopting energy management measures to reduce emissions over last 3 years":"Firms adopting management measures to reduce emissions(%)"
}




for file_name, category in files.items():
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_excel(file_path)
    
    # Replace/Add Category column
    df['Category'] = category
    
     # Rename indicators
    df["Indicator"] = df["Indicator"].replace(indicator_names)
    # Save back to the same file
    df.to_excel(file_path, index=False)
    print(f"Updated {file_name} with Category = {category}")


#excel files in folder. Remember that this uses all excel files in that folder
excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
print("Found files:", excel_files)

dfs = []

for file in excel_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_excel(file_path, na_values=['n.a.'])
    dfs.append(df)

# Appending files together
combined_df = pd.concat(dfs, ignore_index=True, sort=False)

print("Combined data shape:", combined_df.shape)
print(combined_df.head())

# Getting a  list of country columns (all except 'Indicator' and 'Indicator Code')
country_cols = [col for col in combined_df.columns if col not in ['Indicator', 'Indicator Code','Category']]

# Melt to long format
long_df = combined_df.melt(
    id_vars=['Indicator', 'Indicator Code','Category'],
    value_vars=country_cols,
    var_name='Country',
    value_name='Value'
)


# Splitting Country column into Country and Year

long_df[['Country', 'Year']] = long_df['Country'].str.split(' (', expand=True, regex=False)
long_df['Year'] = long_df['Year'].str.replace(')', '', regex=False)

print(long_df.head())



#saving my excel file
output_path = os.path.join(folder_path, "clean_data.xlsx")

long_df.to_excel(output_path, index=False) #no extra column
print("File saved successfully!")
