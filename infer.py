import gensim
import nltk
import pandas as pd
from typing import List
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

df=pd.read_csv('data.csv')
model = Doc2Vec.load("d2v.model")

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
   
    #Simple preprocessing user sentence
    preprocessed_sentence=gensim.utils.simple_preprocess(user_sentence, deacc=True)

    #Lambda function to get only nouns
    is_noun = lambda pos: pos[:2] == 'NN'

    #Applying Lambda function and removing duplicates
    nouns = [word for (word, pos) in nltk.pos_tag(preprocessed_sentence) if is_noun(pos)] 
    nouns = set(nouns)

    #Infering
    v1 = model.infer_vector(list(nouns))
    similar_docs = model.dv.most_similar(positive=[v1])

    #Getting indexes of most similar lines
    indexes=[i[0] for i in similar_docs]

    #returning recommendations

    recommendations=[]
    for i in indexes:
        recommendations.append(df.iloc[[int(i)]])

    return recommendations







