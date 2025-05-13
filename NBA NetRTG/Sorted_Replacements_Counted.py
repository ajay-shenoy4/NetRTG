import pandas as pd
import os
import matplotlib.pyplot as plt

# Define input and output folders
input_folder = "CSV Files"
output_folder = "CSV Files"
graph_folder = "Graphs"

# Ensure the Graphs folder exists
os.makedirs(graph_folder, exist_ok=True)

# Load the CSV file
input_path = os.path.join(input_folder, "highlighted_points_sorted.csv")
data = pd.read_csv(input_path)

# Process "Player Removed" column
removed_df = data.groupby("Player Removed").agg(
    Count=("Player Removed", "count"),
    Cumulative_Minutes=("Substituted Minutes", "sum"),
    Cumulative_NETRTG=("NETRTG Difference", "sum")
).reset_index()
removed_df["Added/Removed"] = "Removed"
removed_df.rename(columns={"Player Removed": "Player"}, inplace=True)

# Process "Player Added" column
added_df = data.groupby("Player Added").agg(
    Count=("Player Added", "count"),
    Cumulative_Minutes=("Substituted Minutes", "sum"),
    Cumulative_NETRTG=("NETRTG Difference", "sum")
).reset_index()
added_df["Added/Removed"] = "Added"
added_df.rename(columns={"Player Added": "Player"}, inplace=True)

# Combine both dataframes
final_df = pd.concat([removed_df, added_df], ignore_index=True)

# Flip NETRTG for removed players
final_df.loc[final_df["Added/Removed"] == "Removed", "Cumulative_NETRTG"] *= -1

# Reorder columns
final_df = final_df[["Player", "Added/Removed", "Count", "Cumulative_Minutes", "Cumulative_NETRTG"]]

# Sort by Cumulative_NETRTG in descending order
final_df = final_df.sort_values(by="Cumulative_NETRTG", ascending=False)

# Save the results to a new CSV file
output_path = os.path.join(output_folder, "player_netrtg_summary.csv")
final_df.to_csv(output_path, index=False)

# Create scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(final_df["Cumulative_Minutes"], final_df["Cumulative_NETRTG"], alpha=0.7, color="black")

# Add labels for players meeting criteria
for _, row in final_df.iterrows():
    if row["Cumulative_Minutes"] > 750 or abs(row["Cumulative_NETRTG"]) > 74:
        plt.text(row["Cumulative_Minutes"], row["Cumulative_NETRTG"], row["Player"], fontsize=9, ha="right", va="bottom")

plt.axhline(0, color='black', linewidth=0.8, linestyle="--")  # Horizontal line at 0
plt.xlabel("Cumulative Minutes")
plt.ylabel("Adjusted Cumulative NETRTG")
plt.title("Impact of Player Additions and Removals on NETRTG")

# Save the graph to the Graphs folder
graph_path = os.path.join(graph_folder, "player_netrtg_scatterplot.png")
plt.savefig(graph_path, dpi=300, bbox_inches="tight")

# Show plot
plt.show()

# Print confirmation
print(f"Player NETRTG summary saved at: {output_path}")
print(f"Scatter plot saved at: {graph_path}")

#ADD FOR THE DOTS TO HAVE COLOR BY TEAM