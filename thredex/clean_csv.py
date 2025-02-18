import pandas as pd

# Path to your CSV file
file_path = "services.csv"

# Load the CSV file
csv_data = pd.read_csv(file_path)

# Strip whitespace from column names
csv_data.columns = csv_data.columns.str.strip()

# Save the cleaned CSV file
cleaned_file_path = "cleaned_services.csv"
csv_data.to_csv(cleaned_file_path, index=False)

print(f"Cleaned CSV file saved to {cleaned_file_path}")
