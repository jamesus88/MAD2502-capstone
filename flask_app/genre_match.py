
import numpy as np
import pandas as pd
#Take in input as list of string inputs with name of genres
#Check movies for most matched tags with preference given to rating
def tag_matcher(input):
    CSV_Data = pd.read_csv("Movies_Data_Full_Clean.csv")
    data = np.array(CSV_Data)
    col = []

    #Iterate through input and get a list of columns to check for matches
    for tag in input:
        if tag == "Action":
            col.append(7)
        if tag == "Adventure":
            col.append(8)
        if tag == "Animation":
            col.append(9)
        if tag == "Comedy":
            col.append(10)
        if tag == "Crime":
            col.append(11)
        if tag == "Documentary":
            col.append(12)
        if tag == "Drama":
            col.append(13)
        if tag == "Family":
            col.append(14)
        if tag == "Fantasy":
            col.append(15)
        if tag == "History":
            col.append(16)
        if tag == "Horror":
            col.append(17)
        if tag == "Music":
            col.append(18)
        if tag == "Mystery":
            col.append(19)
        if tag == "Romance":
            col.append(20)
        if tag == "Science Fiction":
            col.append(21)
        if tag == "TV Movie":
            col.append(22)
        if tag == "Thriller":
            col.append(23)
        if tag == "War":
            col.append(24)
        if tag == "Western":
            col.append(25)

    matched_movies = []
    matched_tags = []
    for movie in data: #iterates through movies in the data file
        if 'Ã' in movie[2]:
            continue
        
        matches = 0
        for c in col: #Check data from csv file to see if movie matches the genres being searched
            if movie[c] == 1:
                matches += 1
        if len(matched_movies) < 10: #Add the first 10 movies to the searching list
            matched_movies.append(movie)
            matched_tags.append(matches)
            continue
        if len(matched_tags) == 10: #Bubble Sort the 10 movies to make finding the one with the fewest matches easier
            swapped = False
            for i in range(len(matched_tags)-1):
                for j in range(len(matched_tags)-1):
                    if matched_tags[i] > matched_tags[i+1]:
                        swapped = True
                        temp1 = matched_tags[i]
                        temp2 = matched_movies[i]
                        matched_tags[i] = matched_tags[i+1]
                        matched_movies[i] = matched_movies[i+1]
                        matched_movies[i+1] = temp2
                        matched_tags[i+1] = temp1
                if swapped == False: #Include break statement so file does not take O(n^2) every single time
                    break

            small = 0
            for i in range(len(matched_tags)): #Iterate through to find the value currently in the top 10 movies with least matches/low rating
                if matched_tags[i] < matched_tags[small]:
                    small = i
                if matched_tags[i] == matched_tags[small]:
                   if matched_movies[small][3] > matched_movies[i][3]:
                       small = i


            if  matched_tags[small] < matches: #Swap minimum value with current movie if necessary
                matched_tags[small] = matches
                matched_movies[small] = movie
            if  matched_tags[small] == matches:
                if matched_movies[small][3] < movie[3]:
                    matched_tags[small] = matches
                    matched_movies[small] = movie
                
    output = ""            
    for i in range(9, -1, -1): #Iterate through the list backwards to form a top 10 ranking string
        output += f"{10-i}. "
        mystr = matched_movies[i][2]
        output += mystr.title()
        output += "\n" #Insert new line characters so it prints nicely
    return output #Return output
    