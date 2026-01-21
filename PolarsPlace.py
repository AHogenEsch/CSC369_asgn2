import sys
import polars as pl
import time
from datetime import datetime

DATA_FILE_PATH = '2022_place_canvas_history.csv'
RPLACE_WIDTH = 2000

def analyze_rplace(start_str, end_str, file_path=DATA_FILE_PATH):
    # Parse input strings for validation
    try:
        start_time = datetime.strptime(start_str, "%Y-%m-%d %H")
        end_time = datetime.strptime(end_str, "%Y-%m-%d %H")
    except ValueError as e:
        print(f"Error parsing input dates: {e}")
        return

    if end_time <= start_time:
        print("Error: End hour must be after start hour.")
        return

    # Start performance timer
    start_perf = time.perf_counter_ns()

    try:
        print(f"Executing Polars Lazy Query on {file_path}...")

        # Define the Lazy Query
        # scan_csv doesn't load the file, it just points to it.
        query = (
            pl.scan_csv(file_path)
            # Filter rows where the timestamp is between start_str and end_str
            # Chopping the string to "YYYY-MM-DD HH"
            .filter(
                (pl.col("timestamp").str.slice(0, 13) >= start_str) & 
                (pl.col("timestamp").str.slice(0, 13) < end_str)
            )
            .select([
                # Get the most frequent color
                pl.col("pixel_color").value_counts(sort=True).first().alias("top_color"),
                # Get the most frequent coordinate
                pl.col("coordinate").value_counts(sort=True).first().alias("top_pixel")
            ])
        )

        # Collect the results (This is where the actual computation happens)
        result = query.collect()

        

        # Extract data from the resulting DataFrame
        if result.height > 0 and result["top_color"][0] is not None:
            # Polars value_counts returns a struct {pixel_color: val, count: num}
            # Extract the inner value using ['field_name']
            most_common_color = result["top_color"][0]["pixel_color"]
            most_common_raw_pixel = result["top_pixel"][0]["coordinate"]

            # Coordinate Math
            try:
                clean_index = int(str(most_common_raw_pixel).replace(',', ''))
                x = clean_index % RPLACE_WIDTH
                y = clean_index // RPLACE_WIDTH
                formatted_pixel = f"({x}, {y})"
            except ValueError:
                formatted_pixel = most_common_raw_pixel
                
            # End timing
            execution_time_ms = (time.perf_counter_ns() - start_perf) // 1_000_000

            print(f"\n--- Final Results (Polars) ---")
            print(f"Timeframe: {start_str} to {end_str}")
            print(f"Execution Time: {execution_time_ms} ms")
            print(f"Most Placed Color: {most_common_color}")
            print(f"Most Placed Pixel Location: {formatted_pixel}")
        else:
            print("No data found for the selected timeframe.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python PolarsPlace.py 2022-04-04 12 2022-04-04 13")
    else:
        start_arg = f"{sys.argv[1]} {sys.argv[2]}"
        end_arg = f"{sys.argv[3]} {sys.argv[4]}"
        analyze_rplace(start_arg, end_arg)