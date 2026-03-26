import pandas as pd

# 1. Load dataset
data = pd.read_csv("data/imdb_data.csv")

# 2. Select only 3 columns
clean_data = data[["Title", "genre", "Synopsis","Director","Content","Content4","Content6","Content8","Content10"]]

# 3. Handle missing values
clean_data = clean_data.fillna("")

# 4. Save as new CSV
clean_data.to_csv("dataset.csv", index=False)

print("✅ Clean dataset saved successfully!")