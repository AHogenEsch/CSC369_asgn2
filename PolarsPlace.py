import polars as pl

# Use scan_csv for 'Lazy' mode 
query = (
    pl.scan_csv('2022_place_canvas_history.csv')
    .filter(pl.col("timestamp").str.starts_with("2022-04-01 12"))
    .select([
        pl.col("pixel_color").value_counts(sort=True).first(),
        pl.col("coordinate").value_counts(sort=True).first()
    ])
)

# This is where the work actually happens
result = query.collect() 