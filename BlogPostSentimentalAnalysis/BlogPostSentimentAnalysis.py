from pathlib import Path
import torch
import torch.nn as nn

def LoadTokenizedBlogPost(file_path):
    
    tokenized_data = torch.load(file_path)
    return tokenized_data

def GetAllTokenizedBlogPosts():
    path = Path("BlogPostSentimentalAnalysis/BlogPosts/")
    tokenized_files = []
    for file in path.iterdir():
        if file.is_file() and file.suffix == ".pt":
            tokenized_files.append(file)
    return tokenized_files

class BlogPostSentimentModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BlogPostSentimentModel, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.softmax(out)
        return out

def CreateBlogPostSentimentModel(input_size=4096, hidden_size=512, output_size=3):
    model = BlogPostSentimentModel(input_size, hidden_size, output_size)
    return model
