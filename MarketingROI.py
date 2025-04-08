#1. Imports
import pandas as pd
import matplotlib.pyplot as plt
#2. Load the dataset
df = pd.read_csv(r'C:\Users\User\Desktop\Projects\Marketing ROI project\marketing_campaign.csv',sep=';')
#3.Clean and Transform
df.fillna(df['Income'].median(), inplace=True)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df.shape)
print(df.columns)
print(df.head(3))
print(df.isnull().sum())

# Basic stats
print(df.describe())

# Check unique values for campaign columns
print(df['Response'].value_counts())  # Who responded to campaign
#Calculate total customer spending across all product categories
product_cols = ['MntWines', 'MntFruits', 'MntMeatProducts',
                'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
df['Total_Spent']= df[product_cols].sum(axis=1)
#4. Grouped analysis
response_group = df.groupby('Response')['Total_Spent'].agg(['count', 'sum', 'mean']).reset_index()
response_group.columns = ['Responded', 'Customers', 'Total_Revenue', 'Avg_Revenue_Per_Customer']
print(response_group)
edu_response = df.groupby(['Education', 'Response'],observed= True).size().unstack().fillna(0)
edu_response['Response_Rate (%)'] = (edu_response[1] / (edu_response[0] + edu_response[1])) * 100
print(edu_response)
df['Age'] = 2025 - df['Year_Birth']
df['Age_Group'] = pd.cut(df['Age'], bins=[18, 30, 45, 60, 80], labels=['18-30', '31-45', '46-60', '61-80'])
df.groupby(['Marital_Status', 'Response']).size().unstack()
age_response = df.groupby(['Age_Group', 'Response'],observed=True).size().unstack().fillna(0)
age_response['Response_Rate (%)'] = (age_response[1] / (age_response[0] + age_response[1])) * 100
print(age_response)

#5. A tiny bit of visualization and more grouping
age_response['Response_Rate (%)'].plot(kind='bar', color='skyblue', edgecolor='black')

plt.title('Campaign Response Rate by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Response Rate (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
# Add estimated cost
estimated_cost_per_response = 50
response_group['Estimated_Cost'] = response_group['Customers'] * estimated_cost_per_response
response_group['ROI (%)'] = ((response_group['Total_Revenue'] - response_group['Estimated_Cost']) / response_group['Estimated_Cost']) * 100
print(response_group)
group = df.groupby(['Age_Group', 'Response'],observed = True)['Total_Spent'].agg(['count', 'sum']).reset_index()
group['Estimated_Cost'] = group['count'] * 50  # or whatever new cost you choose
group['ROI (%)'] = ((group['sum'] - group['Estimated_Cost']) / group['Estimated_Cost']) * 100
group=group.round(2)

print(group)
# Group by Education and Response, get total customers and spending
edu_roi = df.groupby(['Education', 'Response'])['Total_Spent'].agg(['count', 'sum']).reset_index()
edu_roi.columns = ['Education', 'Responded', 'Customers', 'Total_Revenue']

# Add cost assumption (e.g., $50 per customer targeted)
estimated_cost_per_customer = 50
edu_roi['Estimated_Cost'] = edu_roi['Customers'] * estimated_cost_per_customer
edu_roi['ROI (%)'] = ((edu_roi['Total_Revenue'] - edu_roi['Estimated_Cost']) / edu_roi['Estimated_Cost']) * 100
edu_roi = edu_roi.round(2)

print(edu_roi)
# Group by Education, Age Group, and Response
combo_roi = df.groupby(['Education', 'Age_Group', 'Response'],observed = True)['Total_Spent'].agg(['count', 'sum']).reset_index()
combo_roi.columns = ['Education', 'Age_Group', 'Responded', 'Customers', 'Total_Revenue']
combo_roi['Estimated_Cost'] = combo_roi['Customers'] * estimated_cost_per_customer
combo_roi['ROI (%)'] = ((combo_roi['Total_Revenue'] - combo_roi['Estimated_Cost']) / combo_roi['Estimated_Cost']) * 100
combo_roi = combo_roi.round(2)

print(combo_roi)
df['Income_Group'] = pd.cut(df['Income'], bins=[0, 30000, 60000, 90000, 200000],
                            labels=['Low', 'Mid', 'High', 'Very High'])

#6. Exporting the final data
cols_to_keep = [
    'ID', 'Education', 'Marital_Status', 'Age', 'Age_Group', 'Income', 'Income_Group',
    'Response', 'Total_Spent', 'MntWines', 'MntFruits', 'MntMeatProducts',
    'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
]
df['Income_Group'] = df['Income_Group'].cat.add_categories(['Unknown'])
df.fillna({'Income_Group': 'Unknown'}, inplace=True)

df_final = df[cols_to_keep].copy()
df_final.to_csv(r'C:\Users\User\Desktop\Projects\Marketing ROI project/final_marketing_data.csv', index=False)

print("Final dataset exported and ready for Power BI!")