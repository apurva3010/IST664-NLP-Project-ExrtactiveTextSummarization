# This code looks at the data available at https://www.kaggle.com/snap/amazon-fine-food-reviews
# It cleans the data and treats the Summaries provided in the data as the golden data set
# for reference and accuracy measurements. With and without stop words the sentences are summarized
# and then the bleu scores are compared.
# This is done to see the impact of stopwords on special character words in extractive summaries.

# author: appatil
import nltk
import random
import pandas as pd
from nltk.corpus import *
from nltk.translate.bleu_score import sentence_bleu
from gensim.summarization import summarize

# path of the raw data from kaggle
reviews_path = 'Reviews-tst.csv'

# path for english language contractions
# you've -> you have
# he's -> he is
# Source: http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
contractions_path = 'english-contractions.csv'

# Path for the output
output_path = 'output-tst.txt'

# Path for the output metrics
metrics_path = 'metrics-tst.csv'

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

# cleans a text by looping over sentences and calling the cleansing methods above
# then it returns 2 sentences - 1)cleaned with stopwords & 2) other cleaned without stopwords
def clean_review_text(text, contractions, stopwords):

    # Convert words to lower case
    text = text.lower()
    sentences = nltk.sent_tokenize(text)
    new_sentences_with_stopwords = []
    new_sentences_without_stopwords = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)

        # Replace contractions with longer forms
        words = remove_contractions(words, contractions)

        # Remove special characters
        words_with_stopwords = [remove_special_characters(word) for word in words]
        words_without_stopwords = remove_stopwords(words_with_stopwords, stopwords)

        new_sentences_with_stopwords.append(" ".join([word for word in words_with_stopwords if word.isalpha()]) + ".")
        new_sentences_without_stopwords.append(" ".join([word for word in words_without_stopwords if word.isalpha()]) + ".")

    return (" ".join([s for s in new_sentences_with_stopwords if s != "."]),
        " ".join([s for s in new_sentences_without_stopwords if s != "."]))

# removes stopwords from sentence
def remove_stopwords(words, stopwords):
    return [word for word in words if word not in stopwords]

# read the raw reviews
raw_reviews = pd.read_csv(reviews_path)

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

# this is just for printing progress
progress_count = []
for i in range(0, 1000, 1):
    progress_count.append(int(i/1000 * len(raw_reviews)))

# Files to write
output = open(output_path, 'w')
metrics = open(metrics_path, 'w')

# Metrics format:
# bleu1: Cumulative BLEU-1 Score with Stopwords
# bleu4: Cumulative BLEU-4 Score with Stopwords
# bleu1ws: Cumulative BLEU-1 Score without Stopwords
# blue4ws: Cumulative BLEU-4 Score without Stopwords
metrics.write('bleu1,bleu4,bleu1ws,bleu4ws\n')

print("Extracting Summaries ... ", end="", flush=True)
for i, row in raw_reviews.iterrows():
    gold_summary = row['Summary']
    review = row['Text']

    (text_with_stopwords, text_without_stopwords) = clean_review_text(review, contractions, stopwords)

    # gensim doesn't work for single sentence paragraphs so continue
    if text_with_stopwords.count(".") <= 1 or text_without_stopwords.count(".") <= 1:
        continue

    try:
        gensim_summary_with_stopwords = summarize(text_with_stopwords, word_count=10)
    except ValueError:
        continue

    gensim_summary_with_stopwords = gensim_summary_with_stopwords.replace('\n', ' ')

    # continue for empty extractions
    if gensim_summary_with_stopwords.strip(' ') == "":
        continue

    try:
        gensim_summary_without_stopwords = summarize(text_without_stopwords, word_count=10)
    except ValueError:
        continue

    gensim_summary_without_stopwords = gensim_summary_without_stopwords.replace('\n', ' ')

    # continue for empty extractions
    if gensim_summary_without_stopwords.strip(' ') == "":
        continue

    # calculate cumulative bleu scores
    bleu_1_with_stopwords = sentence_bleu(gold_summary, gensim_summary_with_stopwords, weights=(1, 0, 0, 0))
    bleu_4_with_stopwords = sentence_bleu(gold_summary, gensim_summary_with_stopwords, weights=(0.25, 0.25, 0.25, 0.25))
    bleu_1_without_stopwords = sentence_bleu(gold_summary, gensim_summary_without_stopwords, weights=(1, 0, 0, 0))
    bleu_4_without_stopwords = sentence_bleu(gold_summary, gensim_summary_without_stopwords, weights=(0.25, 0.25, 0.25, 0.25))

    metrics.write('{},{},{},{}\n'.format(
        bleu_1_with_stopwords,
        bleu_4_with_stopwords,
        bleu_1_without_stopwords,
        bleu_4_without_stopwords
    ))

    output.write("Review: {}\n".format(review))
    output.write("Gold Summary: {}\n".format(gold_summary))
    output.write("Gensim Summary with Stopwords: {}\n".format(gensim_summary_with_stopwords))
    output.write("Cumulative BLEU-1 Score with Stopwords: {}\n".format(bleu_1_with_stopwords))
    output.write("Cumulative BLEU-4 Score with Stopwords: {}\n".format(bleu_4_with_stopwords))
    output.write("Gensim Summary without Stopwords: {}\n".format(gensim_summary_without_stopwords))
    output.write("Cumulative BLEU-1 Score without Stopwords: {}\n".format(bleu_1_without_stopwords))
    output.write("Cumulative BLEU-4 Score without Stopwords: {}\n--\n".format(bleu_4_without_stopwords))

    # Prints the progress count
    if i in progress_count:
        print ("%.1f%%.. " % (i/len(raw_reviews)*100), end="", flush=True)
print("100%")
