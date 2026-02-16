import pandas as pd

def run_data_factory(file_name):
    try:
        # Load the raw material
        df = pd.read_csv(file_name)
        print("--- RAW DATA RECEIVED ---")
        print(df)

        # FIX 1: Remove rows where the 'Task' is empty
        df_cleaned = df.dropna(subset=['Task'])
        
        # FIX 2: Fill missing 'Priority' with 'Standard'
        df_cleaned['Priority'] = df_cleaned['Priority'].fillna('Standard')
        
        # FIX 3: Fill missing 'Status' with 'In Progress'
        df_cleaned['Status'] = df_cleaned['Status'].fillna('In Progress')

        # Export the 'Refined' product
        df_cleaned.to_csv('cleaned_data.csv', index=False)
        print("\n--- DATA REFINED & SAVED AS 'cleaned_data.csv' ---")
        print(df_cleaned)
        
    except Exception as e:
        print(f"Factory Error: {e}")

# Push the 'Start' button
run_data_factory('sample_data.csv')