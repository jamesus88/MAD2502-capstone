#Note: install packages pandas, numpy, nltk, sklearn, and re before running!!!

#import and download needed imports
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection, naive_bayes, svm
from sklearn.metrics import accuracy_score
import re

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# Add the Data using pandas
data_location = 'MOVIES.csv'
Movies_Data_Uncleaned = pd.read_csv(data_location,encoding='latin-1')

def replace_html_tags_and_http_links(review_str):
    # Define the regular expression pattern to match the HTML tags and review tags
    pattern = r'<[^>]*>([^<]*)</[^>]*>'
    pattern2 = r'<em>([^<]*)</em>'
    pattern3 = r'FULL SPOILER-FREE REVIEW @ https://fandomwire.com/[^\s]+'

    #replaces pattern 1 with required word from link
    matches = re.findall(pattern, review_str)
    intermediate_str = re.sub(pattern, r'\1', review_str)

    # replaces pattern 2 with required word from link
    matches2 = re.findall(pattern2, intermediate_str)
    intermediate_str2 = re.sub(pattern2, r'\1', intermediate_str)

    #removes pattern 3 entirely
    matches3 = re.findall(pattern3, intermediate_str2)
    output_str = re.sub(pattern3, r'', intermediate_str2)

    return output_str #returns final string cleaned of the 3 patterns

def lemmatize_words(entry):
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV

    Final_words = []
    word_Lemmatized = WordNetLemmatizer()

    # POS tagging and lemmatization
    for word, tag in pos_tag(entry):
        if word not in stopwords.words('english') and word.isalpha():
            word_Final = word_Lemmatized.lemmatize(word, tag_map[tag[0]])
            Final_words.append(word_Final)

    return Final_words

#run this function to clean all the reviews
Movies_Data_Uncleaned['reviews'] = [replace_html_tags_and_http_links(entry) for entry in Movies_Data_Uncleaned['reviews']]

#Data Pre-processing: dropping empty rows, converting to lowercase, and tokenize
Movies_Data_Uncleaned.dropna(inplace=True, subset = ['reviews'])
Movies_Data_Uncleaned['reviews'] = Movies_Data_Uncleaned['reviews'].str.lower()
Movies_Data_Uncleaned['reviews_cleaned_partial'] = Movies_Data_Uncleaned['reviews'].apply(word_tokenize)

#Repeat for keywords: dropping empty rows, converting to lowercase, and tokenize
Movies_Data_Uncleaned.dropna(inplace=True, subset = ['keywords'])
Movies_Data_Uncleaned['keywords'] = Movies_Data_Uncleaned['keywords'].str.lower()
Movies_Data_Uncleaned['keywords_cleaned_partial'] = Movies_Data_Uncleaned['keywords'].apply(word_tokenize)

#apply lemmatize function to partially cleaned data
Movies_Data_Uncleaned['reviews_cleaned'] = Movies_Data_Uncleaned['reviews_cleaned_partial'].apply(lemmatize_words)
Movies_Data_Uncleaned['keywords_cleaned'] = Movies_Data_Uncleaned['keywords_cleaned_partial'].apply(lemmatize_words)

#convert list to string (desired datatype for future operations)
Movies_Data_Uncleaned['reviews_cleaned'] = Movies_Data_Uncleaned['reviews_cleaned'].apply(str)
Movies_Data_Uncleaned['keywords_cleaned'] = Movies_Data_Uncleaned['keywords_cleaned'].apply(str)

#fix indexes
Movie_Data_Cleaned = Movies_Data_Uncleaned.reset_index(drop=True)

#add final column for binary quality predictor
Movie_Data_Cleaned['quality_binary'] = [1 if event >= 6 else 0 for event in Movie_Data_Cleaned['quality_rating']]

#save results
Movie_Data_Cleaned.to_csv('Movies_Data_Full_Clean.csv', index=False)