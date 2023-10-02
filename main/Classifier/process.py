from . import DataPreprocessor as dp
from . import DataClassifier as dc
import json
import os

def topic_determinant(list_of_words, exit_code):
    if exit_code != 0:
        return [exit_code, '']
    # text preprocessing
    path = os.getcwd() + '/main/Classifier/'
    preprocessed_dict = dp.Preprocessor.preprocess(raw_text_list=list_of_words, rus_dictionary_path="russian.txt.gz")

    # upload model
    data_classifier = dc.DataClassifier()
    data_classifier.load_vectorizer_nmf(f"{path}vectorizer.sav", f"{path}nmf.sav")

    ready_text = data_classifier.transform_dict_to_text(preprocessed_dict)

    theme_number = data_classifier.predict(ready_text)

    theme_topics_dict = {}
    with open(f'{path}theme_topic.json', 'r') as fp:
        theme_topics_dict = json.load(fp)
        
    theme_cotegory_dict = {}
    with open(f'{path}theme_category.json', 'r') as fc:
        theme_cotegory_dict = json.load(fc)

    return [exit_code, theme_topics_dict[str(theme_number)], theme_cotegory_dict[str(theme_number)]]
    #print(ready_text)


