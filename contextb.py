from sentence_transformers import SentenceTransformer, util
import os
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import contexta as ca

model = SentenceTransformer('all-MiniLM-L6-v2')


# Load embeddings from the file



def  example_generation(kb, question):
    """This function takes NL question and KB and returns the most semantically relvant example"""
    example = ""
    if kb == "dbpedia":
        with open('temp/embeddings_dbpedia.pkl', 'rb') as f:
            embeddings = pickle.load(f)
        df = pd.read_parquet('temp/dbpedia_examples.parquet')
        ques, query, entities, relations = find_similar_query(question,embeddings,df)
        example = f"[question]: {ques} \n[Entities]: {str(entities)}\n[Relations]:{str(relations)} \n[SPARQL]: {query}"
    else:
        with open('temp/embeddings_wikidata.pkl', 'rb') as f:
            embeddings = pickle.load(f)
        df = pd.read_parquet('temp/wikidata_examples.parquet')
        ques, query, entities, relations= find_similar_query(question, embeddings, df)
        example = f"[question]: {ques} \n[Entities]: {str(entities)}\n[Relations]:{str(relations)} \n[SPARQL]: {query}"
        
    return example



def find_similar_query(query, embeddings, df):
    
    """This function takes NL question pre-existing embeddings and the existing dataframe and return the most similar question with its 
        entites, relation and sparql"""
    
    query_embedding = model.encode([query])[0]
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    closest_index = np.argmax(similarities)
    similar_sentence = df.iloc[closest_index]['question']
    sparql_query = df.iloc[closest_index]['query']
    entities = df.iloc[closest_index]['entities']
    relations = df.iloc[closest_index]['relations']   
    return similar_sentence, sparql_query,entities,relations

#print(find_similar_sentence('Who is the prime minister of Pakistan?',embeddings,df))