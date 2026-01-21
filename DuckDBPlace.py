import sys
import duckdb
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
        return

    if end_time <= start_time:
        print("Error: End hour must be after start hour.")
        return
    
    # Start performance timer
    start_perf = time.perf_counter_ns()

    try:
        print(f"Running DuckDB SQL query on {file_path}...")

        # Build the SQL Query
        # We use f-strings to insert our variables into the SQL command.
        # Note: We use >= and < for the timeframe logic.
        query = f"""
            SELECT 
                pixel_color, 
                coordinate, 
                COUNT(*) as placement_count
            FROM '{file_path}'
            WHERE timestamp >= '{start_time}' AND timestamp < '{end_time}'
            GROUP BY pixel_color, coordinate
            ORDER BY placement_count DESC
            LIMIT 1
        """

        # Execute the query
        # fetchone() returns a tuple of the first row: (color, coordinate, count)
        result = duckdb.sql(query).fetchone()

        

        if result:
            most_common_color = result[0]
            most_common_raw_coord = result[1]

            # Coordinate Math
            try:
                clean_index = int(str(most_common_raw_coord).replace(',', ''))
                x = clean_index % RPLACE_WIDTH
                y = clean_index // RPLACE_WIDTH
                formatted_pixel_coord = f"({x}, {y})"
            except ValueError:
                formatted_pixel_coord = most_common_raw_coord

            # End timing
            execution_time_ms = (time.perf_counter_ns() - start_perf) // 1_000_000  

            print(f"\n--- Final Results (DuckDB) ---")
            print(f"Timeframe: {start_str} to {end_str}")
            print(f"Execution Time: {execution_time_ms} ms")
            print(f"Most Placed Color: {most_common_color}")
            print(f"Most Placed Pixel Location: {formatted_pixel_coord}")
        else:
            print("No data found for the selected timeframe.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python DuckDBPlace.py 2022-04-01 12 2022-04-01 13")
    else:
        start_arg = f"{sys.argv[1]} {sys.argv[2]}"
        end_arg = f"{sys.argv[3]} {sys.argv[4]}"
        analyze_rplace(start_arg, end_arg)