import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
dataset = pd.read_csv(r"C:\Users\DELL\Desktop\Study\Aoudjit\dataset\kaggle_Interests_group.csv")

# Preprocessing
# Selecting interest-related columns
interest_columns = [col for col in dataset.columns if "interest" in col]
interests_data = dataset[interest_columns]

# Impute missing values with 0
imputer = SimpleImputer(strategy="constant", fill_value=0)
interests_data_cleaned = imputer.fit_transform(interests_data)

# Standardize the data
scaler = StandardScaler()
interests_data_scaled = scaler.fit_transform(interests_data_cleaned)

# Determine the optimal number of clusters using the elbow method
inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(interests_data_scaled)
    inertia.append(kmeans.inertia_)

# Plot the elbow method
plt.figure(figsize=(8, 5))
plt.plot(range(1, 11), inertia, marker='o', linestyle='--')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia')
plt.grid(alpha=0.5)
plt.show()

# Apply K-Means clustering with the optimal number of clusters (e.g., k=3)
optimal_k = 3  # Adjust based on the elbow method result
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(interests_data_scaled)

# Add cluster labels to the original dataset
dataset["Cluster"] = clusters

# Dimensionality Reduction for Visualization
pca = PCA(n_components=2)
pca_data = pca.fit_transform(interests_data_scaled)

# Visualize the clusters
plt.figure(figsize=(10, 6))
sns.scatterplot(
    x=pca_data[:, 0], 
    y=pca_data[:, 1], 
    hue=clusters, 
    palette='tab10', 
    alpha=0.7, 
    edgecolor='k'
)
plt.title("K-Means Clustering with PCA (2D Projection)")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title="Cluster")
plt.grid(alpha=0.3)
plt.show()

# Analyze Cluster Centers
cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
centroids_df = pd.DataFrame(cluster_centers, columns=interest_columns)
print("Cluster Centers:")
print(centroids_df)

# Save the dataset with clusters to a new CSV file
dataset.to_csv("clustered_dataset.csv", index=False)
print("Clustered dataset saved as 'clustered_dataset.csv'.")
