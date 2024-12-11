import os

import pandas as pd
import matplotlib.pyplot as plt

# Define input CSV file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV_PATH = os.path.join(BASE_DIR, "..", "data", "tenders.csv")

# Load data
df = pd.read_csv(INPUT_CSV_PATH)

# Analysis: Number of tenders by organization
organization_counts = df['organization'].value_counts()
print("Number of tenders by organization:")
print(organization_counts)

# **Solution 1: Limit to Top N Organizations**
TOP_N = 10  # You can adjust this number
top_organizations = organization_counts.head(TOP_N)

# **Solution 2: Adjust Figure Size and Rotate Labels**
plt.figure(figsize=(12, 8))
top_organizations.plot(kind='bar')
plt.title(f'Top {TOP_N} Organizations by Number of Tenders')
plt.xlabel('Organization')
plt.ylabel('Number of Tenders')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Adjust layout to make room for rotated labels
plt.tight_layout()

plt.show()

# Analysis: Average budget
if 'budget' in df.columns:
    avg_budget = df['budget'].mean()
    print(f"\nAverage budget of tenders: {avg_budget:.2f}")
else:
    print("\nThe 'budget' column is not available in the data.")

# Visualization: Tenders published by date
df['publish_date'] = pd.to_datetime(df['publish_date'], errors='coerce')  # Convert to datetime format
date_analysis = df['publish_date'].value_counts().sort_index()

# **Solution 3: Plot Date Analysis**
plt.figure(figsize=(12, 6))
date_analysis.plot(kind='line')
plt.title('Tenders by Publish Date')
plt.xlabel('Date')
plt.ylabel('Number of Tenders')
plt.grid(True)
plt.tight_layout()
plt.show()