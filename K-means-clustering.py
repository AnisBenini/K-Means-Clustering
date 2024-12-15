import pandas as pd

# Load the uploaded dataset to examine its structure and content    
file_path = '/mnt/data/kaggle_Interests_group.csv'
dataset = pd.read_csv(file_path)

# Display the first few rows and basic info to understand the structure
dataset.head(), dataset.info()





from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Select interest columns for clustering
interest_columns = [col for col in dataset.columns if "interest" in col]
interests_data = dataset[interest_columns]

# Handle missing values by imputing with 0 (assuming no interest where NaN)
imputer = SimpleImputer(strategy="constant", fill_value=0)
interests_data_cleaned = imputer.fit_transform(interests_data)

# Standardize the data for K-means clustering
scaler = StandardScaler()
interests_data_scaled = scaler.fit_transform(interests_data_cleaned)

# Apply K-means clustering
kmeans = KMeans(n_clusters=5, random_state=42)  # Using 5 clusters as an example
clusters = kmeans.fit_predict(interests_data_scaled)

# Add cluster labels to the original dataset
dataset['Cluster'] = clusters

# Display a sample of the dataset with clusters
dataset[['group', 'grand_tot_interests', 'Cluster']].head()
