#importing the basic libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import warnings
warnings.filterwarnings('ignore')

# importing the datasets.

movies = pd.read_csv("G:\DataSets\MovieDAta SET\movies_metadata.csv")
ratings = pd.read_csv("G:/DataSets/MovieDAta SET/ratings.csv")
credit = pd.read_csv("G:\DataSets\MovieDAta SET\credits.csv")
keywords = pd.read_csv("G:\DataSets\MovieDAta SET\keywords.csv")
links = pd.read_csv("G:\DataSets\MovieDAta SET\links.csv")

# understanding the data
#movies.head().transpose()

#movies.columns

#movies.shape

movies = movies.drop(['imdb_id'], axis = 1)

movies[movies['original_title'] != movies['title']][['title', 'original_title','production_companies']].head(10)

movies = movies.drop('original_title', axis = 1)

#movies.shape

# replacing the unknown value of revenue to Nan
movies['revenue'] = movies['revenue'].replace(0, np.nan)

# replacing the unknown value of budget to Nan
movies['budget'] = pd.to_numeric(movies['budget'], errors = 'coerce')
movies['budget'] = movies['budget'].replace(0, np.nan)
movies[movies['budget'].isnull()].shape  # no of movies whoes budget information is unknown

# adding some feature to the movies data:

# 1. return
# 2. year


movies['return'] = movies['revenue'] / movies['budget']
movies[movies['return'].isnull()].shape # no of movies whose return information is unknown.

