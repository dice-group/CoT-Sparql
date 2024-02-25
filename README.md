# CoT-Sparql

This repository contains the code for generating SPARQL queries from natural language text using the chain of thought approach.

![architecture](https://github.com/dice-group/CoT-Sparql/blob/main/arch.png)

### Run the System Locally

To run the system locally, follow one of the methods below based on your preferences and settings:

#### Using Conda

If you are using Conda, create the environment with the following commands:

```bash
conda env create -f environment.yml
conda activate sparqlgen
```
#### Without Conda
If you are not using Conda, you can create the environment with this command:

```
pip install -r requirements.txt
```

#### Requirments 

We have provided the sentence embeddings and other relevant information, but users can create their own embeddings using the notebook in the temp folder. To obtain the context examples (embeddings and other information), download the necessary files to the ```temp``` directory using the following command:
```
wget https://files.dice-research.org/datasets/COT-SPARQLGEN/dbpedia_examples.parquet https://files.dice-research.org/datasets/COT-SPARQLGEN/embeddings_dbpedia.pkl https://files.dice-research.org/datasets/COT-SPARQLGEN/embeddings_wikidata.pkl
https://files.dice-research.org/datasets/COT-SPARQLGEN/wikidata_examples.parquet
```
#### Run 
You are now ready to run the system with the following command:
```
python main.py --model_path  --kb  --question 
```
For example:

```
python main.py --model_path TheBloke/CodeLlama-34B-Instruct-GPTQ --kb dbpedia --question 'what is the capital of Germany'
```

You can select the knowledge base using dbpedia or wikidata. Also, you can change the model based on the available system.

### Datasets

We used the following datasets during our experiments:
| Wikidata | Dbpedia |
|-----------------|-----------------|
| QALD-10  | QALD-9  |
| LcQuad2.0  | Vquanda  |

The datasets are available for download in the ```dataset``` folder of our repository.


### Embeddings
We have provided a link to the embeddings and relevant data. However, if you wish to create your own embeddings, the code is available in the `temp` folder, named `embeddings.ipynb`. We utilized `all-MiniLM-L6-v2` for sentence encoding, but users may change it according to their requirements.

### Model Used for Entity Linking and Relation Extraction:
```contexta.py``` provides all the details about the models and tools used for entity linking for DBpedia and Wikidata, respectively. This is also optional, and users may use the tools of their preference.

