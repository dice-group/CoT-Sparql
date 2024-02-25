# CoT-Sparql
This repository contains the code for generating SPARQL from natural language text using the chain of thought approach.
![architecture](https://github.com/yourusername/yourrepository/blob/main/path/to/your/image.png)

### Run the system locally
If you want to run the system locally the follow one of the following method based on your prefrernces and settings:

#### Using Conda
If you are using conda then create the environment using the following command

```
conda env create -f environment.yml
conda activate sparqlgen
```

#### Without Conda
If you are using not using conda then create the environment using the following command:

```
pip install -r requirements.txt
```
#### Requirments 
We have provided the sentences embeddings and other relevant information but user can create their own embeddings and using the notebook given in ```temp``` folder.
To get the context example(embeddings and other information) you need to download the necessary files to ```temp``` directory using the following command:
```
wget https://files.dice-research.org/datasets/COT-SPARQLGEN/dbpedia_examples.parquet https://files.dice-research.org/datasets/COT-SPARQLGEN/embeddings_dbpedia.pkl https://files.dice-research.org/datasets/COT-SPARQLGEN/embeddings_wikidata.pkl
https://files.dice-research.org/datasets/COT-SPARQLGEN/wikidata_examples.parquet
```
#### Run 
Now you are ready to run the system using the following command: 
```
python main.py --model_path  --kb  --question 
```
For example:
```
python main.py --model_path TheBloke/CodeLlama-34B-Instruct-GPTQ --kb dbpedia --question 'what is the capital of Germany'
```

you can select the knolwedge base using ```dbpedia``` or ```wikidata``` also you can change the model based on available system.

### Datasets
We used the following dataset during our experimnets:
| Wikidata | Dbpedia |
|-----------------|-----------------|
| QALD-10  | QALD-9  |
| LcQuad2.0  | Vquanda  |

The dataset are availbe for downlaod in the ```datasets``` folder on our repository.




