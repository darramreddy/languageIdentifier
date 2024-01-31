import math
import os
import re
import sys

def trainBigramLanguageModel(input_string):
    input_string = '~' + input_string.replace('\n', '\n~')
    input_string = input_string.replace('\n', ' ')
    input_string = re.sub(r'[^a-zA-Z0-9\s\'~]', '', input_string)

    unigram_freq = {}
    bigram_freq = {}

    for char in input_string:
        unigram_freq[char] = unigram_freq.get(char, 0) + 1
        

    words = input_string.split()
    for word in words:
        for i in range(len(word) - 1):
            bigram = word[i:i+2]
            bigram_freq[bigram] = bigram_freq.get(bigram, 0) + 1

    return unigram_freq, bigram_freq

def identifyLanguage(test_string, language_names, unigram_freqs, bigram_freqs):
    best_language = None
    best_log_likelihood = float('-inf')
    test_string = '~' + test_string.replace('\n', '\n~')
    test_string = test_string.replace('\n', ' ')
    test_string = re.sub(r'[^a-zA-Z0-9\s\'~]', '', test_string)

    test_bigrams = [test_string[i:i+2] for i in range(len(test_string) - 1)]

    def calculate_prob(bigram, bigram_freq, unigram_freq, vocabulary_size):
        numerator = bigram_freq.get(bigram, 0) + 1
        denominator = unigram_freq.get(bigram[0], 0) + vocabulary_size
        probability = math.log(numerator / denominator)
        return probability
    
    for i, language in enumerate(language_names):
        unigram_freq = unigram_freqs[i]
        bigram_freq = bigram_freqs[i]
        vocabulary_size = len(unigram_freq)

        log_likelihood = sum(calculate_prob(bigram, bigram_freq, unigram_freq, vocabulary_size)
                            for bigram in test_bigrams)

        if log_likelihood > best_log_likelihood:
            best_log_likelihood = log_likelihood
            best_language = language

    return best_language

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python languageIdentification.py [path to training data folder] [test file]")
        sys.exit(1)

    training_folder = sys.argv[1]
    test_file_path = sys.argv[2]
    output_file_path = "languageIdentification.output"

    language_names = []
    unigram_freqs = []
    bigram_freqs = []

    for root, dirs, files in os.walk(training_folder):
        for language_file in files:
            language_name = os.path.splitext(language_file)[0]
            language_names.append(language_name)

            file_path = os.path.join(root, language_file)
            with open(file_path, 'r', encoding='ISO-8859-1') as file:
                training_text = file.read()

            unigram_freq, bigram_freq = trainBigramLanguageModel(training_text)
            unigram_freqs.append(unigram_freq)
            bigram_freqs.append(bigram_freq)

    with open(test_file_path, 'r', encoding='ISO-8859-1') as test_file:
        lines = test_file.readlines()

    with open(output_file_path, 'w', encoding='ISO-8859-1') as output_file:
        for i, line in enumerate(lines, start=1):
            line = line.strip()
            language = identifyLanguage(line, language_names, unigram_freqs, bigram_freqs)
            output_file.write(f"{i} {language}\n")
