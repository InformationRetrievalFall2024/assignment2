import sys


alphabet = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"}
numerical = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

class Tokenizer:

    def yield_line_from_file(self, text_file_path: str) -> str:
        """
        Time complexity is O(n) as I have a single loop going through n lines of a file
        """
        try:
            with open(text_file_path) as infile:
                for line in infile:
                    yield line.lower()
        except FileNotFoundError:
            print(f"File {text_file_path} was not found in path location.")
            yield ""
        except UnicodeDecodeError:
            print(f"File {text_file_path} failed to decode in UTF8 format.")
            yield ""
        except Exception as e:
            print(f"Triggered unexpected error of type {type(e).__name__}")
            yield ""
        

    def get_token(self, line: str) -> str:
        """
        Time complexity is O(n) as I have a single loop going through n lines of a file
        """
        word = ""
        for c in line:
            if c in alphabet or c in numerical:
                word += c
            else:
                if len(word):
                    print(word)
                    yield word
                    word = ""
        if len(word):
            print(word)
            yield word
  

    def tokenize(self, text_file_path: str) -> str:
        """
        Time complexity is O(n2) since I have a nested for loop for n characters for n lines
        """
        for line in self.yield_line_from_file(text_file_path):
            for token in self.get_token(line):
                yield token

    def compute_word_frequencies(self, tokens: list[str]) -> dict[str: int]:
        """
        Time complexity is O(n) since I am looping through n tokens to create a dictionary
        """
        token_counter: dict[str: int] = {}
        for token in tokens:
            if token in token_counter:
                token_counter[token] = token_counter[token] + 1
            else:
                token_counter[token] = 1
        return token_counter

    def print_frequencies(self, mappedFrequencies: dict[str: int]) -> None:
        """
        Using the sorted python function, the time complexity is O(n+ log n) nested within a loop making this operation O(n2)
        Step 1: Sort the dictionary items in desc order then add them to a dictionary 
        Step 2: Iterate through the items, print the words out
        """
        output_to_file = False 
        output_file_path = "results.txt"
        mappedFrequencies = {k: v for k, v in sorted(mappedFrequencies.items(), key=lambda item: item[1], reverse=True)}  # code from https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/

        for k, v in mappedFrequencies.items():
            print(f"{k:<50}\t{v}")

        if output_to_file:
            with open(output_file_path, 'w') as outfile:
                for k, v in mappedFrequencies.items():
                    outfile.write(f"{k:<50}\t{v}\n")


def main():
    """ The most computational function is tokenize which is O(n2) making this call O(n2) """
    if len(sys.argv) != 2:
        print("Error: User forgot to enter a file in the command line.")
        sys.exit(1)

    infile = sys.argv[1]
    
    s = Tokenizer()

    s.print_frequencies(s.compute_word_frequencies(s.tokenize(infile)))


if __name__ == "__main__":
    main()
