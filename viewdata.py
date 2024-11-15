import pandas as pd
import plotly.express as px

# Load the CSV data into a DataFrame
df = pd.read_csv('data/coefsoutput3.csv')  # Replace 'your_data.csv' with your actual file path

# Calculate mean for each year group
df_grouped = df.groupby('year')['coefficient'].mean().reset_index()
mean_values = df_grouped['coefficient'].tolist()

# Create the histogram
fig = px.histogram(df, x='coefficient', facet_col='year', title='Histogram of Coefficients by Year', 
                   category_orders={'year': [21, 22, 23, 24, 25, 26, 27, 28]}, 
                   color='year', log_y=2)

# Add annotations for mean values
fig.for_each_annotation(lambda a: a.update(text=f"Mean: {mean_values[a['x']]:.2f}"))

# Customize the plot (optional)
fig.update_layout(
    xaxis_title='coefficient',
    yaxis_title='Frequency',
    legend_title='Year',
)

# Show the plot
fig.show()