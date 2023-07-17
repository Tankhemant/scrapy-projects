import pandas as pd

# Example dictionary data
data = {
    'Name': ['John', 'Alice', 'Bob'],
    'Age': [25, 30, 35],
    'City': ['New York', 'London', 'Paris']
}

# Create a DataFrame from the dictionary
df = pd.DataFrame(data)

# Specify the file path to save the CSV file
file_path = 'data.csv'

# Save the DataFrame as a CSV file
df.to_csv(file_path, index=False)