from pathlib import Path

def LoadTokenizedBlogPost(file_path):
    import torch
    tokenized_data = torch.load(file_path)
    return tokenized_data

def GetAllTokenizedBlogPosts():
    path = Path("BlogPostSentimentalAnalysis/BlogPosts/")
    tokenized_files = []
    for file in path.iterdir():
        if file.is_file() and file.suffix == ".pt":
            tokenized_files.append(file)
    return tokenized_files