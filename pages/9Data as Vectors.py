import streamlit as st
import numpy as np
from sklearn.decomposition import PCA
import plotly.graph_objects as go

st.title("Data as Vectors: Everything Lives in Vector Space")

st.write("""
In the world of AI and data, everything can be represented as a vector—a list of numbers. 
Whether it's a movie's ratings, the meaning of a word, or the pixels of an image, 
they all exist in a high-dimensional space. Here, we visualize them by projecting into 3D space 
using PCA (Principal Component Analysis) to make it fun and interactive!
""")

# Generate sample data
np.random.seed(42)  # For reproducibility

# Movie ratings: each movie as a vector of ratings from 5 users
movies = np.random.rand(10, 5) * 5  # Ratings 0-5
movie_labels = [f"Movie {i+1}" for i in range(10)]

# Words: simple embeddings (random for demo, in reality like word2vec)
words = np.random.rand(10, 50)  # 50D embedding
word_labels = ["cat", "dog", "run", "jump", "happy", "sad", "king", "queen", "apple", "banana"]

# Images: flattened grayscale images (28x28 for MNIST-like)
images = np.random.rand(10, 28*28)  # Random pixel values
image_labels = [f"Image {i+1}" for i in range(10)]

# Reduce to 3D using PCA separately, then normalize
pca_movies = PCA(n_components=3)
pca_words = PCA(n_components=3)
pca_images = PCA(n_components=3)

reduced_movies = pca_movies.fit_transform(movies)
reduced_words = pca_words.fit_transform(words)
reduced_images = pca_images.fit_transform(images)

# Normalize each to [0, 1] range and combine
def normalize(data):
    return (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0) + 1e-8)

reduced_movies = normalize(reduced_movies)
reduced_words = normalize(reduced_words)
reduced_images = normalize(reduced_images)

reduced_data = np.vstack([reduced_movies, reduced_words, reduced_images])
all_labels = movie_labels + word_labels + image_labels
categories = ["Movie"] * len(movies) + ["Word"] * len(words) + ["Image"] * len(images)

# Create 3D scatter plot
fig = go.Figure()

colors = {"Movie": "red", "Word": "blue", "Image": "green"}
for cat in ["Movie", "Word", "Image"]:
    mask = np.array(categories) == cat
    fig.add_trace(go.Scatter3d(
        x=reduced_data[mask, 0],
        y=reduced_data[mask, 1],
        z=reduced_data[mask, 2],
        mode='markers+text',
        text=[label for label, m in zip(all_labels, mask) if m],
        textposition="top center",
        name=cat,
        marker=dict(size=8, color=colors[cat], opacity=0.8)
    ))

fig.update_layout(
    title="Data Points in 3D Vector Space",
    scene=dict(
        xaxis_title="PC1",
        yaxis_title="PC2",
        zaxis_title="PC3"
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

st.plotly_chart(fig)

st.write("""
**What's happening here?**
- **Movies**: Each point represents a movie, with its vector being the ratings from different users.
- **Words**: Words are embedded in a high-dimensional space capturing their meanings.
- **Images**: Images are flattened into long vectors of pixel intensities.

In reality, these live in much higher dimensions (e.g., 784 for images), but PCA squishes them into 3D for visualization. 
Notice how similar items cluster together in this space!
""")