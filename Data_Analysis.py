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

def Run_SVM_Test(predictor, predicted):
    #convert data to proper format to run model
    Train_X, Test_X, Train_Y, Test_Y = model_selection.train_test_split(Movie_Data_Cleaned[predictor],Movie_Data_Cleaned[predicted],test_size=0.1,shuffle=False)

    #fit data
    Encoder = LabelEncoder()
    Train_Y = Encoder.fit_transform(Train_Y)
    Test_Y = Encoder.fit_transform(Test_Y)

    #using 10,000 features
    Tfidf_vect = TfidfVectorizer(max_features=10000)
    Tfidf_vect.fit(Movie_Data_Cleaned[predictor])

    Train_X_Tfidf = Tfidf_vect.transform(Train_X)
    Test_X_Tfidf = Tfidf_vect.transform(Test_X)

    #Run SVM model on training data
    SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='scale', random_state=1)
    SVM.fit(Train_X_Tfidf,Train_Y)

    # predict binary on test data
    predictions_SVM = SVM.predict(Test_X_Tfidf)

    #return needed values to save if need to rerun anything
    return SVM, Tfidf_vect, predictions_SVM, accuracy_score(predictions_SVM, Test_Y)*100

def add_column_to_df(df, string1, string2):
    # Create array N
    SVMi, Tfidf_vecti, predictions_SVMi, accuracyi = Run_SVM_Test(string1, string2)

    # Add column to df with column nam-e 'string1:string2'
    column_name = f'{string1}:{string2}'
    df[column_name] = predictions_SVMi

    return None

#import cleaned data and convert to df
data_location = 'Movies_Data_Full_Clean.csv'
Movie_Data_Cleaned = pd.read_csv(data_location,encoding='latin-1')
prediction_binary = pd.DataFrame()

#list of predictors and response vars for predictions
predictors = ['reviews_cleaned', 'keywords_cleaned']
responses = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary'
,'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance',
'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western', 'quality_binary']

#run all combos of predictor X response to generate testing data predictions
for predictor in predictors:
  for response in responses:
    add_column_to_df(prediction_binary, predictor, response)

#save final file
prediction_binary.to_csv('Movies_Data_Response_Binary_All.csv', index=False) #DO NOT RUN!!!