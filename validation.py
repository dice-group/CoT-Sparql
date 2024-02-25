import requests

def validate_sparql(response, kb):
    
    """This function takes the generated response and the KB and returns that the sparql query is validated or not"""
    
    is_valid = True
    output = formate_output(response)
    
    if kb == "dbpedia" and output != 'no sparql':
        is_valid, message = check_sparql_query_validity(output, 'dbpedia')
        
    if kb == "wikidata" and output != 'no sparql':
        is_valid, message = check_sparql_query_validity(output, 'wikidata')
    
    return is_valid, output

def formate_output(response):
    if '```' in response:
        return response.split('```')[1]
    if '[sparql]:' in response:
        return response.split('[sparql]:')[1]
    else:
        return 'no sparql'




def check_sparql_query_validity(query, endpoint='wikidata'):
    """
    Checks if a SPARQL query is syntactically valid against the Wikidata or DBPedia endpoint.

    Parameters:
    - query: The SPARQL query as a string.
    - endpoint: 'wikidata' for the Wikidata endpoint, 'dbpedia' for the DBPedia endpoint.

    Returns:
    - A tuple (is_valid, message) where is_valid is True if the query is valid, False otherwise,
      and message contains information about the validity or the error encountered.
    """

    # Endpoint URLs
    endpoints = {
        'wikidata': 'https://query.wikidata.org/sparql',
        'dbpedia': 'https://dbpedia.org/sparql'
    }

    # Select the appropriate endpoint URL
    url = endpoints.get(endpoint.lower())
    if not url:
        return False, "Invalid endpoint selection. Choose 'wikidata' or 'dbpedia'."

    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; your-application-name)',
        'Accept': 'application/sparql-results+json'
    }

    try:
        # Attempt to execute the query
        response = requests.get(url, params={'query': query}, headers=headers)
        
        # Check if the query was successful
        if response.status_code == 200:
            return True, "The SPARQL query is syntactically valid."
        else:
            return False, f"Syntax error or other issue: {response.text}"
    except Exception as e:
        return False, f"An error occurred: {str(e)}"


