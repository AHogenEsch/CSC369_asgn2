import polars as pl
DATA_FILE_PATH = '2022_place_canvas_history.csv'
# DATA_FILE_PATH = 'testplacedata.csv'
RPLACE_WIDTH = 2000

# Use scan_csv for 'Lazy' mode 
query = (
    pl.scan_csv(DATA_FILE_PATH)
    .filter(pl.col("timestamp").str.starts_with("2022-04-01 12"))
    .select([
        pl.col("pixel_color").value_counts(sort=True).first(),
        pl.col("coordinate").value_counts(sort=True).first()
    ])
)

# This is where the work actually happens
result = query.collect() 