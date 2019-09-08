import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import argparse, sys

#Dictionaries for age and occupation codes 
age_dict = {1: "18 below", 18: "18-24", 25: "25-34",
      35: "35-44", 45: "45-49", 50: "50-55", 56: "56+"}
occupation_dict = {0: "other/not specified", 1: "academic/educator", 2: "artist", 3: "clerical/admin",
          4: "college/grad student", 5: "customer service", 6: "doctor/health care", 7: "executive/managerial",
          8: "farmer", 9: "homemaker", 10: "K-12 student", 11: "lawyer",
          12: "programmer", 13: "retired", 14: "sales/marketing", 15: "scientist",
          16: "self-employed", 17: "technician/engineer", 18: "tradesman/craftsman", 19: "unemployed", 20: "writer"}

def main():
    # Parse the arguments (input files)
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratingsfile", type = argparse.FileType(), help = "path of ratings.dat file", 
                        default = 'ratings.dat')
    parser.add_argument("--moviesfile", type = argparse.FileType(), help = "path of movies.dat file", 
                        default = 'movies.dat')
    parser.add_argument("--usersfile", type = argparse.FileType(), help = "path of users.dat file", 
                        default = 'users.dat')
    args = parser.parse_args()
    
    #Read ratings file to dataframe
    ratings_df = pd.read_csv(args.ratingsfile, sep='::', header = None, engine = 'python', 
                          names = ['u_id', 'm_id', 'rating', 'timestamp'] )
    #In timestamp column keep only year value
    ratings_df['timestamp'] = ratings_df['timestamp'].map(lambda a: datetime.fromtimestamp(a).year)
    
    #Read movies file to dataframe
    movies_df = pd.read_csv(args.moviesfile, sep='::', header = None, engine = 'python', 
                         names = ['m_id', 'm_name', 'm_genres'] )
    #Split genre information into a list of genres in movies_df
    movies_df['m_genres'] = movies_df['m_genres'].str.split('|').tolist()
    
    #Prepare a set of distinct genres
    genre_set = ()
    for glist in movies_df['m_genres']:
        genre_set = list(set(glist) | set(genre_set))
    num_genres = len(genre_set)
    
    #Read users file to dataframe
    users_df = pd.read_csv(args.usersfile, sep='::', header = None, engine = 'python',
                        names = ['u_id', 'u_gender', 'u_age', 'u_occupation', 'u_zip'] )
    #Replace codes for age and occupation for their real values
    users_df = users_df.replace({"u_age": age_dict, 'u_occupation': occupation_dict})
    
    # Create a full dataframe that merges ratings_df, movies_df and users_df 
    full_df = pd.merge(pd.merge(ratings_df, movies_df, on = 'm_id'), users_df, on = 'u_id', )
    # Create exploded version of full_df on the column m_genres
    full_df_explode = full_df.explode('m_genres')
    
    # Initialise ist to store figures
    figures = []
    
    # Fig1: Show distribution of users grouped by age and gender
    f, ax = plt.subplots()
    users_age_gender = users_df.groupby(['u_age', 'u_gender']).size()
    ax = users_age_gender.unstack().plot(kind = 'bar') 
    ax.set(xlabel = 'User Age groups', title = 'Fig 1: User composition by age groups and gender')
    ax.legend(title = 'Gender')
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.2)
    figures.append(fig)
    
    # Fig2: Show distribution of users grouped by occupation and age
    f, ax = plt.subplots()
    users_age_gender = users_df.groupby(['u_occupation', 'u_age']).size()
    ax = users_age_gender.unstack().plot(kind = 'bar', stacked = True) 
    ax.set(xlabel = 'User Occupations', title = 'Fig 2: User composition by age and occupation')
    ax.legend(title = 'Age Groups')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    fig = ax.get_figure()
    fig.subplots_adjust(bottom = 0.5, right = 0.8)
    figures.append(fig)
    
    # Fig3: Show distribution of movies by genre 
    f, ax = plt.subplots()
    genre_count = pd.DataFrame(np.zeros(shape=(num_genres,1)), index = genre_set)
    for glist in movies_df['m_genres']:
        for g in glist:
            genre_count[0][g] += 1
    ax = genre_count.plot.pie(y = 0, shadow = True)
    ax.set(title = 'Fig 3: Genres of movies in datatset', ylabel = '')
    ax.legend(loc='center left', bbox_to_anchor=(1.1, 0.5))
    fig = ax.get_figure()
    fig.subplots_adjust(bottom = 0.1, right = 0.7)
    figures.append(fig)
    
    # Fig4: Show genres that co-occur in movies
    genre_cooccurances = pd.DataFrame(np.zeros(shape=(num_genres,num_genres)), columns = genre_set, index  = genre_set)
    for glist in movies_df['m_genres']:
        for g1 in glist:
            for g2 in glist:
                if g1 != g2: genre_cooccurances[g1][g2] += 1
    
    f, ax = plt.subplots()
    mask = np.zeros_like(genre_cooccurances)
    mask[np.triu_indices_from(mask)] = True
    ax = sns.heatmap(genre_cooccurances, mask=mask, cmap="YlGnBu")
    ax.set_title('Fig 4: Co-occuring genres in movies')
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.2)
    figures.append(fig)
    
    # Fig5: Show distribution of rating levels grouped by gender
    f, ax = plt.subplots()
    rating_dis = full_df.groupby(['rating', 'u_gender']).size()
    ax = rating_dis.unstack().plot(kind = 'bar', stacked = True)
    ax.set(title ='Fig 5: Frequencies of rating levels', xlabel = 'Rating Levels', ylabel = '#')
    ax.legend(title = 'Gender')
    fig = ax.get_figure()
    figures.append(fig)
    
    # Fig6: Show 10 most rated movies
    f, ax = plt.subplots()
    ratings_freq = full_df.groupby(['m_name']).size().nlargest(10)
    ax = ratings_freq.plot(kind = 'bar') 
    ax.set(title = 'Fig 6: Most rated movies (popular movies)', xlabel = 'Movies', ylabel = '# Ratings')
    ax.xaxis.set_tick_params(labelsize=8)
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.5)
    figures.append(fig)
   
    # Fig7: Show 10 movies with highest average ratings
    f, ax = plt.subplots()
    rating_freqs = full_df['m_name'].value_counts()
    keep_movies = list(rating_freqs[rating_freqs > 500].index)
    full_df2 = full_df[full_df['m_name'].isin(keep_movies)]
    ratings_avg = full_df2.groupby('m_name')['rating'].mean().nlargest(10)
    ax = ratings_avg.plot(kind = 'bar') 
    ax.set_ylim([4.4,4.6])
    ax.xaxis.set_tick_params(labelsize=6)
    ax.set(title = 'Fig 7: Best rated movies (Avg ratings for movies with more than 500 ratings)', xlabel = 'Movies', ylabel = 'Avg Ratings')
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.5)
    figures.append(fig)
    
    # Fig8: Show number of ratings received by genre
    f, ax = plt.subplots()
    genre_gender_size = full_df_explode.groupby(['m_genres', 'u_gender']).size()
    ax = genre_gender_size.unstack().plot(kind = 'bar', stacked = True)
    ax.set(title= 'Fig 8: Number of ratings received by genres', xlabel = 'Genres', ylabel = '# Ratings')
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.5)
    figures.append(fig)
    
    # Fig9: Show average ratings received by genre
    f, ax = plt.subplots()
    genre_gender_avgrating = full_df_explode.groupby(['m_genres', 'u_gender'])['rating'].mean()
    ax = genre_gender_avgrating.unstack().plot(kind = 'bar')
    ax.set(title = 'Fig 9: Average ratings received for genres', xlabel = 'Genres', ylabel = 'Avg rating')
    ax.set_ylim([2,5])
    fig = ax.get_figure()
    fig.subplots_adjust(bottom=0.2)
    figures.append(fig)
    
    # Fig10: Show number unique users that have given rating per year
    f, ax = plt.subplots()
    unique_users = full_df.groupby(['timestamp', 'u_gender'])['u_id'].nunique()
    ax = unique_users.unstack().plot(kind = 'bar')
    ax.set(title = 'Fig 10: Unique active users (who have given rating) per year', xlabel = 'Year', ylabel = '# Active users')
    fig = ax.get_figure()
    figures.append(fig)
    
    # Fig11: Show average rating received by genre each year
    f, ax = plt.subplots()
    unique_users = full_df_explode.groupby(['timestamp', 'm_genres'])['rating'].mean()
    ax = unique_users.unstack().plot(kind = 'bar')
    ax.set(title = 'Fig 11: Average ratings for genres per year', xlabel = 'Year', ylabel = 'Average rating')
    ax.set_ylim([2.5,4.5])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    fig = ax.get_figure()
    fig.subplots_adjust(right = 0.8)
    figures.append(fig)
    
    # Save all figures to report.pdf file
    with PdfPages('ML1M-report.pdf') as pdf:
        for fi in figures:
            fi.set_size_inches([10,7])
            
            pdf.savefig(fi)

if __name__ == '__main__':
    main()