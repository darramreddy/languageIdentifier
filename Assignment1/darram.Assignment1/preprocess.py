import os
import re
import sys
from collections import defaultdict

def removeSGML(input_string: str):
    # remove all text between the < > and those characters themselves
    pattern = re.compile(r'<.*?>')
    result_string = re.sub(pattern, '', input_string)
    return result_string

def tokenizeText(input_string):
    # Contractions dictionary
    contractions = {
      "ain't": "am not",
      "aren't": "are not",
      "can't": "cannot",
      "can't've": "cannot have",
      "'cause": "because",
      "could've": "could have",
      "couldn't": "could not",
      "couldn't've": "could not have",
      "didn't": "did not",
      "doesn't": "does not",
      "don't": "do not",
      "hadn't": "had not",
      "hadn't've": "had not have",
      "hasn't": "has not",
      "haven't": "have not",
      "he'd": "he would",
      "he'd've": "he would have",
      "he'll": "he will",
      "he'll've": "he will have",
      "he's": "he is",
      "how'd": "how did",
      "how'd'y": "how do you",
      "how'll": "how will",
      "how's": "how is",
      "I'd": "I would",
      "I'd've": "I would have",
      "I'll": "I will",
      "I'll've": "I will have",
      "I'm": "I am",
      "I've": "I have",
      "isn't": "is not",
      "it'd": "it had",
      "it'd've": "it would have",
      "it'll": "it will",
      "it'll've": "it will have",
      "it's": "it is",
      "let's": "let us",
      "ma'am": "madam",
      "mayn't": "may not",
      "might've": "might have",
      "mightn't": "might not",
      "mightn't've": "might not have",
      "must've": "must have",
      "mustn't": "must not",
      "mustn't've": "must not have",
      "needn't": "need not",
      "needn't've": "need not have",
      "o'clock": "of the clock",
      "oughtn't": "ought not",
      "oughtn't've": "ought not have",
      "shan't": "shall not",
      "sha'n't": "shall not",
      "shan't've": "shall not have",
      "she'd": "she would",
      "she'd've": "she would have",
      "she'll": "she will",
      "she'll've": "she will have",
      "she's": "she is",
      "should've": "should have",
      "shouldn't": "should not",
      "shouldn't've": "should not have",
      "so've": "so have",
      "so's": "so is",
      "that'd": "that would",
      "that'd've": "that would have",
      "that's": "that is",
      "there'd": "there had",
      "there'd've": "there would have",
      "there's": "there is",
      "they'd": "they would",
      "they'd've": "they would have",
      "they'll": "they will",
      "they'll've": "they will have",
      "they're": "they are",
      "they've": "they have",
      "to've": "to have",
      "wasn't": "was not",
      "we'd": "we had",
      "we'd've": "we would have",
      "we'll": "we will",
      "we'll've": "we will have",
      "we're": "we are",
      "we've": "we have",
      "weren't": "were not",
      "what'll": "what will",
      "what'll've": "what will have",
      "what're": "what are",
      "what's": "what is",
      "what've": "what have",
      "when's": "when is",
      "when've": "when have",
      "where'd": "where did",
      "where's": "where is",
      "where've": "where have",
      "who'll": "who will",
      "who'll've": "who will have",
      "who's": "who is",
      "who've": "who have",
      "why's": "why is",
      "why've": "why have",
      "will've": "will have",
      "won't": "will not",
      "won't've": "will not have",
      "would've": "would have",
      "wouldn't": "would not",
      "wouldn't've": "would not have",
      "y'all": "you all",
      "y'alls": "you alls",
      "y'all'd": "you all would",
      "y'all'd've": "you all would have",
      "y'all're": "you all are",
      "y'all've": "you all have",
      "you'd": "you had",
      "you'd've": "you would have",
      "you'll": "you you will",
      "you'll've": "you you will have",
      "you're": "you are",
      "you've": "you have"
    }
    
    current_token = ""
    final_tokens = []
    for i in range(len(input_string)):
        char = input_string[i]
        if char.isspace() or char in ['(', ')']:
            if current_token:
                if "'" in current_token:
                    if current_token in contractions.keys():
                        current_token = contractions[current_token]
                        tokens_to_append = current_token.split()
                        for tok in tokens_to_append:
                            final_tokens.append(tok)
                        current_token = ""
                    else:
                        final_tokens.append(current_token)
                        current_token = ""
                else:
                    final_tokens.append(current_token)
                    current_token = ""
        elif char == '.':
            # Handle abbreviations like U.S.A.
            if current_token and current_token[-1].isalpha() and current_token[-1].isupper():
                current_token += char
            elif current_token and current_token[-1].isdigit():
                if i+1 < len(input_string):
                    if input_string[i+1].isdigit():
                        current_token+=char
                else:
                    final_tokens.append(current_token)
                    current_token = ""
            else:
                if current_token:
                    final_tokens.append(current_token)
                    current_token = ""
        elif char == ',':
            if i+1 < len(input_string):
                if input_string[i+1].isspace():
                    final_tokens.append(current_token)
                    current_token = ""
                else:
                    current_token += char
            elif current_token:
                final_tokens.append(current_token)
                current_token = ""
        else:
            current_token += char
    if current_token:
        final_tokens.append(current_token)
    return final_tokens

