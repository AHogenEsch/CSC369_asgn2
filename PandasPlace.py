import pandas as pd
import time

# Start timer
df = pd.read_csv('2022_place_canvas_history.csv')

# Convert timestamp column to actual dates
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter for the timeframe
mask = (df['timestamp'] >= '2022-04-01 12:00:00') & (df['timestamp'] < '2022-04-01 13:00:00')
filtered_df = df.loc[mask]

# Get most common
most_common_color = filtered_df['pixel_color'].mode()[0]
most_common_pixel = filtered_df['coordinate'].mode()[0]