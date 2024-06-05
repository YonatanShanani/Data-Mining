### IMPORTS ###
from typing import *
import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def analyze_data(dataset: pd.DataFrame) -> Dict:
    stats = {}
    numerical_columns = ['DollarsPledged', 'DollarsGoal', 'NumBackers', 'DaysToGo']

    for col in numerical_columns:
        col_data = dataset[col].dropna().values
        stats[col] = {
            'min': np.min(col_data),
            'max': np.max(col_data),
            'mean': np.mean(col_data),
            'std': np.std(col_data)
        }

    return stats

### LOAD FILES ###
output_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
os.makedirs(output_directory, exist_ok=True)
script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, '..', 'output', 'problem1.json')
with open(json_path) as f:
    data = json.load(f)


### DATAFRAME INIT ###
records = data['records']['record']
df = pd.DataFrame(records)
df['DollarsPledged'] = pd.to_numeric(df['DollarsPledged'], errors='coerce')
df['DollarsGoal'] = pd.to_numeric(df['DollarsGoal'], errors='coerce')
df['NumBackers'] = pd.to_numeric(df['NumBackers'], errors='coerce')
df['DaysToGo'] = pd.to_numeric(df['DaysToGo'], errors='coerce')
df.dropna(how='all', inplace=True)

### STATS ###
stats = analyze_data(df)

output_path = os.path.join(output_directory, 'problem2.json')
with open(output_path, 'w') as f:
    json.dump(stats, f, indent=4)

### BUILD HISTOGRAM ###
plt.figure(figsize=(10, 6))
plt.hist(df['DaysToGo'].dropna(), bins=20, color='blue', edgecolor='black', alpha=0.7)
plt.title('Distribution of DaysToGo', fontsize=16)
plt.xlabel('Days To Go', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(True)
plt.tight_layout()

histogram_output_path = os.path.join(output_directory, 'DaysToGo_histogram.png')
plt.savefig(histogram_output_path)
plt.show()

### VIZ DIST DollarsPledged with DollarsGoal ###
plt.figure(figsize=(10, 6))
plt.scatter(df['DollarsPledged'], df['DollarsGoal'], alpha=0.6, edgecolors='w', s=100)
plt.title('DollarsPledged vs DollarsGoal', fontsize=16)
plt.xlabel('Dollars Pledged', fontsize=14)
plt.ylabel('Dollars Goal', fontsize=14)
plt.grid(True)
plt.tight_layout()

dollars_pledged_vs_goal_output_path = os.path.join(output_directory, 'DollarsPledged_vs_DollarsGoal.png')
plt.savefig(dollars_pledged_vs_goal_output_path)
plt.show()

### VIZ DIST DollarsPledged with DollarsGoal ###
plt.figure(figsize=(10, 6))
plt.scatter(df['DollarsPledged'], df['NumBackers'], alpha=0.6, edgecolors='w', s=100)
plt.title('DollarsPledged vs NumBackers', fontsize=16)
plt.xlabel('Dollars Pledged', fontsize=14)
plt.ylabel('Number of Backers', fontsize=14)
plt.grid(True)
plt.tight_layout()

dollars_pledged_vs_backers_output_path = os.path.join(output_directory, 'DollarsPledged_vs_NumBackers.png')
plt.savefig(dollars_pledged_vs_backers_output_path)
plt.show()


print("Exit Success")
