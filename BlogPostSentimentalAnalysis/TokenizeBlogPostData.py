from tokenizers import Tokenizer
from transformers import AutoTokenizer
from pathlib import Path
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

def create_tokenized_blog_posts():
    path = Path("BlogPostSentimentalAnalysis/BlogPosts/")

    for file in path.iterdir():
        if file.is_file() and file.suffix == ".txt":
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
            tokenized_data = tokenize_texts([content])
            torch.save(tokenized_data, file.with_suffix(".pt"))

create_tokenized_blog_posts()