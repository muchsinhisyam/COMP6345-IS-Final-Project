import pandas
from sklearn.model_selection import train_test_split
import Recommenders as Recommenders

# Read user_id, song_id, listen_count
# This step might take time to download data from external sources
triplets = 'https://static.turi.com/datasets/millionsong/10000.txt'
songs_metadata = 'https://static.turi.com/datasets/millionsong/song_data.csv'

song_df_a = pandas.read_table(triplets,header=None)
song_df_a.columns = ['user_id', 'song_id', 'listen_count']

# Read song  metadata
song_df_b = pandas.read_csv(songs_metadata)

# Merge the two dataframes above to create input dataframe for recommender systems
song_df1 = pandas.merge(song_df_a, song_df_b.drop_duplicates(['song_id']), on="song_id", how="left")
song_df1.head()

song_df1 = song_df1.head(10000)

# Merge song title and artist_name columns to make a new column
song_df1['song'] = song_df1['title'].map(str) + " - " + song_df1['artist_name']

song_gr = song_df1.groupby(['song']).agg({'listen_count': 'count'}).reset_index()
grouped_sum = song_gr['listen_count'].sum()
song_gr['percentage']  = song_gr['listen_count'].div(grouped_sum)*100
song_gr.sort_values(['listen_count', 'song'], ascending = [0,1])

print("Total no of songs:",len(song_df1))
u = song_df1['user_id'].unique()
print("The no. of unique users:", len(u))

#Train data
train, test_data = train_test_split(song_df1, test_size = 0.20, random_state=0)
print(train.head(5))

# Create an instance of the class
# pm = Recommenders.popularity_recommender()
# pm.create(train, 'user_id', 'song')
# user_id1 = u[5]
# Recommended songs list for a user
# pm.recommend(user_id1)
# user_id2 = u[8]
# pm.recommend(user_id2)

is_model = Recommenders.similarity_recommender()
is_model.create_s(train, 'user_id', 'song')

# Print the songs for the user
user_id1 = u[5]
user_items1 = is_model.get_u_items(user_id1)
print("------------------------------------------------------------------------------------")
print("Songs played by first user %s:" % user_id1)
print("------------------------------------------------------------------------------------")
for user_item in user_items1:
    print(user_item)
print("----------------------------------------------------------------------")
print("Similar songs recommended for the first user:")
print("----------------------------------------------------------------------")
#Recommend songs for the user using personalized model
is_model.recommend_s(user_id1)

user_id2 = u[7]
#Fill in the code here
user_items2 = is_model.get_u_items(user_id2)
print("------------------------------------------------------------------------------------")
print("Songs played by second user %s:" % user_id2)
print("------------------------------------------------------------------------------------")
for user_item in user_items2:
    print(user_item)
print("----------------------------------------------------------------------")
print("Similar songs recommended for the second user:")
print("----------------------------------------------------------------------")
#Recommend songs for the user using personalized model
is_model.recommend_s(user_id2)

is_model.similar_items(['U Smile - Justin Bieber'])