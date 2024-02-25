import spacy
import spacy_component
import requests
import spacy_dbpedia_spotlight





def entity_linking(kb,question):
    
    """This function takes NL question and KB and returns the linked entites list"""
    nlp = spacy.load('en_core_web_lg')
    entities = []
    if kb == "dbpedia":
        nlp.add_pipe('dbpedia_spotlight')
        doc = nlp(question)
        entities = [(ent.text, ent.kb_id_) for ent in doc.ents]
    else:
        
        nlp.add_pipe('entityfishing')
        doc = nlp(question)
        entities = [ent.text+': wd:'+ str(ent._.kb_qid) for ent in doc.ents]
    
    return entities

def relation_extraction(kb, question):
    
    """This function takes NL question and KB and returns the relations found in the question"""
   
    rel_list = []
    if kb == "dbpedia":
        return format_output(query_falcon_api(question)['relations'])

    else:
        nlp = spacy.load('en_core_web_lg')
        nlp.add_pipe("rebel", after="senter", config={'device':0, 'model_name':'Babelscape/rebel-large'})
        doc = nlp(question)
        for value, rel_dict in doc._.rel.items():
            relation =  str(execute_sparql_query(rel_dict['relation']))
            rel_list.append(relation)
        return rel_list
        
        

def execute_sparql_query(label):
    """This function takes label generated from REBEL and return its wikidata identfier"""
    #label = f'"{label}"'
    endpoint_url = "https://query.wikidata.org/sparql"
    sparql_query = """
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?item ?itemLabel 
            WHERE 
            {
              ?item rdfs:label """+label+"""@en.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }limit 1
            """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    params = {
        'query': sparql_query,
        'format': 'json'
    }

    response = requests.get(endpoint_url, headers=headers, params=params)
    data = response.json()
    results = data['results']['bindings']
    item = ""
    for result in results:
        item = result['propertyLabel']['value']
    
    return item


def query_falcon_api(text):
    """This function takes NL question and return Dbpedia relations using falcon API"""
    api_url = "https://labs.tib.eu/falcon/api?mode=long"
    payload = {
        "text": text
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def format_output(data):
    """This function takes data and return formatd output"""
    output = {}
    for item in data:
        surface_form = item.get('surface form')
        uri = item.get('URI')
        output[surface_form] = uri
    return output