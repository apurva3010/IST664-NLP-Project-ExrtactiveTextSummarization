# Exrtactive Text Summarization:

## Motivation:

The history of writing dates back to 3100 BC in ancient Sumer of Mesopotamia [1] and since then along with the progress of human civilization, texts and written doctrines containing information have exploded many folds. In the age of information technology this means explosions of data. Based on a study by ACI Information Group, 5 exabytes of data was created on a daily basis in 2013 [2]. The International Data Corporation (IDC), estimates world’s digital data size to be 40 Zetabytes by 2020 [3].

![alt text](https://www.signiant.com/wp-content/uploads/2015/04/Screen-Shot-2015-04-28-at-1.55.54-PM.png "Signiant Data Growth")

In today’s age where data is considered one of the most critical assets of a large-scale organization, managing it efficiently becomes increasingly important. We our project we are going to look at a particular segment of efficient data management using Natural Language Processing (NLP) called Text Summarization. The aim is to use machines to consume large volumes of text and come up with a human readable most concise and relevant summary. Besides an information philanthropic philosophy, Text Summarization also has critical significance in present day businesses to understand which we will be worked on reviews from Amazon’s retail website.

## Data Description:

The data we worked on are reviews for products in the Fine Food category sold on Amazon’s retail website. It is adapted from McAuley & Leskovec’s (2013) work on modeling the evolution of user expertise through online reviews done at Stanford University [4]. The data spreads over a period of more than 10 years from **Oct 1999 - Oct 2012** and contains **568,454** reviews on **74,258** products written by over **256,059** Amazon customers. The **10** columns in the dataset are as follows:

```
Id, ProductId, UserId, ProfileName, HelpfulnessNumerator, HelpfulnessDenominator, Score, Time, Summary, Text
```

Data Download: [here](https://www.kaggle.com/snap/amazon-fine-food-reviews)

## Extractive Summarization using TextRank:

### Preprocessing:
For preprocessing the reviews, besides special character removal and mainstream data cleansing, we have also replaced English contraction words, e.g. “you’ve” = “you have”, “he’s” = “he is”, etc.  This has been specifically thought through based on the nature of the data we processed. Generally, in writing a review, a customer is most interested in conveying their experience and not too much concerned with their style of writing or grammatical correctness. The source of contractions is taken from: [here](http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python)

Tokenization at different granularities and stopwords removal is done using NLTK. We summarize reviews both with removal and without removal of stopwords and try to also answer to what extent an extractive summary depends on common stop words which when added make more logical sense from a language interpretation perspective.

### Summarization:
TextRank is a graph-based algorithm for text processing where segments of texts are ranked based on unsupervised methods of sentence extraction [5]. The graph is constructed by assigning each sentence of the text to a *vertex (V)* and then connected to every other vertex with *edges (E)* whose weights are comparative measures of similarities of the sentences by making adaptive usage of Google’s PageRank algorithm used in the anatomy of a large-scale hypertextual Web search engine (Brin & Page 1998) [6]. Analytically, for a directed graph *G(V,E)* if *In(Vi)* and *Out(Vi)* are the set of vertices that are its predecessors and successors respectively, the score of vertex *S(Vi)* is given by

![alt text](https://raw.githubusercontent.com/apurva3010/IST664-NLP-Project-ExrtactiveTextSummarization/master/PageRankScores.png "Page Rank Scores Formula")

TextRank then ranks the text segments by these scores and given a particular threshold or limit of cardinality of segments, it returns the prioritized segments as the summary. For our project we will be using the implementation of this TextRank summarization bundled as a part of **RaRe Technologies** robust open-source vector space modeling and topic modeling toolkit implemented in Python called **Gensim**. Internal dependencies of genism include **NumPy**, **SciPy** and **Cython** for performance.

### Measurement:
After extracting the summaries using Gensim TextRank summarization, we measure the effectiveness using BLEU (bilingual evaluation understudy) algorithm for evaluating the quality of the machine summarized text proposed by Papineni et al (2002) [7]. The BLEU score ranges from 0 to 1 with 0 for a complete mismatch and 1 for a complete match. BLEU comes in built with NLTK. These are N-gram scores computed by matching grams of a specific order, such as single words (1-gram) or word pairs (2-gram or bigram). We will generate both Cumulative 1-gram and 4-gram scores where the grams are weighted as (1,0,0,0) and (0.25, 0.25, 0.25, 0.25).

### Results:

![alt text](https://raw.githubusercontent.com/apurva3010/IST664-NLP-Project-ExrtactiveTextSummarization/master/BLEU-1.png "BLEU-1 Score Distribution")
![alt text](https://raw.githubusercontent.com/apurva3010/IST664-NLP-Project-ExrtactiveTextSummarization/master/BLEU-4.png "BLEU-4 Score Distribution")

![alt text](https://raw.githubusercontent.com/apurva3010/IST664-NLP-Project-ExrtactiveTextSummarization/master/BLEU_Score_Table_Results.png "BLEU Scores Table")

### Observations:
* The distributions obtained above shows that this heuristic unsupervised algorithm does a good job of pulling out key words or phrases but for more control on summarization we should us the abstractive approach give the low mean scores for both BLEU-1 and BLEU-4.
* The BLEU-4 scores are relatively higher compared to BLEU-1 show that TextRank does a better job when looking at the presence of group of 4 words as compared to specific location-based positioning of single words indicating more towards its efficiency in extracting key words/phrase but not particularly ordering them internally.
* An interesting thing we noticed is that the scores were higher when we did not remove stopwords which is counter intuitive to the fact that as a part of text pre-processing we cleanse the text by removing these words. This is because golden data summaries while being archived manually are done in a way that it makes sense from a linguistic perspective and while doing so lots of stopwords get involved in a golden summary.

## References:
1. Brian M. Fagan, Charlotte Beck, ed. (1996). The Oxford Companion to Archaeology. Oxford University Press. p. 762. ISBN 978-0-19-507618-9.
2. [ACI Data Explosion Article](http://aci.info/2014/07/12/the-data-explosion-in-2014-minute-by-minute-infographic/)
3. [Signiant Data Growth Article](https://www.signiant.com/articles/file-transfer/the-historical-growth-of-data-why-we-need-a-faster-transfer-solution-for-large-data-sets/)
4. McAuley, J. J., & Leskovec, J. (2013, May). From amateurs to connoisseurs: modeling the evolution of user expertise through online reviews. In Proceedings of the 22nd international conference on World Wide Web (pp. 897-908). ACM.
5. Mihalcea, R., & Tarau, P. (2004). Textrank: Bringing order into text. In Proceedings of the 2004 conference on empirical methods in natural language processing.
6. Brin, S., & Page, L. (1998). The anatomy of a large-scale hypertextual web search engine. Computer networks and ISDN systems, 30(1-7), 107-117.
7. Papineni, K., Roukos, S., Ward, T., & Zhu, W. J. (2002, July). BLEU: a method for automatic evaluation of machine translation. In Proceedings of the 40th annual meeting on association for computational linguistics (pp. 311-318). Association for Computational Linguistics.




