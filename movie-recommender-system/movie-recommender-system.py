#!/usr/bin/env python
# coding: utf-8

#  # movie recommender system 
#  * content based recommendation system

# In[ ]:


import numpy as np
import pandas as pd


# In[232]:


movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')


# In[174]:


movies.head(3)


# In[175]:


movies.columns


# In[177]:


id = movies[movies.title=='Avatar'].id[0]
credits[credits.movie_id == id]


# 
# > **Q** can we can join these two tables ? 
# - yes table (movies-> id , credits.movie_id) or on 'title'

# In[178]:


movies.merge(credits, on='title').columns, movies.merge(credits, on='title').shape


# In[179]:


movies.merge(credits, left_on='id', right_on='movie_id').columns, movies.merge(credits, left_on='id', right_on='movie_id').shape


# In[233]:


# when we merge on id , we are getting extra columns on title and there are some rows missing, 
# we will merge on movie title
movies_db = movies.merge(credits, on='title')


# In[181]:


movies_db.info()


# #### now which columns to keep which shall be important for content based filtering? 
# 
# 
# | column | keep ? | remark |
# |:---------|:--------:|:--------:|
# | **budget**  | no | people do not watch movies based on budget |
# | **homepage**  | no | not required |
# | **original_language**  | no | biased towards english language |
# | **original_title**  | no | this is mostly regional based |
# | **popularity**  | no | not suitable to create tags, also numberic based |
# | **production_companies**  | no | normally we do not recommend who has produced the movie |
# | **production_countries**  | no | does not matter to the viewes where it is produced |
# | **release_date**  | maybe | skipped becuase of numeric |
# | **revenue**  | maybe | skipped becuase of numeric |
# | **runtime**  | no | does not matter |
# | **spoken_languages**  | no | more than languages, story matters |
# | **status**  | no | does not matter |
# | **tagline**  | no | give something else, keep overview |
# | **vote_average**  | no | skipped becuase of numeric |
# | **vote_count**  | no | skipped becuase of numeric |
# | **movie_id**  | no | we have kept id |
# | **genres**  | yes | people talk which genre they like |
# | **id**  | yes | to make the picture |
# | **keywords**  | yes | to get the tags |
# | **overview**  | yes | to find the context |
# | **release_date**  | yes | older guys like certain time period movies, yonger more recent |
# | **title**  | yes | this is not regional based |
# | **cast**  | yes | people like actors based |
# | **crew**  | yes | people like directors based |
# 
# 
# columns_we_kept = ['genres', 'id', 'keywords', 'overview', 'release_date', 'title', 'cast', 'crew']
# 
# 
# 
# 

# In[247]:


columns_we_kept = ['id','title', 'overview', 'genres', 'keywords','cast', 'crew']


# In[ ]:





# In[183]:


movies_db[movies_db['original_title'] != movies_db['title']][['original_title', 'title']]


# In[184]:


movies_db[['tagline', 'overview']]


# In[248]:


movies_db = movies_db[columns_we_kept]


# In[186]:


## below are the movies data with reduced columns that we are going to work
movies_db.info()


# In[249]:


movies_db.head()


# In[111]:


## now we want to have 
# movie_id, title , tags
# we are goings to merge overview, keyword, title, cast, crew


# ### Data cleaning

# #### missing data

# In[236]:


movies_db.isna().sum()


# In[237]:


movies_db.dropna(inplace=True)
movies_db.isna().sum()


# In[190]:





# In[238]:


# check dubplicates 
movies_db.duplicated().sum()


# In[129]:


### genres


# In[239]:


movies_db.iloc[0].genres


# In[240]:


def convert(genres):
    genres = eval(genres)
    return [genre['name'] for genre in genres] 

convert(movies_db.iloc[0].genres)


# In[241]:


movies_db.genres.apply(lambda x:convert(x))


# In[242]:


movies_db.genres = movies_db.genres.apply(convert)
movies_db.keywords = movies_db.keywords.apply(convert)


# In[243]:


movies_db


# In[244]:


def get_top3_cast(cast):
    top3cast = [cast['name'] for cast in eval(cast)[:3]]
    return top3cast

