import requests # package used to call api
from credentials import headers # import local file to load in api username and password. Users should provide their own credentials.py

def get_genres() -> list:
    '''
    Gets all available movie genres that each movie can be categorized under
    \nInput - None
    \nOutput - list of dictionaries containing genre id and name
    '''
    url = "https://api.themoviedb.org/3/genre/movie/list?language=en" 

    response = requests.get(url, headers=headers).json() # get response, convert to json
    return response['genres']

def get_movies(year: int, page=1, min_pop=0):
    '''
    Gets movies from certain page since year provided on api. Each page can contain up to 20 movies. 
    \nInput - \nyear (int): find all movies released in this year\npage (int): search page of data in api\nmin_pop (int): filter movies by minimum popularity value
    \nOutput - response (dict): gets list of all movies on page searched
    '''
    url = f"https://api.themoviedb.org/3/discover/movie?include_adult=true&include_video=false&language=en-US&page={page}&primary_release_year={year}&sort_by=popularity.desc&vote_count.gte={min_pop}"
    
    response = requests.get(url, headers=headers).json() # get response, convert to json
    
    return response

def get_all_movies_in(year=2000, max_pages=500):
    '''
    Gets all movies from year provided. Calls 'get_movies' for as many pages as allowed.
    \nInput -\nyear (int): finds all movies from year \nmax_pages (int): max number of pages allowed to search api for each year.
    \nOutput - list_of_movies (list): list of all movies in year searched
    '''
    page = 1 # start on page 1, no movies
    list_of_movies = []
    while True:
        print('Getting movies from page', page)
        response = get_movies(year, page, min_pop=100) # call get_movies for year and page (default min_pop value = 100)

        if len(response['results']) < 1: # if no results on page, stop searching and return movies
            print('Exhausted year, moving on...')
            break
        list_of_movies.extend(response['results']) # extend list of movies to include ones found on this page
        page = int(response['page']) # get current page number from api response
        
        page += 1
        if page > max_pages: # if page > max allowed, stop searching and return movies
            print('Max pages reached, moving on...')
            break
    
    return list_of_movies


def get_details(id):
    '''
    Gets details of movie with given id
    \nInput - id (any): id of movie to search
    \nOutput - details (dict): details of movie found
    '''
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"
    details = requests.get(url, headers=headers).json() # call api for movie details
    if 'title' not in details: # if no details, return None
        return None
    else: # else return details
        return details

def get_reviews(id):
    '''
    Gets reviews of movie with given id
    \nInput - id (any): id of movie to search
    \nOutput - review_content_str (str): reviews of movie found concatenated into one str
    '''
    url = f"https://api.themoviedb.org/3/movie/{id}/reviews?language=en-US&page=1"
    reviews = requests.get(url, headers=headers).json() # call api for all reviews
    if 'results' in reviews: # if review info, get info from response
        reviews = reviews['results']
    else: # else return None
        return None
    
    review_content = [review['content'] for review in reviews] # get all content from each review
    if len(review_content) > 0: # if any reviews, join all reviews into one string and clean it. Return str
        review_content_str = ' '.join(review_content).replace(",", "").replace("\n", " ").replace("\r", " ")
        return review_content_str
    else: # if no reviews, return None
        return None

def get_keywords(id):
    '''
    Gets keywords of movie with given id
    \nInput - id (any): id of movie to search
    \nOutput - keywords (str): keywords of movie found concatenated into one str
    '''
    url = f"https://api.themoviedb.org/3/movie/{id}/keywords"
    keywords = requests.get(url, headers=headers).json()['keywords'] # get keywords from api response
    return ' '.join([key['name'] for key in keywords]) # return str of keyword names for each keyword in response