import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
data = pd.read_csv("D:/bysjcs/game.csv")

# Get the column names
column_names = data.columns.tolist()

# Separate the x and y values
x_columns = column_names[:-1]  # Exclude the last column ("评价值")
y_column = column_names[-1]  # Last column ("评价值")

# Configure Chinese font
plt.rcParams['font.sans-serif'] = ['SimHei']  # Use SimHei font for Chinese characters
plt.rcParams['axes.unicode_minus'] = False  # Disable minus sign as a Unicode character

# Create a scatter plot for each x column
for x_column in x_columns:
    # Get x and y values
    x_values = data[x_column]
    y_values = data[y_column]

    # Generate a unique color and marker for each x column
    color = plt.cm.viridis(x_columns.index(x_column) / len(x_columns))
    marker = 'o'

    # Plot the scatter plot
    plt.scatter(x_values, y_values, c=color, marker=marker, label=x_column)

# Set plot title and labels
plt.title("散点图")
plt.xlabel("X轴数值")
plt.ylabel("Y轴数值")

# Add a legend
plt.legend()

# Save the scatter plot as an image file
plt.savefig("D:/bysjcs/scatter_plot.png")

# Show the plot
plt.show()