get_top3_cast(movies_db.iloc[0].cast)


# In[245]:


movies_db.cast = movies_db.cast.apply(get_top3_cast)


# In[246]:


movies_db


# In[223]:


[cast['name'] for cast in eval(movies_db.iloc[0].cast)[:3]]


# In[251]:


movies_db


# In[268]:


def get_director_name(crew):
    director = [item['name'] for item in eval(crew) if item['job'] == 'Director']
    return director

get_director_name(movies_db.iloc[1].crew)


# In[269]:


movies_db.crew = movies_db.crew.apply(get_director_name)


# In[272]:


movies_db.head()


# In[278]:


movies_db.overview = movies_db.overview.apply(lambda x: x.split())


# In[280]:


movies_db.head()


# #### transformation to join two words into one, so that one tag should be formed instead of two

# In[289]:


def remove_space_from_words(words):
    return [item.replace(" ", "") for item in words]

remove_space_from_words(movies_db.cast[0])


# In[295]:


movies_db.keywords.apply(remove_space_from_words)


# In[305]:


for col in ['cast', 'crew', 'keywords', 'genres']:
    movies_db[col] = movies_db[col].apply(remove_space_from_words)


# In[307]:


movies_db


# In[308]:


movies_db['tag'] = movies_db.overview + movies_db.keywords + movies_db.genres + movies_db.cast + movies_db.crew


# In[310]:


movies_db.head(3)


# In[312]:


movies_db_final = movies_db[['id', 'title', 'tag']]


# In[316]:


movies_db_final['tag'] = movies_db_final['tag'].apply(lambda x: " ".join(x))


# In[320]:


movies_db_final.iloc[0].tag


# In[322]:


movies_db_final.tag = movies_db_final.tag.apply(lambda x: x.lower())


# In[324]:


movies_db_final.head()


# ### vectorization

# #### we need to get the simlarity score for the tags
# * we need to convert the tags into the vectors
# * bag of words -> technique for converting tags to vector

# In[344]:


import nltk
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()


# In[353]:


def stem(text):
    return " ".join([ps.stem(item) for item in text.split() ])


# In[349]:


['loved', 'loving', 'love']


# In[359]:


## we will get the root word -> 
stem(" ".join(['loved', 'loving', 'loves', 'love']))


# In[355]:


stem(movies_db_final.tag[0])


# In[327]:


movies_db_final['tag'][0]


# In[ ]:





# In[361]:


movies_db_final['tag'] = movies_db_final.tag.apply(stem)


# In[362]:


movies_db_final.head()


# In[372]:


from sklearn.feature_extraction.text import CountVectorizer


# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html
# 
# * Convert a collection of text documents to a matrix of token counts.

# In[364]:


cv = CountVectorizer(max_features=5000,stop_words='english')
vectors = cv.fit_transform(movies_db_final['tag']).toarray()


# In[365]:


vectors.shape


# In[366]:


# every movie is in vecotr
vectors


# In[368]:


# words most used
# we have prolem with words like action, actions, 
# we will apply stemming 
cv.get_feature_names_out()[:100]


# In[370]:


# now we have to calculate distance of each movie with other
# we will not use euclidean distance, instead we will use Cosine Similarity
# euclidean distance is not a reliable measure in high dimensions


# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html
# 
# * Compute cosine similarity between samples in X and Y.

# In[374]:


from sklearn.metrics.pairwise import cosine_similarity


# In[378]:


cosine_similarity(vectors).shape


# In[380]:


similarity_matrix = cosine_similarity(vectors)


# In[383]:


# simlarity of 1st movie with others
similarity_matrix[0]


# In[401]:


def recommend(movie):
    return


# In[489]:


movies_db.sample(4).title


# In[493]:


def recommend(movie):
    index = movies_db[movies_db.title == movie].index[0]
    distances = similarity_matrix[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    for i in movie_list:
        print(movies_db.iloc[i[0]].title)
    
    return 0

recommend('Avatar')


# In[431]:


sorted(list(enumerate(similarity_matrix[0])), reverse=True, key=lambda x:x[1])[1:6]
    

