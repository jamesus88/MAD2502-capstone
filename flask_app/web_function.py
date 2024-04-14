import pandas as pd
from sklearn.metrics import accuracy_score
from flask import url_for

all_genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary'
,'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance',
'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']
#website functionality
def website_functionality(movie_title, predictor_var, response_var):
    print(movie_title, predictor_var, response_var)
    Binary_outputs = pd.read_csv('Movies_Data_Response_Binary_All.csv',encoding='latin-1')
    Movie_Data_Cleaned = pd.read_csv('Movies_Data_Full_Clean.csv',encoding='latin-1')
    cleaned_tail = Movie_Data_Cleaned.tail(735)
    index_initial = cleaned_tail[cleaned_tail['title'] == movie_title].index
    if index_initial.empty and not(movie_title=='overview'):
        return None

    index =  index_initial-6608

    column = predictor_var + ':' + response_var
    print(column)
    num_6 = []
    num_7 = []

    if movie_title == 'overview' and response_var != 'all genres':
        num_6.append(accuracy_score(Binary_outputs[column], cleaned_tail[response_var])*100)
    elif movie_title == 'overview' and response_var == 'all genres':
        for genre in all_genres:
            column = predictor_var + ':' + genre
            num_6.append(accuracy_score(Binary_outputs[column], cleaned_tail[genre])*100)
    elif response_var == 'all genres':
        print('all genres running')
        for genre in all_genres:
            column = predictor_var + ':' + genre
            if Binary_outputs.loc[index, column].iloc[0] == 1:
                num_6.append(genre)
            if Movie_Data_Cleaned.loc[index, genre].iloc[0] == 1:
                num_7.append(genre)
    elif response_var == 'quality_binary':
        num_6.append(Binary_outputs.loc[index, column].iloc[0])
        num_7.append(Movie_Data_Cleaned.loc[index, 'quality_rating'].iloc[0])
    else:
        num_6.append(Binary_outputs.loc[index, column].iloc[0])
        num_7.append(Movie_Data_Cleaned.loc[index, response_var].iloc[0])

    return num_6, num_7

def get_movie_titles():
    Movie_Data_Cleaned = pd.read_csv('Movies_Data_Full_Clean.csv',encoding='latin-1')
    return Movie_Data_Cleaned.tail(735)['title'].to_list()