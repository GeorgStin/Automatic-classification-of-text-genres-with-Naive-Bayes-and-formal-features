##############################################
# 1. Read the file
# This function reads the text-file and replaces all "bad" characters
# Input:   Filename (str), Language (str)
# Output:  Corrected String

def get_text(text, language):

    # Read the text file and remove whitespaces from both left and right
    str = open(text, 'r', encoding='utf8').read().strip()

    # Replace various quotes with one standard
    str = str.replace("»", "\"").replace("«", "\"").replace("„", "\"").replace("“", "\"").replace("\n", " ")

    # Replace some "bad" (for tokenizing) characters
    # German
    if language == 'DE':
        str = str.replace("z. B.", "z.B.")\
            .replace("Abb.", "Abb#")\
            .replace("ggf.", "ggf#")\
            .replace("bspw.", "bspw#")\
            .replace("v.a.", "v#a#")\
            .replace("ca.", "ca#")\
            .replace("et al.", "et al#")\
            .replace("Tab.", "Tab#")\
            .replace("bzgl.", "bzgl#")\
            .replace("z.T.", "z#T#")\
            .replace("Mr.", "Mr#")\
            .replace("Mrs.", "Mrs#")
    # Russian
    elif language == 'RU':
        str = str.replace("et al.", "et al#")

    return str

##############################################
# 2. Sentence-Tokenizer
# This function tokenizes sentences from a text-string
# Input:  Text (str), Language (str)
# Output: Sentences (list)

def tokenize_sentences(text, language):

    # Create tokenizer from NLTK (Punkt)
    # German
    if language == 'DE':
        sent_detector = nltk.load('tokenizers/punkt/german.pickle')
    # Russian
    elif language == 'RU':
        sent_detector = nltk.load('tokenizers/punkt/russian.pickle')

    # Create a list with tokenized sentences
    text_sent = sent_detector.tokenize(text)

    # Fix incorrect tokenized sentences with '"' at the beginning
    sentences = []
    for x in text_sent:
        if x[0:2] == "\",":
            sentences[-1] = sentences[-1] + x
        else:
            sentences.append(x)

    return sentences

##############################################
# 3. Tokens
# This function separates sentences into single tokens
# Input:  Sentences (list)
# Output: All tokens (list)

def tokenize_tokens(sentences):

    # Initialize empty list for tokens
    tokens = []

    # for-loop for separating
    for s in sentences:
        # 'l' is all tokens in one sentence
        l = word_tokenize(s)
        # append tokens to the list
        tokens.extend(l)
        # append empty token at the end of a sentence
        tokens.append("")

    return tokens

##############################################
# 4. "Only words" filter
# This function filters tokens. Only words (word characters) remain
# Input:  All tokens (list)
# Output: Only words (list)

def tokenize_words(tokens):

    # Initialize empty list
    words = []

    # for-loop for searching words
    for token in tokens:
        if re.fullmatch(r'\w+', token):
            words.append(token)

    return words

##############################################
# 5. "Only LONG words" filter
# This function searches and collects long words (>6 letters)
# Input:  Only words (list)
# Output: Long words (list)

def tokenize_long_words(words):

    # Initialize empty list
    long_words = []

    # for-loop for searching long words
    for word in words:
        if len(word) > 6:
            long_words.append(word)

    return long_words

##############################################
# 6. Types dictionary
# This function searches, collects and counts all types (unique words) in the text
# Input:  Words (list)
# Output: Types (dict) {type: count}

def get_types(words):

    # Initialize list and make all words lowercased
    words = [word.lower() for word in words]

    # Сount any word sequence (in a dict)
    types = nltk.Counter(words)

    return types

##############################################
# 9. Hapax legomena
# This function searches and collects hapax legomena (unique words)
# Input:  Types (dict), Language (str)
# Output: Hapax (dict)

