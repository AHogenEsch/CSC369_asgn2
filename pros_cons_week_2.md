# Week 2 Results
## Polars
**Pros:** 
- Doesn't process data until .collect() is called, allowing it to optimize how the query is ran.
- Multithreading makes use of all availible CPU cores
- Doesn't load the whole file, only specific data, reducing RAM usage
**Cons:**
- More complex result, to get a single value you index a dataframe, then Series, then a final struct.
- Lots of chained syntax, can make code hard to read
## Pandas
**Pros:** 
- Nice helper functions, support for complex tasks built in.
- Lots of documentation, easy to find answers to most questions
- the 2D table format is similar to Excel, a familiar tool. 
**Cons:**
- Loads the entire file into memory, was using 17.3GBs while running
- Single Threaded
- Eager Execution, performs each stpe immediately with no automatic query optimization

## DuckDB
**Pros:** 
- Fastest
- Uses SQL syntax, very readable
- "Out-of-core" processing, it "streams" the data directly from disk in batches, instead of loading the whole file into RAM.
**Cons:**
- You must be familiar with SQL
- passing variables into an SQL string requires careful formatring
- Less flexible for performing complex nuanced tasks that require math and logic outside of the standard SQL functions

My favorite was Polars, it felt intuitive to write once I learned how to use the different functions, and it analyzed the data very quickly. The filter and select functions were easy to understand and are very readable. The fastest was DuckDB, and if I was more familiar with SQL, that one would probably be my favorite. 

The most frequent issue I had was properly filtering the data by the timestamp. For Pandas it didn't like my initial attempt comparing a stripped timestamp that didn't have the timezone to the raw data, an I had to use .dt.tz_localize(None) on the .to_datetime call. In Polars, I was able to compare a slice of the timestamp instead of converting it to a datetime object when filtering, saving those extra opertaions. 