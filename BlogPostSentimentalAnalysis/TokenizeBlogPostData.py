from tokenizers import Tokenizer
from transformers import AutoTokenizer
import torch

def tokenize_texts(texts, model_name='bert-base-uncased', max_length=4096):
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    encoded_inputs = tokenizer(
        texts,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors='pt'
    )

    return {
        'input_ids': encoded_inputs['input_ids'],
        'attention_mask': encoded_inputs['attention_mask']
    }