def get_hapaxe(types, language):

    # Initialize empty dict
    hapaxe = {}

    # Define what is a "word"
    # German
    if language == 'DE':
        word = r'[a-zäöüA-ZÄÖÜ]+'
    # Russian
    elif language == 'RU':
        word = r'[а-яёА-ЯЁ]+'

    # for-loop that searches all tokens with freq "1" and checks if token is a word
    for type in types:
        if types[type] == 1 and re.fullmatch(word, type):
            hapaxe[type] = 1

    return hapaxe

##############################################
# 10. Personal pronouns
# This function searches and counts all personal pronouns
# Input:  Types (dict), Language (str)
# Output: Amount of personal pronouns (int)

def get_personal(types, language):

    # the list with german personal pronouns
    if language == 'DE':
        personal = ['ich', 'wir', 'du', 'ihr', 'er', 'sie', 'es']

    # the list with russian personal pronouns
    elif language == 'RU':
        personal = ['я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они']

    # Initialize a counter for pronouns
    personal_count = 0

    # for-loop for searching and counting personal pronouns
    for key in types:
        if key in personal:
            personal_count += types[key]

    return personal_count


##############################################
# --. Write trained features
# This function saves trained data in the txt-file
# (and creates the file, if it is necessary)
# Input:  Features (list), txt-file (str)
# Output: None

def save_features(data, parameters):

    with open(parameters, "a", encoding='utf8') as file:
        file.write(str(data) + '\n')

    return None

##############################################
# Funktion, die alle weiteren Funktionen aufruft

def run_script(text):

    # 1. The file as a string
    str_text = get_text(text, language)

    # 2. List with tokenized sentences
    sentences = tokenize_sentences(str_text, language)

    # 3. List with all tokens
    tokens = tokenize_tokens(sentences)

    # 4. List with word-tokens (only word characters [a-zA-Z0-9_])
    words_only = tokenize_words(tokens)

    # 5. Long words (>6) in the text
    long_words_only = tokenize_long_words(words_only)

    # 6. Dictionary of types
    types = get_types(words_only)

    # 7. Amount of sentences in the text
    sentences_count = tokens.count("")

    # 8. Amount of commas in the text
    commas_count = tokens.count(",")

    # 9. List of hapax legomena
    hapaxe = get_hapaxe(types, language)

    # 10. List of personal pronouns
    personal_count = get_personal(types, language)


    ########## FEATURES ##########

    # 1. Average word length
    avg_word_length = len(''.join(words_only)) / len(words_only)

    # 2. Average long words amount
    avg_long_word_count = len(long_words_only) / len(words_only)

    # 3. Average amount of words per sentence
    avg_word_count = len(words_only) / sentences_count

    # 4. Average amount of commas per sentence
    avg_commas_count = commas_count / sentences_count

    # 5. Type/Token ratio
    type_token_ratio = len(types) / len (words_only)

    # 6. Relative part of hapax legomena
    hapax_ratio = len(hapaxe) / len(types)

    # 7. Relative part of personal pronouns
    avg_personal = personal_count / sum(types.values())

    # Collect all features together
    data = [
        str(text),
        genre,
        avg_word_length,
        avg_long_word_count,
        avg_word_count,
        avg_commas_count,
        type_token_ratio,
        hapax_ratio,
        avg_personal
    ]

    # Save features (for train-mode)
    if mode == 'train':
        save_features(data, parameters)

    return data

###########################################################
###################  CLASSIFIER  ##########################
###########################################################

