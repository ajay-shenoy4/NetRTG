import pandas as pd
import os

# Define the folder where the CSV files are stored
input_folder = "CSV Files"
output_folder = "CSV Files"

# Load the CSV file from the CSV Files folder
input_path = os.path.join(input_folder, "table_data_filtered_25.csv")
data = pd.read_csv(input_path)

# Ensure the CSV Files folder exists for output
os.makedirs(output_folder, exist_ok=True)

# Function to find similar lineups and include requested information
def find_similar_lineups(data):
    # Split the LINEUPS column into individual players
    data["Players"] = data["LINEUPS"].apply(lambda x: set(x.split(" - ")))

    # Create a list to store matching lineups
    similar_lineups = []

    # Compare each lineup against the others
    for i, row1 in data.iterrows():
        for j, row2 in data.iterrows():
            if i >= j:  # Avoid duplicate comparisons and self-comparison
                continue
            # Find the intersection of players
            common_players = row1["Players"].intersection(row2["Players"])
            if len(common_players) == 4:  # If they share 4 out of 5 players
                # Identify the player removed and added
                player_removed = next(iter(row1["Players"] - row2["Players"]), None)
                player_added = next(iter(row2["Players"] - row1["Players"]), None)

                # Calculate differences in ratings
                offrtg_diff = row2["OFFRTG"] - row1["OFFRTG"]
                defrtg_diff = row2["DEFRTG"] - row1["DEFRTG"]
                netrtg_diff = row2["NETRTG"] - row1["NETRTG"]

                # Calculate substituted minutes
                substituted_minutes = row1["MIN"] - row2["MIN"]

                # Append the results to the list
                similar_lineups.append({
                    "Lineup 1": row1["LINEUPS"],
                    "Team 1": row1["TEAM"],
                    "GP 1": row1["GP"],
                    "MIN 1": row1["MIN"],
                    "OFFRTG 1": row1["OFFRTG"],
                    "DEFRTG 1": row1["DEFRTG"],
                    "NETRTG 1": row1["NETRTG"],
                    "Lineup 2": row2["LINEUPS"],
                    "Team 2": row2["TEAM"],
                    "GP 2": row2["GP"],
                    "MIN 2": row2["MIN"],
                    "OFFRTG 2": row2["OFFRTG"],
                    "DEFRTG 2": row2["DEFRTG"],
                    "NETRTG 2": row2["NETRTG"],
                    "Common Players": ", ".join(common_players),
                    "Player Removed": player_removed,
                    "Player Added": player_added,
                    "OFFRTG Difference": offrtg_diff,
                    "DEFRTG Difference": defrtg_diff,
                    "NETRTG Difference": netrtg_diff,
                    "Substituted Minutes": substituted_minutes,  # New column for substituted minutes
                })

    # Convert results to a DataFrame
    similar_lineups_df = pd.DataFrame(similar_lineups)
    return similar_lineups_df

# Find similar lineups
similar_lineups_df = find_similar_lineups(data)

# Save the results to a CSV file in the CSV Files folder
output_path = os.path.join(output_folder, "similar_lineups_with_details.csv")
similar_lineups_df.to_csv(output_path, index=False)

# Print the result
print(f"CSV file saved at: {output_path}")
print(similar_lineups_df)
