from numpy import array

from Classifier.SVM import SVM
from Classifier.features import characteristic_vector
from Data.clean_data import clean_text
from Data.dataset import get_randomised_sample
from Ressources.resource import Resource, get_correct_stop_word

# Collect some tweets from the data set
tweets = get_randomised_sample(256)

# Gather the resources for cleaning the text and compute the features vectors
Resources = Resource()

# Create the cleaned list of label and text contained in the collection
clean_list_tweet = [x for x in tweets]
l_label = [float(x[0]) for x in clean_list_tweet]
l_text = [clean_text(x[1], get_correct_stop_word(Resources)) for x in clean_list_tweet]

# Create the dual array of features and labels for training and testing
m_features, m_label = list(), list()
for index, text in enumerate(l_text):
    feature_vector = characteristic_vector(text, Resources)
    if feature_vector != [0, 0, 0, 0, 0]:
        m_features.append(feature_vector)
        m_label.append(l_label[index])
m_f_train, m_f_test = array(m_features[:len(m_features) // 2]), array(m_features[len(m_features) // 2:])
m_l_train, m_l_test = array(m_label[:len(m_label) // 2]), array(m_label[len(m_label) // 2:])

# Create an SVM classifier
Classifier = SVM()

# Compute the parameters of the SVM classifier with the training arrays
Classifier.fit(m_f_train, m_l_train)

# Predict the labels of the testing collection
result = [Classifier.predict(array([x.tolist()])) for x in m_f_test]

# Result of the prediction
correct = 0
for idx, value in enumerate(result):
    if result[idx] == "Positive" and m_l_test[idx] == 1.0 or result[idx] == "Negative" and m_l_test[idx] == 0.0 or \
            result[idx] == "Neutral":
        correct += 1
print("{} out of {} predictions correct : {} %".format(correct, len(result), correct / len(result) * 100))
