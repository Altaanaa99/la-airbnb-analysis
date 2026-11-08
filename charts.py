# charts.py
# Makes 4 charts from the clean LA Airbnb data

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("listings_clean.csv")
color = "#FF5A5F"  # Airbnb-style coral

# Chart 1: Listings by room type
rooms = df["room_type"].value_counts().sort_values()
plt.figure(figsize=(8, 4))
plt.barh(rooms.index, rooms.values, color=color)
plt.title("LA Airbnb Listings by Room Type")
plt.xlabel("Number of listings")
plt.tight_layout()
plt.savefig("chart1_room_types.png", dpi=150)
plt.close()

# Chart 2: Top 10 most expensive neighborhoods (50+ listings)
hood = df.groupby("neighborhood")["price"].agg(["count", "median"])
top10 = hood[hood["count"] >= 50].sort_values("median").tail(10)
plt.figure(figsize=(10, 5))
plt.barh(top10.index, top10["median"], color=color)
plt.title("Top 10 Most Expensive LA Neighborhoods (median price per night)")
plt.xlabel("Median price ($)")
plt.tight_layout()
plt.savefig("chart2_expensive_neighborhoods.png", dpi=150)
plt.close()

# Chart 3: Average rating by price range
rated = df.dropna(subset=["rating"]).copy()
bins = [0, 100, 200, 300, 500, 10000]
labels = ["Up to $100", "$101-200", "$201-300", "$301-500", "$501+"]
rated["price_range"] = pd.cut(rated["price"], bins=bins, labels=labels)
avg = rated.groupby("price_range", observed=True)["rating"].mean()
plt.figure(figsize=(8, 4))
bars = plt.bar(avg.index, avg.values, color=color)
plt.bar_label(bars, fmt="%.2f")
plt.ylim(4.5, 5)
plt.title("Average Rating by Price Range (axis starts at 4.5)")
plt.ylabel("Average rating")
plt.tight_layout()
plt.savefig("chart3_rating_by_price.png", dpi=150)
plt.close()

# Chart 4: Share of listings by host size
df["host_type"] = pd.cut(df["host_listings"], bins=[0, 1, 9, 100000],
                         labels=["1 listing", "2-9 listings", "10+ listings"])
share = df["host_type"].value_counts(normalize=True).sort_index() * 100
plt.figure(figsize=(7, 4))
bars = plt.bar(share.index.astype(str), share.values, color=color)
plt.bar_label(bars, fmt="%.0f%%")
plt.title("Share of LA Airbnb Listings by Host Size")
plt.ylabel("% of listings")
plt.tight_layout()
plt.savefig("chart4_host_size.png", dpi=150)
plt.close()

print("Saved 4 charts!")