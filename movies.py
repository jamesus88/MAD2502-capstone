# import csv module and other py files
import write
import db_data
import csv

all_genres = db_data.get_genres() # call function to get all genres
file = open('./MOVIES.csv', 'w', newline='') # open csv file to append data to 
writer = csv.writer(file, delimiter=',') # create csv writer instance
# create list of all column headers for csv
cols = ['id','release_date', 'title', 'quality_rating', 'revenue', 'keywords', 'reviews'] + [g['name'] for g in all_genres]
writer.writerow(cols) # write headers

year_range = [1970, 2024]

movie_list = [] # initialize movie list
for year in range(year_range[0], year_range[1]+1): # for each year in year_range
    print('Finding movies in', year)
    # call function to get list of all movies in each year. Extend movie_list with this list.
    movie_list.extend(db_data.get_all_movies_in(year, max_pages=300))

total = len(movie_list)
print(f'Found {total} movies between {year} and {movie_list[-1]['release_date']}')
# initialize total count and added movies
count = 0
added = 0

for movie in movie_list:
    print(f'{round(count/total*100, 2)}% complete ({count}/{total}) - {added} movies added so far!')
    print('Looking up', movie['title'])
    count += 1

    # pull movie id and initialize data to empty dict
    id = movie['id']
    movie_data = {}
    
    reviews = {'reviews': db_data.get_reviews(id)} # call function to get concatenated str of all reviews for the movie
    if not reviews['reviews']: # if no reviews, skip movie
        print('No reviews...')
        continue

    details = db_data.get_details(id) # call fucntion to get details for each movie
    if not details: # if no details, skip movie
        print('No details...')
        continue

    keywords = {'keywords': db_data.get_keywords(id)} # call function to get all keywords for each movie

    # add each dict of data to movie_data
    movie_data.update(details)
    movie_data.update(reviews)
    movie_data.update(keywords)

    # call writer function to append to file
    write.write_to_file(writer, movie_data, all_genres)
    print('Added movie!')
    added += 1

file.close() # close file
