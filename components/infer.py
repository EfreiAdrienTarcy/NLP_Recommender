import gensim
import nltk
import pandas as pd
from typing import List
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

df = pd.read_csv('data/dataset_nlp.csv')
model = Doc2Vec.load("models/d2v.model")

def inference(user_sentence:str)-> List:
    """Gets user sentence en returns most similar lines according to ingredients list

    Parameters
    ----------
    user_sentence : str
        The sentence entered by user
 
    Returns
    -------
    list
        a list of pandas dataframe most similar rows
    """
   
    preprocessed_sentence = gensim.utils.simple_preprocess(user_sentence, deacc=True)           #Simple preprocessing user sentence
    is_noun = lambda pos: pos[:2] == 'NN'                                                       #Lambda function to get only nouns

    nouns = [word for (word, pos) in nltk.pos_tag(preprocessed_sentence) if is_noun(pos)]       #Applying Lambda function and removing duplicates
    nouns = set(nouns)

    v1 = model.infer_vector(list(nouns))                                                        #Infering
    similar_docs = model.dv.most_similar(positive=[v1])

    indexes=[i[0] for i in similar_docs]                                                        #Getting indexes of most similar lines

    # Returning recommendations
    recommendations=[]
    for i in indexes:
        recommendations.append(df.iloc[[int(i)]])

    return recommendations