movies['year'] = pd.to_datetime(movies['release_date'], errors = 'coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

movies = movies.drop('adult', axis = 1)  # there is almost 0 adult movies in this dataset, so drop it.

base_poster_url = 'http://image.tmdb.org/t/p/w500/'
movies['poster_path'] = "<img src='" + base_poster_url + movies['poster_path'] + "' style='height:100px;'>"

# discovering the most often used words as a movie title and movie overview.

movies['title'] = movies['title'].astype('str')
movies['overview'] = movies['overview'].astype('str')

#  making the Recommendation System
import ast
movies['genres'] = movies['genres'].fillna('[]').apply(ast.literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

movies['movieId'] = movies['title'] + movies['year']
#movies['movieId']
parent_movies = movies
# Making the Top Movies Chart by using IMDB weighted rating formula  Weighted Rating (WR) = ((v/v+m).R)+((m/v+m).C)


#  v is the number of votes for the movie
#  m is the minimum votes required to be listed in the chart
#  C is the mean vote across the whole report
#  R is the average rating of the movie

vote_counts = movies[movies['vote_count'].notnull()]['vote_count'].astype('int')
vote_averages  = movies[movies['vote_average'].notnull()]['vote_average'].astype('int')
C = vote_averages.mean()
#C

M = vote_counts.quantile(0.95)
#M

movies['year'] = pd.to_datetime(movies['release_date'],errors = 'coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)

qualified_movies = movies[(movies['vote_count'] >= M) & (movies['vote_count'].notnull()) & (movies['vote_average'].notnull())][['title', 'year', 'vote_count','vote_average', 'popularity', 'genres', 'poster_path']]
qualified_movies['vote_count'] = qualified_movies['vote_count'].astype('int')
qualified_movies['vote_average'] = qualified_movies['vote_average'].astype('int')
#qualified_movies.shape

#  I have 2274 movies in my top movies chart
# qualified movies have at least 434 vote count and average rating of 5.2 on TMDB.

def weighted_rating(x):
    v = x['vote_count']
    r = x['vote_average']
    return (v/(v+M)*r) + (M/(M + v)*C)

qualified_movies['wr'] = qualified_movies.apply(weighted_rating, axis = 1)

qualified_movies = qualified_movies.sort_values('wr', ascending = False).head(300)
qualified_movies["movieId"] = qualified_movies["title"] + qualified_movies["year"]
our_qualified_movies = qualified_movies
# Top Movies

#qualified_movies.head(20)

# Top movies based on genere of the movie.
#
# Simple Recommender

g = movies.apply(lambda x: pd.Series(x['genres']), axis = 1).stack().reset_index(level = 1, drop = True)
g.name = 'genre'
movie_genre = movies.drop('genres', axis = 1).join(g)

def top_movie_based_on_genre(genre, percentile = 0.85):
    mov = movie_genre[movie_genre['genre'] == genre]
    vote_counts = mov[mov['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = mov[mov['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    M = vote_counts.quantile(percentile)


    qualified_movies = mov[(mov['vote_count'] >= M) & (mov['vote_count'].notnull()) & (mov['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'poster_path',]]

    qualified_movies['vote_count'] = qualified_movies['vote_count'].astype('int')
    qualified_movies['vote_average'] = qualified_movies['vote_average'].astype('int')
    qualified_movies['weighted_ratio'] = qualified_movies.apply(lambda x: (x['vote_count']/(x['vote_count'] + M) * x['vote_average']) + (M/(M + x['vote_count']) * C), axis = 1)

    qualified_movies = qualified_movies.sort_values('weighted_ratio', ascending = False).head(300)
    qualified_movies["movieId"] = qualified_movies["title"] + qualified_movies["year"]
    return qualified_movies

# Top Action Movie:

#top_movie_based_on_genre('Action').head(10)
#top_movie_based_on_genre('Romance').head(10)
#top_movie_based_on_genre('Comedy').head(10)
#top_movie_based_on_genre('Drama').head(10)


# Simple Content-based Recommender

keywords['id'] = keywords['id'].astype('int')

credit['id'] = credit['id'].astype('int')
movies = movies.drop([19730, 29503, 35587])
movies['id'] = movies['id'].astype('int')

links_small = pd.read_csv('G:\DataSets\MovieDAta SET\links_small.csv')
links_small = links_small[links_small['tmdbId'].notnull()]['tmdbId'].astype('int')

movies = movies.merge(credit, on = 'id')
movies = movies.merge(keywords, on = 'id')

small_movie_df = movies[movies['id'].isin(links_small)]
small_movie_df.shape

small_movie_df['crew'] = small_movie_df['crew'].apply(ast.literal_eval)
small_movie_df['cast'] = small_movie_df['cast'].apply(ast.literal_eval)
small_movie_df['keywords'] = small_movie_df['keywords'].apply(ast.literal_eval)
small_movie_df['crew_size'] = small_movie_df['crew'].apply(lambda x: len(x))
small_movie_df['cast_size'] = small_movie_df['crew'].apply(lambda x: len(x))

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
        return np.nan

small_movie_df['director'] = small_movie_df['crew'].apply(get_director)

small_movie_df['cast'] = small_movie_df['cast'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
small_movie_df['cast'] = small_movie_df['cast'].apply(lambda x: x[ :3] if len(x) >= 3 else x)
small_movie_df['keywords'] = small_movie_df['keywords'].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

small_movie_df['cast'] = small_movie_df['cast'].apply(lambda x: [str.lower(i.replace(" ","")) for i in x])
small_movie_df['director'] = small_movie_df['director'].astype('str').apply(lambda x: str.lower(x.replace(" ","")))
small_movie_df['director'] = small_movie_df['director'].apply(lambda x: [x, x, x])# making director 3 times so that it have more weighted than entire cast we can do same with cast too.

s = small_movie_df.apply(lambda x: pd.Series(x['keywords']),axis=1).stack().reset_index(level=1, drop=True)
s.name = 'keyword'


small_movie_df['cas_dir_gen'] = small_movie_df['cast'] + small_movie_df['director'] + small_movie_df['genres']
small_movie_df['cas_dir_gen'] = small_movie_df['cas_dir_gen'].apply(lambda x: ' '.join(x))

# importing the sklearn countvectorizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

count = CountVectorizer(analyzer = 'word', ngram_range = (1, 2), min_df = 0, stop_words = 'english')
count_matrix = count.fit_transform(small_movie_df['cas_dir_gen'])

# importing the cosine similarity function

from sklearn.metrics.pairwise import linear_kernel, cosine_similarity

cosin_sim = cosine_similarity(count_matrix, count_matrix)

small_movie_df = small_movie_df.reset_index()
#recomended_movies = [['title', 'poster_path']]
titles = small_movie_df['title']
poster = small_movie_df['poster_path']
indices = pd.Series(small_movie_df.index, index = small_movie_df['title'])

#def content_based_recommendation(title):
    #index = indices[title]
    #sim_scores = list(enumerate(cosin_sim[index]))
    #sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    #sim_scores = sim_scores[1:31]
    #movie_indices = [i[0] for i in sim_scores]
    #return titles.iloc[movie_indices]

#content_based_recommendation('Jumanji').head(10)

# improved content-based recommender

def improved_content_based_recommender(title):
    index = indices[title]
    sim_scores = list(enumerate(cosin_sim[index]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:25] # top 25 movies based on similarity score.
    movie_indices = [i[0] for i in sim_scores]

    mov = small_movie_df.iloc[movie_indices][['title', 'vote_count', 'vote_average', 'year', 'poster_path']]
    mov['movieId'] = mov['title'] + mov['year']
    mov1 = mov
    vote_counts = mov1[mov1['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = mov1[mov1['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)
    qualified = mov1[(mov1['vote_count'] >= m) & (mov1['vote_count'].notnull()) & (mov1['vote_average'].notnull())]

    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified['wr'] = qualified.apply(weighted_rating, axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    return qualified


#improved_content_based_recommender('Jumanji')

# collaborative Filtering:

#imporint the surprise librarie
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate

reader = Reader()

#ratings.head()

data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

svd = SVD()

#cross_validate(svd, data, measures = ['RMSE', 'MAE'], cv = 5, verbose = True)

trainset = data.build_full_trainset()
svd.fit(trainset)

#hybrid recommender

def convert_int():
    try:
        return int()
    except:
        return np.nan

id_map = pd.read_csv('G:\DataSets\MovieDAta SET\links_small.csv')[['movieId', 'tmdbId']]

#id_map['tmdbId'] = id_map['tmdbId'].apply(convert_int)
id_map.columns = ['movieId', 'id']
id_map = id_map.merge(small_movie_df[['title', 'id']], on='id').set_index('title')

indices_map = id_map.set_index('id')

def hybrid_recommender(userId, title):
    index = indices[title]
    tmdbId = id_map.loc[title]['id']
    movie_id = id_map.loc[title]['movieId']
    sim_scores = list(enumerate(cosin_sim[int(index)]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:26]
    movie_index = [i[0] for i in sim_scores]
    movies = small_movie_df.iloc[movie_index][['title', 'vote_count', 'vote_average', 'year', 'id', 'poster_path']]
    movies['movieId'] = movies['title'] + movies['year']
    movies['est'] = movies['id'].apply(lambda x: svd.predict(userId, indices_map.loc[x]['movieId']).est)
    movies = movies.sort_values('est', ascending = False)
    return movies.head(10)
#hybrid_recommender(1,'Toy Story')        
