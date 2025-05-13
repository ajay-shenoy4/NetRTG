import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Define the folder where the CSV files are stored
folder_path = "CSV Files"
graph_path = "Graphs"

# Load the CSV file from the CSV Files folder
file_path = os.path.join(folder_path, "table_data_filtered_50.csv")
data = pd.read_csv(file_path)

# Extract relevant columns
offensive_ratings = data["OFFRTG"]
defensive_ratings = data["DEFRTG"]
lineups = data["LINEUPS"]

# Calculate mean point
mean_offrtg = offensive_ratings.mean()
mean_defrtg = defensive_ratings.mean()
mean_point = (mean_offrtg, mean_defrtg)

# Calculate distances and filter points 15 units or more from the mean
distances = np.sqrt((offensive_ratings - mean_offrtg)**2 + (defensive_ratings - mean_defrtg)**2)
data["Distance"] = distances  # Add distances to the DataFrame

# Filter points 15 units or more from the mean
highlighted_points = data[data["Distance"] >= 15]

# Sort the highlighted points by NETRTG
highlighted_points_sorted = highlighted_points.sort_values(by="NETRTG", ascending=False)

# Save the sorted highlighted points to a new CSV file in the CSV Files folder
output_path = os.path.join(folder_path, "highlighted_lineups_sorted_Greater_50_Mins.csv")
highlighted_points_sorted.to_csv(output_path, index=False)

# Plot the scatterplot
plt.figure(figsize=(10, 6))
plt.scatter(offensive_ratings, defensive_ratings, label="Data Points", alpha=0.7)
plt.scatter(mean_offrtg, mean_defrtg, color="red", label="Mean Point", s=100)

# Highlight points 15 units away
plt.scatter(
    highlighted_points["OFFRTG"], 
    highlighted_points["DEFRTG"], 
    color="orange", 
    label="Points ≥ 15 Units from Mean With > 50 Mins Played", 
    edgecolor="black"
)

# Annotate highlighted points with lineup names
for _, row in highlighted_points.iterrows():
    plt.text(
        row["OFFRTG"], 
        row["DEFRTG"] - 0.5,  # Slightly below the point
        row["LINEUPS"], 
        fontsize=8, 
        ha="center", 
        color="black"
    )

# Add labels and legend
plt.xlabel("OFFRTG")
plt.ylabel("DEFRTG")
plt.title("Scatterplot of OFFRTG vs DEFRTG with Highlighted Points With > 50 Mins Played")
plt.legend()
plt.grid(alpha=0.5)

# Invert the y-axis
plt.gca().invert_yaxis()

# Save the plot
plot_path = os.path.join(graph_path, "scatterplot_with_mean_and_highlights_annotated_Greater_50_Mins.png")
plt.savefig(plot_path, dpi=300)
plt.show()

# Print confirmation
print(f"Highlighted lineups (≥ 15 units from mean) have been saved to '{graph_path}'.")
