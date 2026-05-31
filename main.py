import pandas as pd
import glob
import os

# 1. Define the path where your files were extracted
# (Adjust this path if your directory name is different)
data_folder = "./"

# 2. Use glob to find all files starting with 'data-'
# This matches data-01, data-02, up to data-70
file_pattern = os.path.join(data_folder, "data-*")
all_files = glob.glob(file_pattern)

# Sort the files alphabetically so patient IDs align nicely
all_files.sort()

# 3. Create an empty list to hold dataframes for each patient
patient_dfs = []

print(f"Starting batch import of {len(all_files)} patient records...")

# 4. Loop through each file and process it
for file_path in all_files:
    # Extract the file name (e.g., 'data-01')
    file_name = os.path.basename(file_path)
    
    # Extract the number to use as a unique Patient ID
    patient_id = file_name.split("-")[1]
    
    try:
        # Read the tab-separated file. 
        # These files don't have headers, so we define them manually.
        single_patient_df = pd.read_csv(
            file_path, 
            sep='\t', 
            names=['date', 'time', 'code', 'value'],
            header=None,
            dtype={'code': int, 'value': str} # Keep value as string initially to catch mixed formatting
        )
        
        # Add the tracking ID to this patient's rows
        single_patient_df['patient_id'] = f"Patient_{patient_id}"
        
        # Append to our master list
        patient_dfs.append(single_patient_df)
        
    except Exception as e:
        print(f"Error reading {file_name}: {e}")

# 5. Concatenate all separate dataframes into one master dataframe
master_df = pd.concat(patient_dfs, ignore_index=True)

print("\n--- Batch Import Complete ---")
print(f"Total rows loaded: {master_df.shape[0]}")
print(f"Total unique patients: {master_df['patient_id'].nunique()}")


# Convert values to numeric, turning corrupted strings or blanks into NaN
master_df['value'] = pd.to_numeric(master_df['value'], errors='coerce')

# Drop missing values to keep our analysis clean
master_df = master_df.dropna(subset=['value'])

# Look at the distribution of records per patient
print("\nTop 5 patients with the most recorded clinical events:")
print(master_df['patient_id'].value_counts().head())

# Show a quick breakdown of records by clinical codes
print("\nTotal record counts per clinical code:")
print(master_df['code'].value_counts())




# Export to a single CSV file for Python/Excel dashboards
master_df.to_csv("consolidated_diabetes_records.csv", index=False)
print("\nSaved as 'consolidated_diabetes_records.csv'")