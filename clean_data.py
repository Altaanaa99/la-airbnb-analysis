# clean_data.py
# Cleans the Inside Airbnb Los Angeles listings data (September 2026)

import pandas as pd

# 1. Load the raw data
df = pd.read_csv("listings.csv")
print("Raw data:", df.shape[0], "rows,", df.shape[1], "columns")

# 2. Keep only the columns we need
columns = [
    "id", "name", "host_id", "host_is_superhost",
    "neighbourhood_cleansed", "neighbourhood_group_cleansed",
    "latitude", "longitude", "room_type", "accommodates", "bedrooms",
    "price", "minimum_nights", "availability_365",
    "number_of_reviews", "review_scores_rating",
    "calculated_host_listings_count",
]
df = df[columns]

# 3. Rename columns to simpler names
df = df.rename(columns={
    "neighbourhood_cleansed": "neighborhood",
    "neighbourhood_group_cleansed": "area",
    "calculated_host_listings_count": "host_listings",
    "review_scores_rating": "rating",
})

# 4. Clean the price: "$1,250.00" -> 1250.0
df["price"] = pd.to_numeric(
    df["price"].astype(str).str.replace(r"[$,]", "", regex=True),
    errors="coerce",
)
missing_price = df["price"].isna().sum()
df = df.dropna(subset=["price"])
print("Removed", missing_price, "listings with no price")

# 5. Remove extreme prices (top 1%)
cutoff = df["price"].quantile(0.99)
outliers = (df["price"] > cutoff).sum()
df = df[(df["price"] > 0) & (df["price"] <= cutoff)]
print(f"Removed {outliers} listings above ${cutoff:,.0f} per night (top 1%)")

# 6. Superhost: "t"/"f" -> True/False
df["host_is_superhost"] = df["host_is_superhost"].map({"t": True, "f": False})

# 7. Save the clean data
df.to_csv("listings_clean.csv", index=False)
print("Clean data:", df.shape[0], "rows,", df.shape[1], "columns")
print("Saved to listings_clean.csv")
