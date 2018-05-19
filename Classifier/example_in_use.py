from numpy import (array)

from Classifier.SVM import SVM
from Classifier.features import characteristic_vector
from Data.clean_data import *
from Data.dataset import *

tweets = get_randomised_sample(256)

clean_list_tweet = [clean_line(x) for x in tweets]
l_label = [float(x[0]) for x in clean_list_tweet]
l_text = [clean_text(x[1]) for x in clean_list_tweet]

m_features, m_label = list(), list()
for indice, text in enumerate(l_text):
    feature_vector = characteristic_vector(text)
    if feature_vector != [0, 0, 0, 0, 0]:
        m_features.append(feature_vector)
        m_label.append(l_label[indice])
m_f_train, m_f_test = array(m_features[:len(m_features) // 2]), array(m_features[len(m_features) // 2:])
m_l_train, m_l_test = array(m_label[:len(m_label) // 2]), array(m_label[len(m_label) // 2:])

Classifier = SVM()
Classifier.fit(m_f_train, m_l_train)
y_predict = Classifier.predict(m_f_test)
correct = sum(y_predict == m_l_test)
print("{} out of {} predictions correct : {} %".format(correct, len(y_predict), correct / len(y_predict) * 100))
