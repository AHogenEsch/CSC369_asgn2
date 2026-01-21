import duckdb
DATA_FILE_PATH = '2022_place_canvas_history.csv'
# DATA_FILE_PATH = 'testplacedata.csv'
RPLACE_WIDTH = 2000
# DuckDB can run SQL directly on the CSV file
query = """
    SELECT pixel_color, coordinate, COUNT(*) as count
    FROM {DATA_FILE_PATH}
    WHERE timestamp LIKE '2022-04-01 12%'
    GROUP BY pixel_color, coordinate
    ORDER BY count DESC
    LIMIT 1
"""
# Get the result
result = duckdb.sql(query).fetchone()