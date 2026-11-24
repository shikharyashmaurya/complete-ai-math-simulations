import streamlit as st
import numpy as np
from sklearn.decomposition import PCA
import plotly.graph_objects as go

st.set_page_config(page_title="Data as Vectors", layout="wide")

st.title("Data as Vectors: Everything Lives in Vector Space")

st.write("""
In the world of AI and data, everything can be represented as a vector—a list of numbers. 
Whether it's a movie's ratings, the meaning of a word, or the pixels of an image, 
they all exist in a high-dimensional space. Here, we visualize them by projecting into 3D space 
using PCA (Principal Component Analysis) to make it fun and interactive!
""")

# Generate sample data. The data is synthetic but *structured* (each item is built from a group "prototype"
# plus a little noise), so that similar items really are close together, just like in real datasets.
@st.cache_data
def build_datasets(seed: int = 42):
    rng = np.random.default_rng(seed)

    # Movie ratings: each movie is a vector of ratings (1-5) from 5 users.
    # Users 1-2 love action, users 3-4 love romance, user 5 likes everything a bit.
    action_taste = np.array([4.6, 4.2, 1.5, 1.8, 3.5])
    romance_taste = np.array([1.4, 1.9, 4.7, 4.4, 3.2])
    movies = np.vstack([
        action_taste + rng.normal(0, 0.4, (5, 5)),
        romance_taste + rng.normal(0, 0.4, (5, 5)),
    ]).clip(1, 5)
    movie_labels = [f"Action movie {i+1}" for i in range(5)] + [f"Romance movie {i+1}" for i in range(5)]
    movie_groups = ["Action"] * 5 + ["Romance"] * 5

    # Words: toy 50-D "embeddings". Words with related meanings share a topic prototype
    # (in reality these come from a model such as word2vec).
    word_topics = {"Animals": ["cat", "dog"], "Actions": ["run", "jump"], "Feelings": ["happy", "sad"],
                   "Royalty": ["king", "queen"], "Fruit": ["apple", "banana"]}
    words, word_labels, word_groups = [], [], []
    for topic, members in word_topics.items():
        prototype = rng.normal(0, 1, 50)
        for word in members:
            words.append(prototype + rng.normal(0, 0.35, 50))
            word_labels.append(word)
            word_groups.append(topic)
    words = np.array(words)

    # Images: 28x28 grayscale images flattened to 784-D vectors. Half show a vertical bar, half a horizontal bar.
    images, image_labels, image_groups = [], [], []
    for i in range(10):
        img = rng.uniform(0, 0.15, (28, 28))
        offset = int(rng.integers(-3, 4))
        if i < 5:
            img[4:24, 12 + offset:16 + offset] = 0.9
            image_groups.append("Vertical bar")
        else:
            img[12 + offset:16 + offset, 4:24] = 0.9
            image_groups.append("Horizontal bar")
        images.append(img.flatten())
        image_labels.append(f"Image {i+1}")
    images = np.array(images)

    return {
        "Movies (5-D rating vectors)": (movies, movie_labels, movie_groups),
        "Words (50-D embeddings)": (words, word_labels, word_groups),
        "Images (784-D pixel vectors)": (images, image_labels, image_groups),
    }


@st.cache_data
def reduce_to_3d(data: np.ndarray):
    pca = PCA(n_components=3)
    reduced = pca.fit_transform(data)
    return reduced, pca.explained_variance_ratio_


datasets = build_datasets()

st.info(
    "Each kind of data lives in its **own** vector space with its own number of dimensions, so each one gets its "
    "own PCA. Comparing a movie point with a word point would be meaningless — their axes measure different things."
)
dataset_name = st.radio("Pick a dataset to explore", list(datasets), horizontal=True, key="p09_dataset")
data, labels, groups = datasets[dataset_name]
reduced, explained = reduce_to_3d(data)

# Create 3D scatter plot, one colour per group
fig = go.Figure()
palette = ["#ef4444", "#3b82f6", "#22c55e", "#f59e0b", "#a855f7"]
for group_index, group in enumerate(dict.fromkeys(groups)):
    mask = np.array(groups) == group
    fig.add_trace(go.Scatter3d(
        x=reduced[mask, 0],
        y=reduced[mask, 1],
        z=reduced[mask, 2],
        mode='markers+text',
        text=[label for label, m in zip(labels, mask) if m],
        textposition="top center",
        name=group,
        marker=dict(size=8, color=palette[group_index % len(palette)], opacity=0.85)
    ))

fig.update_layout(
    title=f"{dataset_name}: squeezed from {data.shape[1]}-D down to 3-D",
    scene=dict(
        xaxis_title="PC1",
        yaxis_title="PC2",
        zaxis_title="PC3"
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    height=600,
)

st.plotly_chart(fig, width="stretch")
st.caption(
    f"These 3 directions keep {explained.sum():.0%} of the variation in the original {data.shape[1]}-D vectors "
    f"(PC1 {explained[0]:.0%}, PC2 {explained[1]:.0%}, PC3 {explained[2]:.0%})."
)

st.write("""
**What's happening here?**
- **Movies**: Each point is a movie; its vector is the ratings it got from 5 different users.
- **Words**: Each point is a word; its vector is a (toy) embedding where related meanings get similar numbers.
- **Images**: Each point is an image; its 28×28 pixels are flattened into one long 784-number vector.

In reality, these live in much higher dimensions (e.g., 784 for images), but PCA squishes them into 3D for visualization. 
Notice how similar items (same colour) cluster together: action movies near action movies, "king" near "queen",
vertical-bar images near other vertical-bar images. That closeness is exactly what AI models exploit.

*The data on this page is synthetic (generated with a fixed seed) so that the patterns are easy to see.*
""")