def run_classify(text, parameters):

    ##############################################
    # 1. Read the dataset
    # This function reads the dataset with trained parameters
    # Input:   txt-file (str)
    # Output:  Dataset (list with lists)
    def get_data(parameters):

        with open(parameters, 'r', encoding='utf-8') as file:
                data = [ast.literal_eval(line.strip()) for line in file]

        return data

    ##############################################
    # 2. Split the dataset
    # This function splits the dataset by classes and their values
    # Input:   Dataset (list)
    # Output:  Dataset (dict)
    def separate_by_class(data):

        # Initialize empty dict for classes and values-sets
        separated = {}

        # for-loop for separating and collecting
        for i in range(len(data)):

            # every item has information and features of one text
            item = data[i]

            # collect all STATISTIC features
            features = item[2:]

            # define a genre
            class_name = item[1]

            # create new dict-category for a new genre
            if (class_name not in separated):
                separated[class_name] = list()

            # collect all features by genre
            separated[class_name].append(features)

        return separated

    ##############################################
    # 3. Split the dataset
    # This function calculates and collects mean, standard derivation and count for each feature
    # Input:   Dataset (list)
    # Output:  Dataset for features (list)
    def get_dataset(data):

        # Initialize empty list for (mean, standard derivation, count)
        data_features = []

        # for-loop that unpacks dataset and calculates mean, stdev and count
        for feature in zip(*data):

            # Calculate the mean
            mean = sum(feature) / float(len(feature))

            # Calculate the standard derivation
            stdev = (sum([(x - (sum(feature) / float(len(feature)))) ** 2 for x in feature]) / float(len(feature) - 1)) ** 0.5

            # Collect all as a tuple and add to the list
            data_features.append((mean, stdev, len(feature)))

        return data_features

    ##############################################
    # 4. Split the dataset by class
    # This function splits the dataset of features by class and calculates statistics for each item (text)
    # Input:   Dataset (list)
    # Output:  Statistics for features by class (dict)
    def get_stat_by_class(data_separated):

        # Initialize empty dict
        class_stat = {}

        # for-loop that calculates statistics for each item (text)
        for class_value, item in data_separated.items():
            class_stat[class_value] = get_dataset(item)

        return class_stat

    ##############################################
    # 5. Getting features of target text
    # This function calculates and saves the features of target text
    # Input:   Filename (str)
    # Output:  Features (list)
    def get_text_features(text):

        # Run script to getting text features
        data_test = run_script(text)

        # Delete first two features (filename and genre)
        del data_test[0:2]

        return data_test

    ##############################################
    # 6. Calculate the probabilities of predicting
    # This function calculates the Gaussian probability distribution function
    # and then calculates probabilities (for each class)
    # Input:   Dataset (list)
    # Output:  Probabilities (dict)
    def get_class_probabilities(class_stat, features):

        # Total sum of training items
        total_items = sum([class_stat[label][0][2] for label in class_stat])

        # Initialize empty dict for probabilities
        probabilities = {}

        # for-loop for calculating of probabilities
        for class_value, class_summaries in class_stat.items():

            # calculate probability for each class (50:50 here)
            probabilities[class_value] = class_stat[class_value][0][2] / float(total_items)

            # for-loop for calculating the Gaussian probability distribution function
            # and final probabilities
            for i in range(len(class_summaries)):

                # The mean value
                mean = class_summaries[i][0]
                # Standard derivation value
                stdev = class_summaries[i][1]
                # Calculate exponent
                exponent = exp(-((features[i] - mean) ** 2 / (2 * stdev ** 2)))
                # Calculate probability distribution
                distribution = (1 / (((2 * 3.141592653589793) ** 0.5) * stdev)) * exponent

                # Calculate probability
                probabilities[class_value] *= distribution

        return probabilities


    # 1. Dataset (list)
    data = get_data(parameters)

    # 2. Separated dataset (dict)
    data_separated = separate_by_class(data)

    # 4. Split the dataset by class
    class_stat = get_stat_by_class(data_separated)

    # 5. Getting features of target text
    classified_text = get_text_features(text)

    # 6. Calculate the probabilities of predicting
    probabilities = get_class_probabilities(class_stat, classified_text)

    # 7. Calculate the maximum probability
    result = max(probabilities, key=probabilities.get)

    # print(probabilities)
    print(str(text),'is', result)

    # 8. Save the result
    save_clas = [str(text), result]
    save_features(save_clas, 'result.txt')

    return result

###########################################################
# Main program
###########################################################

