# This code looks at the data available at https://www.kaggle.com/snap/amazon-fine-food-reviews
# It cleans the data and treats the Summaries provided in the data as the golden data set
# for reference and accuracy measurements. We create 2 types of golden data:
#
# golden-with-removal.txt - Golden summary in lowercase after removal of stopwords
# golden-without-removal.txt - Golden summary in lowercase without removal of stopwords
#
# Similary the clean data is also written with and without stopwords removal as
# This is done to see the impact of stopwords on special character words in extractive summaries.


# author: appatil
import nltk
from nltk.corpus import *
import pandas as pd

# path of the raw data from kaggle
raw_reviews_path = '../../data/raw/Reviews-tst.csv'

# path for english language contractions
# you've -> you have
# he's -> he is
# Source: http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
contractions_path = '../../data/clean/english-contractions.csv'

# Path for the golden summary
golden_with_removal_path = '../../data/golden/golden-with-removal-tst.txt'
golden_without_removal_path = '../../data/golden/golden-without-removal-tst.txt'

# Path for the cleansed reviews
clean_reviews_with_removal_path = '../../data/clean/clean-reviews-with-removal-tst.txt'
clean_reviews_without_removal_path = '../../data/clean/clean-reviews-without-removal-tst.txt'

# method to remove english language contractions
def remove_contractions(words, contractions):
    new_words = []
    for word in words:
        if word in contractions:
            new_words.append(contractions[word])
        else:
            new_words.append(word)

    return new_words

# removes the special characters from word
def remove_special_characters(word):
    word = re.sub(r'https?:\/\/.*[\r\n]*', '', word, flags=re.MULTILINE)
    word = re.sub(r'\<a href', '', word)
    word = re.sub(r'&amp;', '', word)
    word = re.sub(r'[_"\-;%()|+&=*%.,!?:#$@\[\]/`~,]', '', word)
    word = re.sub(r'<br />', '', word)
    word = re.sub(r'\'', '', word)
    return word

# cleans a text
def clean_text(text, contractions, stopwords):

    # Convert words to lower case
    text = text.lower()
    sentences = nltk.sent_tokenize(text)
    new_sentences_without_removal = []
    new_sentences_with_removal = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)

        # Replace contractions with longer forms
        words = remove_contractions(words, contractions)

        # Remove special characters
        words_without_removal = [remove_special_characters(word) for word in words]
        words_with_removal = remove_stopwords(words_without_removal, stopwords)

        new_sentences_without_removal.append(" ".join([word for word in words_without_removal if word.isalpha()]) + ".")
        new_sentences_with_removal.append(" ".join([word for word in words_with_removal if word.isalpha()]) + ".")

    return (" ".join([s for s in new_sentences_without_removal if s != "."]), " ".join([s for s in new_sentences_with_removal if s != "."]))

# removes stopwords from sentence
def remove_stopwords(words, stopwords):
    return [word for word in words if word not in stopwords]

# read the raw reviews
raw_reviews = pd.read_csv(raw_reviews_path)

# Remove null values and unneeded features
raw_reviews = raw_reviews.dropna()
raw_reviews = raw_reviews.drop(['Id','ProductId','UserId','ProfileName','HelpfulnessNumerator','HelpfulnessDenominator',
                        'Score','Time'], 1)
raw_reviews = raw_reviews.reset_index(drop=True)

# read the contractions
contractions_data = pd.read_csv(contractions_path)
contractions = dict(zip(list(contractions_data.contraction), list(contractions_data.phrase)))

# NLTK stopwords
stopwords = nltk.corpus.stopwords.words('english')
golden_with_removal = open(golden_with_removal_path, 'w')
golden_without_removal = open(golden_without_removal_path, 'w')
clean_reviews_with_removal = open(clean_reviews_with_removal_path, 'w')
clean_reviews_without_removal = open(clean_reviews_without_removal_path, 'w')

# this is just for printing progress
progress_count = []
for i in range(0, 100, 7):
    progress_count.append(int(i/100 * len(raw_reviews)))

print("Cleaning Summaries ... ", end="", flush=True)
for i, summary in enumerate(raw_reviews.Summary):
    (summary_without_removal, summary_with_removal) = clean_text(summary, contractions, stopwords)
    golden_without_removal.write("{}\n".format(summary_without_removal))
    golden_with_removal.write("{}\n".format(summary_with_removal))

    # Prints the progress count
    if i in progress_count:
        print ("{}%..".format(int(i/len(raw_reviews)*100)), end="", flush=True)
print("100%")

print("Cleaning Reviews ... ", end="", flush=True)
for i, text in enumerate(raw_reviews.Text):

    (text_without_removal, text_with_removal) = clean_text(text, contractions, stopwords)
    clean_reviews_without_removal.write("{}\n".format(text_without_removal))
    clean_reviews_with_removal.write("{}\n".format(text_with_removal))

    # Prints the progress count
    if i in progress_count:
        print ("{}%..".format(int(i/len(raw_reviews)*100)), end="", flush=True)
print("100%")