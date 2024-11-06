

def read_stop_tokens(file_path: str):
    with open(file_path, "r") as infile:
        for line in infile:
            yield line.strip()

class StopWords:

    collection = set([token for token in read_stop_tokens("resources/stopwords.txt")])
    