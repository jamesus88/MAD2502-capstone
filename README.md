# README.md
This file contains instructions on how and in what order to run the files provided for our capstone project (group: girlscout)
## Collecting Movie Data
1. You will need credentials to access TMDB. Go to https://www.themoviedb.org/?language=en-US to create an account. Visit their API documentation to get the appropriate header json to include when running the movies.py file.
2. Paste your headers variable into a python file named *credentials.py* in the same folder as this *README.md*. The file *db_data.py* will call this file to load in the movie data.
3. Configure *movies.py*:
On line 13, enter a year range of movies to search for.
4. Run *movies.py*. This will output a large csv file full of movie reviews called *MOVIES.csv*.
## Creating Prediction Data
6. Run *Data_Cleaning.py*. This will clean *MOVIES.csv* and output a cleaned file.
7. Run *Data_Analysis.py*. This will train an SVM model and save the output binary as a csv file.
## Starting the Webapp
8. This portion requires Flask as a dependency. Alternatively, view our example webapp at https://tinyurl.com/yc6tzvme
9. If running on your own, open the *flask_app* directory as your main folder.
10. Drag and drop *Movies_Data_Full_Clean.csv* and *Movies_Data_Response_Binary.csv* into the *flask_app* directory.
11. Run *app.py* to host a local server
12. Upload *app.yaml* to a Google Cloud App Engine to host a live server on the internet.
