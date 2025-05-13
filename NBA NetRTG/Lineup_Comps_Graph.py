import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the folders for input and output
input_folder = "CSV Files"
output_folder = "CSV Files"
graphs_folder = "Graphs"

# Load the CSV file from the CSV Files folder
input_path = os.path.join(input_folder, "similar_lineups_with_details.csv")
data = pd.read_csv(input_path)

# Ensure the output and graphs folders exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(graphs_folder, exist_ok=True)

# Extract the relevant columns: 'Substituted Minutes' and 'NETRTG Difference'
substituted_minutes = data["Substituted Minutes"]
netrtg_diff = data["NETRTG Difference"]

# Create a condition for highlighting points
highlight_condition = (
    (substituted_minutes > 300) |
    (netrtg_diff > 30) |
    (netrtg_diff < -30)
)

# Separate highlighted points
highlighted_points = data[highlight_condition]

#filter rows with less than 40 substituted minutes
highlighted_points = highlighted_points[highlighted_points["Substituted Minutes"] > 40]

# Select only the specified columns for saving
columns_to_save = [
    "Team 1",
    "Player Removed",
    "Player Added",
    "Substituted Minutes",
    "NETRTG Difference",
    "OFFRTG Difference",
    "DEFRTG Difference"
]
highlighted_points_filtered = highlighted_points[columns_to_save]

# Sort the DataFrame by NETRTG Difference in descending order
highlighted_points_sorted = highlighted_points_filtered.sort_values(by="NETRTG Difference", ascending=False)

# Save the sorted highlighted points to a new CSV file
highlighted_output_path = os.path.join(output_folder, "highlighted_points_sorted.csv")
highlighted_points_sorted.to_csv(highlighted_output_path, index=False)

# Print confirmation
print(f"Highlighted points sorted by NETRTG Difference saved at: {highlighted_output_path}")

# Create the scatter plot
plt.figure(figsize=(10, 6))

# Plot all points
plt.scatter(substituted_minutes, netrtg_diff, color='blue', alpha=0.7, label="Normal Points")

# Highlight points and annotate them
plt.scatter(
    highlighted_points["Substituted Minutes"],
    highlighted_points["NETRTG Difference"],
    color='red',
    alpha=0.7,
    label="Highlighted Points"
)

# Add annotations for highlighted points
for _, row in highlighted_points.iterrows():
    plt.text(
        row["Substituted Minutes"],
        row["NETRTG Difference"] - 2,  # Slightly below the point
        row["Player Added"],  # Name of the substituted player
        fontsize=8,
        color='darkred',
        ha='center'
    )

# Add labels, title, and legend
plt.xlabel("Substituted Minutes")
plt.ylabel("NETRTG Difference")
plt.title("Scatterplot of Substituted Minutes vs NETRTG Difference")
plt.legend()

# Add grid for better readability
plt.grid(True)

# Save the scatter plot as an image in the Graphs folder
scatterplot_output_path = os.path.join(graphs_folder, "scatterplot_highlighted_points_with_names.png")
plt.savefig(scatterplot_output_path, dpi=300)

# Display the plot
plt.show()

# Print confirmation
print(f"Scatterplot saved at: {scatterplot_output_path}")
