import os
import re
import random
import requests
import matplotlib.pyplot as plt
from collections import Counter


DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def get_text(url, filename):
    filepath = os.path.join(DATA_DIR, filename)
    
    if os.path.exists(filepath):
        print(f"Loading {filename} from local cache...")
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
            
    print(f"Downloading linguistic weapons, just kidding - downloading... {filename}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        text = response.text
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return text
    except Exception as e:
        print(f"Failed to download {filename}. Error: {e}")
        return ""

def clean_and_slice(text, word_limit=30000, is_voynich=False):
    text = text.lower()
    
    if is_voynich:
        # Strip out bracketed annotator comments like {plant} or {A}
        text = re.sub(r'\{.*?\}', '', text)
        
    words = re.findall(r'[a-z]+', text)
    
    if len(words) < word_limit:
        print(f"WARNING: Text only has {len(words)} words. Needed {word_limit}.")
        return words
        
    return words[:word_limit]



def generate_gibberish(word_limit=30000, vocab_size=1000):
    print(f"Generating algorithmic gibberish (choosing from {vocab_size} unique words).......")
    
    # Allow up to 1,500 unique combinations
    prefixes = ['al', 'qo', 'ch', 'sh', 'd', 'o', 'ko', 'to', 'te', 'so']
    roots = ['ar', 'or', 'ol', 'am', 'yk', 'ee', 'in', 'as', 'et', 'el', 'on', 'um', 'il', 'op', 'at']
    suffixes = ['dy', 'ey', 'y', 'in', 'ai', 'op', 'as', 'es', 'is', 'us']
    
    vocab_set = set()
    # Keep generating until we hit exactly the target vocab size with 0 duplicates
    while len(vocab_set) < vocab_size:
        word = random.choice(prefixes) + random.choice(roots) + random.choice(suffixes)
        vocab_set.add(word)
        
    vocab = list(vocab_set)
    gibberish_text = random.choices(vocab, k=word_limit)

    return gibberish_text




def calculate_zipf(words):
    word_counts = Counter(words)
    sorted_counts = sorted(word_counts.values(), reverse=True)
    ranks = range(1, len(sorted_counts) + 1)
    return ranks, sorted_counts

def plot_zipf():
    # I am planning to add more langs, but for now, these are the ones I have available. I will also add more gibberish datasets in the future..
    sources = {
        "English (Moby Dick)": {
            "url": "https://www.gutenberg.org/cache/epub/2701/pg2701.txt",
            "file": "english.txt"
        },
        "French (Les Misérables)": {
            "url": "https://www.gutenberg.org/cache/epub/17489/pg17489.txt", 
            "file": "french.txt"
        },
        "Spanish (Don Quijote)": {
            "url": "https://www.gutenberg.org/cache/epub/2000/pg2000.txt",
            "file": "spanish.txt"
        },
        "Italian (Divina Commedia)": {
            "url": "https://www.gutenberg.org/cache/epub/1012/pg1012.txt",
            "file": "italian.txt"
        },
        "German (Critique of Pure Reason)": {
            "url": "https://www.gutenberg.org/cache/epub/6342/pg6342.txt",
            "file": "german.txt"
        },
        "Latin (Aeneidos)": {
            "url": "https://www.gutenberg.org/cache/epub/227/pg227.txt", 
            "file": "latin.txt"
        },
        # I had to try different mirrors for the Voynich dataset because the original one was not working. The backup mirror is from a different GitHub repo....
        "Voynich (EVA)": {
            "url": "https://raw.githubusercontent.com/DethRaid/voynich-translation/master/corpus.txt",
            "file": "voynich_eva.txt"
        }
    }
    
    plt.figure(figsize=(12, 8))
    
    # Process Natural Lang and Voynich
    for lang, info in sources.items():
        raw_text = get_text(info["url"], info["file"])
        
        # Backup Voynich mirror...
        if lang == "Voynich (EVA)" and not raw_text:
            print("Trying backup Voynich dataset...")
            backup_url = "https://raw.githubusercontent.com/musyoku/voynich-transcription/master/voynich.txt"
            raw_text = get_text(backup_url, "voynich_eva_backup.txt")

        if lang == "Voynich (EVA)":
            words = clean_and_slice(raw_text, word_limit=30000, is_voynich=True)
            print(f"Success: {lang} words extracted: {len(words)}")
            ranks, freqs = calculate_zipf(words)

            plt.plot(ranks, freqs, marker='o', markersize=2, linestyle='-', color='red', linewidth=2.5, label=lang)

        else:
            words = clean_and_slice(raw_text[10000:], word_limit=30000)
            print(f"Success: {lang} words extracted: {len(words)}")
            ranks, freqs = calculate_zipf(words)
            plt.plot(ranks, freqs, marker='o', markersize=1, linestyle='-', alpha=0.5, label=lang)

    # Process the rando gibberish
    gibberish_words = generate_gibberish(word_limit=30000, vocab_size=1000)
    g_ranks, g_freqs = calculate_zipf(gibberish_words)
    plt.plot(g_ranks, g_freqs, marker='x', markersize=3, linestyle='--', color='black', linewidth=2, label="Algorithmic Gibberish")
    
    plt.xscale('log')
    plt.yscale('log')
    plt.title("Zipf's Law - Word Freq vs Rank", fontsize=15, fontweight='bold')
    plt.xlabel("Rank of Word (Log Scale)", fontsize=12)
    plt.ylabel("Freq of Word (Log Scale)", fontsize=12)
    plt.legend(loc="lower left", fontsize=10)
    plt.grid(True, which="both", ls="--", alpha=0.3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_zipf()