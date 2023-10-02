import numpy as np
import pandas as pd
import json
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import pickle

class DataClassifier:

    nmf: NMF
    vectorizer: TfidfVectorizer

    def __init__(self):
        pass

    def fit_vectorizer_nmf(self, data: pd.DataFrame, n_clusters: int):

        if "url" not in data.columns or "dict" not in data.columns:
            raise Exception("url not in data.columns or dict not in data.columns!")

        start_df = data.drop_duplicates(subset=["dict"], ignore_index=True)
        start_df = start_df.drop(start_df[(start_df["dict"] == "{}") | (start_df["dict"] == "``")].index).reset_index()

        urls = start_df["url"]
        data = start_df["dict"]
        texts = np.array([])

        for i in range(data.shape[0]):
            #print(f"Processed: {i}/{data.shape[0]}")
            dict_i = json.loads(re.sub('\w\'\w', '', data[i].replace('"\'', '"').replace('\'"', '"')).replace("'", '"'))
            counter_i = Counter(dict_i)
            elements_i = counter_i.elements()
            string_i = " ".join(elements_i)
            texts = np.append(texts, string_i)

        vectorizer = TfidfVectorizer(max_features=10000, stop_words='english')
        self.vectorizer = vectorizer

        X = vectorizer.fit_transform(texts)
        nmf = NMF(n_components=n_clusters, random_state=42)
        nmf.fit(X)
        self.nmf = nmf

    def _check_algorithms(self):
        if not self.nmf:
            raise Exception("NMF is null!")
        if not self.vectorizer:
            raise Exception("Vectorizer is null!")

    def save_vectorizer_nmf(self, vectorizer_path, nmf_path):
        self._check_algorithms()

        pickle.dump(self.vectorizer, open(vectorizer_path, 'wb'))
        pickle.dump(self.nmf, open(nmf_path, 'wb'))

    def load_vectorizer_nmf(self, vectorizer_path, nmf_path):
        loaded_vectorizer = pickle.load(open(vectorizer_path, 'rb'))
        loaded_nmf = pickle.load(open(nmf_path, 'rb'))
        self.vectorizer = loaded_vectorizer
        self.nmf = loaded_nmf


    def get_topics_dict(self):
        self._check_algorithms()

        feature_names = self.vectorizer.get_feature_names_out()
        topics = dict()
        for topic_idx, topic_words in enumerate(self.nmf.components_):
            top_words_idx = topic_words.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            topics[topic_idx] = top_words
        return topics

    def transform_dict_to_text(self, input_dict: dict):
        #dict_i = json.loads(re.sub('\w\'\w', '', input_dict.replace('"\'', '"').replace('\'"', '"')).replace("'", '"'))
        counter_i = Counter(input_dict)
        elements_i = counter_i.elements()
        string_i = " ".join(elements_i)
        return string_i

    def predict(self, text):
        self._check_algorithms()
        vectorized_data = self.vectorizer.transform([text])
        i = np.where(self.nmf.transform(vectorized_data) == np.max(self.nmf.transform(vectorized_data)))
        return i[1][0]


if __name__ == "__main__":
    dc = DataClassifier()
    train_data = pd.read_csv("res_parse.csv", header=0)[["url", "dict"]]
    train_data = train_data.drop(train_data[(train_data["dict"] == "{}") | (train_data["dict"] == "``")].index).reset_index()
    theme_topics_dict = {}
    with open('theme_topic.json', 'r') as fp:
        theme_topics_dict = json.load(fp)
    #dc.fit_vectorizer_nmf(train_data, 62)
    #dc.save_vectorizer_nmf("vectorizer.sav", "nmf.sav")

    dc.load_vectorizer_nmf("vectorizer.sav", "nmf.sav")
    dc1 = json.loads(re.sub('\w\'\w', '', train_data["dict"][100].replace('"\'', '"').replace('\'"', '"')).replace("'", '"'))
    text = dc.transform_dict_to_text(dc1)

    print(theme_topics_dict[str(dc.predict(text))])
    print(text)





