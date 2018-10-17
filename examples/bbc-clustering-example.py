from sklearn.decomposition import IncrementalPCA
import matplotlib.pyplot as plt
from sklearn import cluster, datasets
from sklearn.datasets import fetch_20newsgroups
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from bokeh.layouts import row, column
from bokeh.plotting import figure, show, output_file
import csv
import numpy as np

#newsgroups_train = fetch_20newsgroups(subset='train',
#                                      categories=['alt.atheism', 'sci.space'])

documents = []
with open("../resources/datasets/bbc-text.csv") as file:
    reader = csv.reader(file, delimiter=",")
    for r in reader:
        documents.append(r[1])

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
])
X = pipeline.fit_transform(documents[0:500]).todense()


pca = IncrementalPCA(n_components=2).fit(X)
data2D = pca.transform(X)
PLOT_SIZE = 400
#plt.scatter(data2D[:,0], data2D[:,1])
#plt.show()

colors = np.array([x for x in ('#00f', '#0f0', '#f00', '#0ff', '#f0f', '#ff0')])
colors = np.hstack([colors] * 20)

dbscan = cluster.DBSCAN(eps=.2)
birch = cluster.Birch(n_clusters=5)
means = cluster.MiniBatchKMeans(n_clusters=5)
spectral = cluster.SpectralClustering(n_clusters=5, eigen_solver='arpack', affinity="nearest_neighbors")
affinity = cluster.AffinityPropagation(damping=.9, preference=-200)

algorithms = [dbscan, birch, means, affinity]
data2D = StandardScaler().fit_transform(data2D)

plots =[]
for algorithm in algorithms:

    # predict cluster memberships
    algorithm.fit(data2D)
    if hasattr(algorithm, 'labels_'):
        y_pred = algorithm.labels_.astype(np.int)
    else:
        y_pred = algorithm.predict(data2D)

    p = figure(output_backend="webgl", title=algorithm.__class__.__name__,
               plot_width=PLOT_SIZE, plot_height=PLOT_SIZE)

    p.scatter(data2D[:, 0], data2D[:, 1], color=colors[y_pred].tolist(), alpha=0.5, )

    plots.append(p)

layout = column(row(plots[:2]), row(plots[2:]))
output_file("clustering.html", title="clustering with sklearn")
show(layout)