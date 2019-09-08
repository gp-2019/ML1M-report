# ML1M-report
Creation of reports on Movielens 1M dataset (available at: https://grouplens.org/datasets/movielens/1m/ )

The report.py script needs the three files from the dataset: ratings.dat, movies.dat and users.dat

It creates a pdf file as output: ML1M-report.pdf

### How to run?
The script can be run as:

```
python report.py --ratingsfile /PATH/ --usersfile /PATH/ --moviesfile /PATH/
```

Note: These arguments are not needed if the three files (ratings.dat, movies.dat and users.dat) are in the same folder as report.py

### How the report is created?
The report is simply created using the ratings given by the users to the movies (from ratings.dat) as well as user metadata (from users.dat) and movies metadata (movies.dat). Pandas dataframes for these datafiles are created alongwith the dataframe of their merge. Then plots that give insights are created using the available data, that are then stored in a pdf file (resultant report ML1M-report.pdf). 

### Brief information about the created plots:



