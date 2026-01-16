import duckdb

# DuckDB can run SQL directly on the CSV file
query = """
    SELECT pixel_color, coordinate, COUNT(*) as count
    FROM '2022_place_canvas_history.csv'
    WHERE timestamp LIKE '2022-04-01 12%'
    GROUP BY pixel_color, coordinate
    ORDER BY count DESC
    LIMIT 1
"""

result = duckdb.sql(query).fetchone()