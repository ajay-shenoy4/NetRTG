# Define the folder path for saving CSV files
folder_path = os.path.join(os.getcwd(), "CSV Files")
os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

csv_file_path = os.path.join(folder_path, "table_data_filtered_5.csv")
