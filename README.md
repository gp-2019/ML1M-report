# ML1M-report
Creation of reports on Movielens 1M dataset (available at: https://grouplens.org/datasets/movielens/1m/ )

The report.py script needs the three files from the dataset: ratings.dat, movies.dat and users.dat

It creates a pdf file as output: ML1M-report.pdf

### How to run?
The script can be run as:

```
python report.py --ratingsfile /PATH/ --usersfile /PATH/ --moviesfile /PATH/
```

Note: These arguments are not needed if the three files (ratings.dat, movies.dat and users.dat) are in the current directory.

### How the report is created?
The report is simply created using the ratings given by the users to the movies (from ratings.dat) as well as user metadata (from users.dat) and movies metadata (movies.dat). Pandas dataframes for these datafiles are created alongwith the dataframe of their merge. Then plots that give insights are created using the available data, that are then stored in a pdf file (resultant report ML1M-report.pdf). 

### Brief information about the created plots:

In the output file there are 11 different figures.

#### Fig 1: User composition by age groups and gender
This figure shows the distribution of users in the dataset by their age groups and gender.

#### Fig 2: User composition by age and occupation
This figure shows the distribution of users in the dataset by their occupations and age groups.

#### Fig 3: Genres of movies in datatset
This figure shows the share of genres in the movies present in the dataset in the form of a pie chart.

#### Fig 4: Co-occuring genres in movies
Since movies can have multiple genres, this figure presents a heat map showing pairwise co-occurance of genres in movies.

#### Fig 5: Frequencies of rating levels
Users have given ratings on level 1 to 5 (only natural numbers) to movies. This figure shows the freqeuncy of each rating level (also user gender wise).

#### Fig 6: Most rated movies (popular movies)
This figure simply shows the 10 movies that have received the highest number of ratings in the dataset.

#### Fig 7: Best rated movies (Avg ratings for movies with more than 500 ratings)
This figure shows the top 10 movies that have received the highest average ratings. Only those movies that have received more than 500 ratings are considered.

#### Fig 8: Number of ratings received by genres
This figure shows the number of ratings received by each genre (measure of popularity of each genre), and is also separated by gender.

#### Fig 9: Average ratings received for genres
This figure shows the average ratings received by each genre (measure of popularity of each genre), and is also compared for genders.

#### Fig 10: Unique active users (who have given rating) per year
This figure shows the number of unique users that have given any rating for the different years.

#### Fig 11: Average ratings for genres per year
This figure shows the average rating received by the genres per year.






