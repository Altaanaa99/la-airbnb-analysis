# analysis.py
# Answers 5 questions about LA Airbnb listings (September 2026)

import pandas as pd

df = pd.read_csv("listings_clean.csv")
print("Listings analyzed:", len(df))

# Q1. What types of places are listed, and what do they cost?
print("\nQ1. Listings and median price by room type")
q1 = df.groupby("room_type")["price"].agg(listings="count", median_price="median")
print(q1.sort_values("listings", ascending=False))

# Q2. Which neighborhoods are most expensive? (50+ listings only)
print("\nQ2. Top 10 most expensive neighborhoods (median price)")
hood = df.groupby("neighborhood")["price"].agg(listings="count", median_price="median")
hood = hood[hood["listings"] >= 50]
print(hood.sort_values("median_price", ascending=False).head(10))

# Q3. Do more expensive places get better ratings?
print("\nQ3. Average rating by price range")
rated = df.dropna(subset=["rating"]).copy()
bins = [0, 100, 200, 300, 500, 10000]
labels = ["Up to $100", "$101-200", "$201-300", "$301-500", "$501+"]
rated["price_range"] = pd.cut(rated["price"], bins=bins, labels=labels)
q3 = rated.groupby("price_range", observed=True)["rating"].agg(listings="count", avg_rating="mean")
print(q3.round(2))

# Q4. How much of LA Airbnb is run by hosts with many listings?
print("\nQ4. Share of listings by host size (%)")
df["host_type"] = pd.cut(df["host_listings"], bins=[0, 1, 9, 100000],
                         labels=["1 listing", "2-9 listings", "10+ listings"])
print(df["host_type"].value_counts(normalize=True).mul(100).round(1))

# Q5. Do Superhosts get better ratings?
print("\nQ5. Superhosts vs regular hosts")
q5 = df.groupby("host_is_superhost").agg(
    listings=("id", "count"),
    avg_rating=("rating", "mean"),
    median_price=("price", "median"),
)
print(q5.round(2))