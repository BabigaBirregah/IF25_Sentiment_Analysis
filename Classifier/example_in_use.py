import numpy as np

from Classifier.Kernel import Kernel
from Classifier.SVM import SVMTrainer
from Classifier.features import characteristic_vector
from Data.clean_data import *
from Data.dataset import *

# 1) collect some tweet from our data set
pos_tweets, neg_tweets = get_randomised_pos_neg_sample()

# 2) clean the text and gather the important element from it
clean_list_tweet = [clean_text(x) for x in pos_tweets]

# 3) create the matrix of the features vectors of the tweets
features_pos = np.matrix([characteristic_vector(x) for x in clean_list_tweet])

# 4) create the associated label of the tweets
labels_pos = np.matrix([[1.]] * len(features_pos))

# 5) initiate a trainer with the desired parameter
trainer = SVMTrainer(Kernel.linear(), 0.1)

# 6) train the SVM classifier
predictor = trainer.train(features_pos, labels_pos)

# 7) use SVM with the obtained parameters to predict new elements or measure known data
for x in features_pos:
    print(predictor.predict(x))
