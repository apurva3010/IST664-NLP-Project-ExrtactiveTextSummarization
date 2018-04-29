# This code looks at the data available at https://www.kaggle.com/snap/amazon-fine-food-reviews
# It cleans the data and treats the Summaries provided in the data as the golden data set
# for reference and accuracy measurements.
# We create extractive summaries using pyteaser.

# author: appatil
import re
from pyteaser import Summarize

# Path for the cleansed reviews
clean_reviews_with_removal_path = '../../data/clean/clean-reviews-with-removal-tst.txt'
clean_reviews_without_removal_path = '../../data/clean/clean-reviews-without-removal-tst.txt'

# Path for the pyteaser summaries
pyteaser_summary_with_removal_path = '../../data/summary/pyteaser-summary-with-removal-tst.txt'
pyteaser_summary_without_removal_path = '../../data/summary/pyteaser-summary-without-removal-tst.txt'

# Read the data
pyteaser_summary_with_removal = open(pyteaser_summary_with_removal_path, 'w')
pyteaser_summary_without_removal = open(pyteaser_summary_without_removal_path, 'w')
clean_reviews_with_removal = open(clean_reviews_with_removal_path, 'r')
clean_reviews_without_removal = open(clean_reviews_without_removal_path, 'r')
texts_with_removal = clean_reviews_with_removal.readlines()
texts_without_removal = clean_reviews_without_removal.readlines()

# this is just for printing progress
progress_count = []
for i in range(0, 100, 7):
    progress_count.append(int(i/100 * len(texts_with_removal)))

print("Summarizing with removal using pyteaser ... ", end="", flush=True)
for i, text in enumerate(texts_with_removal):
    summary = text
    if(text.count(".") > 1):
        summary = Summarize('',text)
    summary = summary.replace('\n', ' ')
    pyteaser_summary_with_removal.write("{}\n".format(summary))
    # Prints the progress count
    if i in progress_count:
        print ("{}%..".format(int(i/len(texts_with_removal)*100)), end="", flush=True)
print("100%")

print("Summarizing without removal using pyteaser ... ", end="", flush=True)
for i, text in enumerate(texts_without_removal):
    summary = text
    if(text.count(".") > 1):
        summary = Summarize('',text)
    summary = summary.replace('\n', ' ')
    pyteaser_summary_without_removal.write("{}\n".format(summary))
    # Prints the progress count
    if i in progress_count:
        print ("{}%..".format(int(i/len(texts_with_removal)*100)), end="", flush=True)
print("100%")