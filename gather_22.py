from strlearn.streams import StreamGenerator
import numpy as np

# Variables
clfs = ["GNB", "HT", "KNN", "SVM"]
methods = ["NON-KNORAU2", "RUS-KNORAU2", "CNN-KNORAU2", "NON-KNORAE2", "RUS-KNORAE2", "CNN-KNORAE2"]
random_states = [1994, 1410]
distributions = [[0.97, 0.03]]
label_noises = [
    0.01,
    0.03,
    0.05,
]

drifttype = [(5, False), (5, True), (None, False)]

n_chunks = 199
metrics = ["BAC", "geometric_mean_score", "f_score", "precision", "recall", "specificity"]

scores = np.zeros(
    (
        len(clfs),
        len(random_states),
        len(drifttype),
        # len(incremental),
        len(distributions),
        len(label_noises),
        # len(css),
        len(methods),
        n_chunks,
        len(metrics),
    )
)

print(scores.shape)

# Prepare streams
streams = {}
for i, clf in enumerate(clfs):
    for j, random_state in enumerate(random_states):
        for k, kurwa in enumerate(drifttype):
            for l, distribution in enumerate(distributions):
                for m, flip_y in enumerate(label_noises):
                    # for n, spacing in enumerate(css):
                    spacing, drift_type = kurwa
                    stream = StreamGenerator(
                        incremental=drift_type,
                        weights=distribution,
                        random_state=random_state,
                        y_flip=flip_y,
                        concept_sigmoid_spacing=spacing,
                        n_drifts=1,
                        n_chunks=200,
                        chunk_size=250,
                        n_clusters_per_class = 1,
                        n_features = 8,
                        n_informative= 8,
                        n_redundant= 0,
                        n_repeated = 0,
                    )
                    if spacing == None and drift_type == True:
                        pass
                    else:
                        results = np.load(
                            "results/experiment22_%s/%s.npy" % (clf, stream)
                        )
                        scores[i, j, k, l, m] = results
scores_metrics_22 = scores
np.save("scores_metrics_22", scores_metrics_22)
scores = np.mean(scores, axis=1)
np.save("scores_22", scores)
print(scores, scores.shape)
