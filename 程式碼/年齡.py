import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # Mac使用

# Load the CSV file
file_path = '刑事案件嫌疑犯人數－按案類及年齡層別.csv'
data = pd.read_csv(file_path)

# Extracting the relevant data for plotting
crime_types = data.iloc[2, 4:].dropna().tolist()  # Crime types from the header

# Extracting age group data for each crime type
age_groups = ['兒童', '少年', '青年', '成年', '不詳']
age_group_data = data.iloc[6:11, 4:].dropna(axis=1)

# Clean the data by removing non-numeric values and converting to integers
age_group_data_clean = age_group_data.apply(lambda x: x.str.replace(',', '').apply(lambda y: int(y) if y.replace(',', '').isdigit() else 0))

# Plotting a stacked bar chart
plt.figure(figsize=(14, 8))

# Plot each age group as a segment in the stacked bar
bottom = None
for i, age_group in enumerate(age_groups):
    values = age_group_data_clean.iloc[i].tolist()
    plt.bar(crime_types, values, bottom=bottom, label=age_group)
    if bottom is None:
        bottom = values
    else:
        bottom = [b + v for b, v in zip(bottom, values)]

plt.xlabel('Crime Type')
plt.ylabel('Number of Suspects')
plt.title('Number of Criminal Case Suspects by Crime Type and Age Group (2015)')
plt.xticks(rotation=90)
plt.legend(title='Age Group')
plt.tight_layout()
plt.show()
