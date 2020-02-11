import sys, os 
from math import log2
import gzip

def get_info(discover_file):
    data = discover_file.read()
    total_symbols = len(data)
    alphabet = set(list(data))
    print(alphabet)
    print(f"Total number of symbols in text: {total_symbols}")
    
    entropy = 0
    for symbol in alphabet: 
        frequency = data.count(symbol)
        prob = frequency / total_symbols
        entropy += prob * log2(1/prob)
        if (symbol != '\n'):
            print(f"Probability for {symbol}: {prob}")
        else:
            print(f"Probability for \\n: {prob}")
    print(f"Entropy: {entropy}")
    quantity_info = entropy * total_symbols / 8
    print(f"Size of file: {os.stat(sys.argv[1]).st_size} bytes")
    print(f"Quantity of information: {quantity_info} bytes")


if __name__ == "__main__":
    try:
        if (sys.argv[1].endswith(".gz")):
            with gzip.open(sys.argv[1]) as discover_file:
                get_info(discover_file)
        else:
            with open(sys.argv[1]) as discover_file:
                get_info(discover_file)
    except IOError:
        print("File not found")



