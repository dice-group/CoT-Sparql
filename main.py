import argparse
import os
from accelerate import Accelerator
from transformers import AutoTokenizer, pipeline, logging
from auto_gptq import AutoGPTQForCausalLM, BaseQuantizeConfig
import time
import warnings
import contexta as ca
import contextb as cb
import validation as val
# Filter out all warnings
warnings.filterwarnings("ignore")


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", type=str, default="")
    parser.add_argument("--kb", type=str, default="")
    parser.add_argument("--question", type=str, default="")
    parser.add_argument("--top_k", type=int, default=10)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--max_length", type=int, default=700)
    parser.add_argument("--repetition_penalty", type=float, default=1.1)
    parser.add_argument("--num_return_sequences", type=int, default=1)

    return parser.parse_args()


def prompt_building(kb, question):
    """This function return a final prompt that will include everyting and LLM ready"""
    
    instruction = """[INST]
        Task: convert question to SPARQL query for """+kb+""" knowledge graph.\n
        Description: given an input question and a list of """+kb+""" URIs for the mentioned entities in the question and relations 
        mentioned in the question. Write a correct SPARQL code to query these """+kb+""" URIs in """ +kb+ """ Knowledge graph. 
        Please wrap your SPARQL code answer using ``` :\n
        You can formulate your SPARQL query as the following examples. \n
        <examples>
           """+str(cb.example_generation(kb, question))+"""
      </examples>

     [/INST]
"""
   # print(instruction)
    prompt = instruction+'\n [question]:'+ question+'\n [entities] :'+ str(ca.entity_linking(kb, question)) +'\n[relations]:' +str(ca.relation_extraction(kb, question))
    
    return prompt






    
def generate_sparql(prompt, pipe):
    
    """This function takes the formated prompt and and the Pipe and retururn the response of the LLM"""

    response = pipe(prompt)[0]['generated_text']
    #print(prompt)
    return response.split('[/INST]')[1]



def main(args):
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, use_fast=True)
    model_basename = "model"
    use_triton = False
    model = AutoGPTQForCausalLM.from_quantized(args.model_path,
        model_basename=model_basename,
        use_safetensors=True,
        trust_remote_code=True,
        device="cuda:0",
        skip_special_tokens= True, 
        use_triton=use_triton,
        quantize_config=None)
    
    logging.set_verbosity(logging.CRITICAL)
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        use_cache=True,
        device_map="auto",    
        do_sample=True,
        top_k=args.top_k,
        temperature=args.temperature,
        max_length=args.max_length,
        repetition_penalty=args.repetition_penalty,  
        num_return_sequences=args.num_return_sequences,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,)
    
    prompt = prompt_building(args.kb,args.question)
    #print('here')
    is_valid, output = val.validate_sparql(generate_sparql(prompt,pipe),args.kb)
    if is_valid:
        print(output)
    else:
        print("The generated sparql is not valid do you want to try again")

if __name__ == "__main__":
    args = get_args()
    assert args.model_path != "", "Please provide the llama model path"
    assert args.kb != "", "Please provde the targeted Knowledge base"
    assert args.question != "" "Please provide a natural language (en) question"
    print("ok")
    
    main(args)