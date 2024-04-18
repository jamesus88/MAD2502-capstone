from flask import Flask, render_template, url_for, request # import Flask
from web_function import *
from genre_match import tag_matcher
app = Flask(__name__) # create app

@app.route("/", methods=['GET', 'POST']) # route get and post methods to "/"
def home(): # run when user goes to 'domain/'
    msg = ''

    if request.method == 'POST': # if it is a post request, read form data and get data from model
        if request.form.get('function') == 'predict_genre': # if user selected the predict genre function
            print('predicting genres')

            # get user inputs
            movie_title = request.form.get('movie_title').lower()
            response_var = request.form.get('response_var')
            predictor_var = request.form.get('predictor_var')

            # get predicted results from user inputs
            res = website_functionality(movie_title, predictor_var, response_var)

            if res:
                # format response for html viewing
                response = {
                    'used_var': 'Reviews' if predictor_var=='reviews_cleaned' else 'Keywords',
                    'predicted_key': 'Quality Rating' if response_var == 'quality_binary' else 'All Genres' if response_var == 'all genres' else response_var,
                    'actual': res[1],
                    'predicted': res[0],
                    'title': movie_title.title()
                }

                return render_template("predicted.html", response=response, all_genres=all_genres) # return rendered html
            else: # movie does not exist
                msg = 'Error: movie not in prediction data (choose 1 of 735)!'
            

        elif request.form.get('function') == 'get_popular':
            genres = request.form.getlist('genres')
            top_ten = tag_matcher(genres).split('\n')
            return render_template("popular.html", top_ten=top_ten, genres=genres)

    return render_template("home.html", msg=msg, all_genres=all_genres) # return rendered html to the user with variable arguments


@app.route("/movies") # routes users to "/movies"
def movies():
    all_movies = get_movie_titles() # get all searchable movies
    return render_template("movies.html", all_movies=all_movies) # return rendered templates

if __name__ == '__main__':
    app.run(debug=True) # run the webapp


