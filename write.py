def write_to_file(writer, movie, all_genres):
    '''
    generic write function for a csv writer and movie
    '''
    # get movie data from movie dict
    _id = str(movie['id'])
    release_date = movie.get('release_date')
    title = movie.get('title', 'n/a').lower()
    quality_rating = movie.get('vote_average')
    revenue = movie.get('revenue')
    keywords = movie['keywords']
    reviews = movie['reviews']

    genres = [genre['name'] for genre in movie.get('genres')] # list of all genre names

    # list of all outputs, including whether or not the movie has each genre possible represented in binary
    movie_cols = [_id, release_date, title, quality_rating, revenue, keywords, reviews] + [1 if g['name'] in genres else 0 for g in all_genres]

    writer.writerow(movie_cols) # write to the file