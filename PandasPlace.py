import sys
import pandas as pd
import time
from datetime import datetime

DATA_FILE_PATH = '2022_place_canvas_history.csv'
RPLACE_WIDTH = 2000

def analyze_rplace(start_str, end_str, file_path=DATA_FILE_PATH):
    # Parse input strings into datetime objects for validation
    try:
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H")
    except ValueError as e:
        print(f"Error parsing input dates: {e}")
        print("Usage format: 'YYYY-MM-DD HH'")
        return

    if end_time <= start_time:
        print("Error: End hour must be after start hour.")
        return
    
    # Start performance timer
    start_perf = time.perf_counter_ns()

    try:
        print(f"Loading data from {file_path} into Pandas... ")
        # Don't need to load user ID, waste of memory
        df = pd.read_csv(file_path, usecols=['timestamp', 'pixel_color', 'coordinate'])

        # Convert timestamp column to datetime objects
        # errors='coerce' will turn unparseable dates into NaT (Not a Time) instead of crashing
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

        # Filter for the requested timeframe
        # Using the datetime objects directly for comparison
        mask = (df['timestamp'] >= start_time) & (df['timestamp'] < end_time)
        filtered_df = df.loc[mask]

        rows_matched = len(filtered_df)
        print(f"Rows Matched: {rows_matched}")

        if rows_matched > 0:
            # Find most common values using .mode() which returns a Series
            # if there is a tie, it returns multiple values, but I take the first one [0]
            most_common_color = filtered_df['pixel_color'].mode()[0]
            most_common_coord = filtered_df['coordinate'].mode()[0]

            # Coordinate Math (assuming the raw coordinate is an index string)
            try:
                clean_index = int(str(most_common_coord).replace(',', ''))
                x = clean_index % RPLACE_WIDTH
                y = clean_index // RPLACE_WIDTH
                formatted_pixel_coord = f"({x}, {y})"
            except ValueError:
                # If the coordinate is already "x,y", just use it as is
                formatted_pixel_coord = most_common_coord

            # End timing
            execution_time_ms = (time.perf_counter_ns() - start_perf) // 1_000_000

            print(f"\n--- Final Results (Pandas) ---")
            print(f"Timeframe: {start_str} to {end_str}")
            print(f"Execution Time: {execution_time_ms} ms")
            print(f"Most Placed Color: {most_common_color}")
            print(f"Most Placed Pixel Location: {formatted_pixel_coord}")
        else:
            print("No data found for the selected timeframe.")

    # Catching and logging errors
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except MemoryError:
        print("Error: The dataset is too large for your computer's RAM. Consider using Polars or DuckDB.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python PandasPlace.py 2022-04-01 12 2022-04-01 13")
    else:
        # Constructing the date strings from command line arguments
        start_arg = f"{sys.argv[1]} {sys.argv[2]}"
        end_arg = f"{sys.argv[3]} {sys.argv[4]}"
        analyze_rplace(start_arg, end_arg)