def calculate_pair_freqs(tokens, vocab, all_tokens):
    pairs = {}
    most_freq_word = ""
    first_freq = ""
    second_freq = ""
    highest_freq = -1
    for first in vocab:
        for second in vocab:
            curr_pair = first+second
            if curr_pair in all_tokens.keys():
                pairs[curr_pair] = all_tokens[curr_pair]
                if pairs[curr_pair] > highest_freq:
                    highest_freq = pairs[curr_pair]
                    most_freq_word = curr_pair
                    first_freq = first
                    second_freq = second
            else:
                if curr_pair not in pairs.keys():
                    for token in tokens:
                        curr_freq = token.count(curr_pair)
                        if curr_pair in pairs.keys():
                            pairs[curr_pair] += curr_freq
                            if pairs[curr_pair] > highest_freq:
                                highest_freq = pairs[curr_pair]
                                most_freq_word = curr_pair
                                first_freq = first
                                second_freq = second
                        else:
                            pairs[curr_pair] = curr_freq
                            if pairs[curr_pair] > highest_freq:
                                highest_freq = pairs[curr_pair]
                                most_freq_word = curr_pair
                                first_freq = first
                                second_freq = second
    return pairs, most_freq_word, first_freq, second_freq

def BPE(tokens, vocab_size):
    vocab = {}
    all_tokens = {}
    merge_rules = []

    for token in tokens:
        for char in token:
            if char in vocab.keys():
                vocab[char] += 1
            else:
                vocab[char] = 1
            if char in all_tokens.keys():
                vocab[char] += 1
            else:
                vocab[char] = 1
    
    while(len(vocab.keys()) < vocab_size):
        pairs, most_freq_word, first, second = calculate_pair_freqs(tokens, vocab.keys(), all_tokens)

        for pair in pairs.keys():
            if pair not in all_tokens.keys():
                all_tokens[pair] = pairs[pair]
        
        merge_rules.append(most_freq_word)
        vocab[most_freq_word] = pairs[most_freq_word]
        vocab[first] -= pairs[most_freq_word]
        vocab[second] -= pairs[most_freq_word]

    return vocab, merge_rules

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python preprocess.py [data_folder] [vocab_size]")
        sys.exit(1)

    data_folder = sys.argv[1]
    vocab_size = int(sys.argv[2])

    all_tokens = []
    merge_rules = []
    for filename in os.listdir(data_folder):
        filepath = os.path.join(data_folder, filename)
        
        with open(filepath, 'r', encoding='ISO-8859-1') as file:
            content = file.read()

        content = removeSGML(content)
        tokens = tokenizeText(content)

        all_tokens.extend(tokens)

    final_vocab, merge_rules = BPE(all_tokens, vocab_size)

    total_merge_rules = len(merge_rules)
    first_20_merge_rules = merge_rules[:20]

    # Write results to preprocess.output
    with open('preprocess.output', 'w') as output_file:
        output_file.write(f"Tokens {len(final_vocab)} Merge rules {total_merge_rules}\n")
        output_file.write("The first 20 merge rules\n")
        for rule in first_20_merge_rules:
            output_file.write(f"{rule[0]} -> {rule[1]}\n")
        #output_file.write("Top 50 tokens\n")
        #for token, frequency in top_50_tokens:
            #output_file.write(f"{token} [{frequency}]\n")