if __name__ == "__main__":

    import nltk
    import re
    import sys
    import os
    import ast
    from nltk.tokenize import word_tokenize
    from math import exp

    # python script.py mode dataset text language genre
    #
    # python script.py classify dataset_de.txt Science/01.txt DE None
    # python script.py train my_dataset.txt Science DE science

    # SELECT MODE: 'train' or 'classify'
    mode = sys.argv[1].lower()
    if mode != 'classify' and mode != 'train':
        raise ValueError("mode can be only classify or train")

    # WRITE FILENAME FOR TRAINED FEATURES (DATASET)
    # note: if the file does not exist, it will be created automatically
    parameters = sys.argv[2]
    if not parameters.endswith('.txt'):
        raise ValueError("dataset can be only .txt file")

    # SELECT A TARGET TEXT/S FOR TRAINING OR CLASSIFYING
    # (s. the list below)
    # note: you can select whole FOLDER with texts (e.g. just "Science")
    text = sys.argv[3]

    # SELECT LANGUAGE: 'DE' or 'RU'
    language = sys.argv[4].upper()
    if language != 'DE' and language != 'RU':
        raise ValueError("language can be only DE or RU")

    # SELECT GENRE OF TEXT/S for train mode
    # e.g. "science" or "fiction" (or just something if the mode is "classify")
    genre = sys.argv[5]

    """
    SCIENCE DE:         FICTION DE:                 SCIENCE RU:         FICTION RU:
    Science/01.txt      Fiction/01_Martin.txt       Science_ru/01.txt   Fiction_ru/01.txt
    Science/02.txt      Fiction/02_Carroll.txt      Science_ru/02.txt   Fiction_ru/02.txt
    Science/03.txt      Fiction/03_Doyle.txt        Science_ru/03.txt   Fiction_ru/03.txt
    Science/04.txt      Fiction/04_Meyer.txt        Science_ru/04.txt   Fiction_ru/04.txt
    Science/05.txt      Fiction/05_Christie.txt     Science_ru/05.txt   Fiction_ru/05.txt
    Science/06.txt      Fiction/06_Lewis.txt        Science_ru/06.txt   Fiction_ru/06.txt
    Science/07.txt      Fiction/07_Dumas.txt        Science_ru/07.txt   Fiction_ru/07.txt
    Science/08.txt      Fiction/08_Kafka.txt        Science_ru/08.txt   Fiction_ru/08.txt
    Science/09.txt      Fiction/09_Hesse.txt        Science_ru/09.txt   Fiction_ru/09.txt
    Science/10.txt      Fiction/10_Mann.txt         Science_ru/10.txt   Fiction_ru/10.txt
    Science/11.txt      Fiction/11_Dickens.txt      Science_ru/11.txt   Fiction_ru/11.txt
    Science/12.txt      Fiction/12_Remarque.txt     Science_ru/12.txt   Fiction_ru/12.txt
    Science/13.txt      Fiction/13_Rowling.txt      Science_ru/13.txt   Fiction_ru/13.txt
    Science/14.txt      Fiction/14_Twain.txt        Science_ru/14.txt   Fiction_ru/14.txt
    Science/15.txt      Fiction/15_Dostojewski.txt  Science_ru/15.txt   Fiction_ru/15.txt
    Science/16.txt      Fiction/16_Wilde.txt        Science_ru/16.txt   Fiction_ru/16.txt
    """

    # Functions, that call all another functions
    # for training-mode
    if mode == "train":
        # function for one text
        if text.endswith('.txt'):
            run_script(text)

        # function for whole folder
        else:
            for root, directories, files in os.walk(text):
                for file_name in files:
                    text_location = root + '/' + file_name
                    if text_location.endswith('.txt'):
                        run_script(text_location)

    # for classifying-mode
    elif mode == "classify":
        # function for one text
        if text.endswith('.txt'):
            run_classify(text, parameters)

        # function for whole folder
        else:
            for root, directories, files in os.walk(text):
                for file_name in files:
                    text_location = root + '/' + file_name
                    if text_location.endswith('.txt'):
                        run_classify(text_location, parameters)
