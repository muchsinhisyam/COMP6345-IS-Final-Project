import pandas
from sklearn.model_selection import train_test_split
import Recommenders as Recommenders
import spotipy
import spotipy.util as util
import sys

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)

# Spotify Client Settings
client_id = '8654953b081e4a93be3dc54a0bb94b76'
client_secret = 'ddf018ff1b3b4681878b036d6518ac29'
redirect_uri = 'http://google.com/'

# Username & Scope, and Prompt for user permission
username = ''
scope = 'user-top-read user-modify-playback-state user-read-playback-state'

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
spotifyObject = spotipy.Spotify(auth=token)

# Read user_id, song_id, listen_count
# This step might take time to download data from external sources
triplets = 'data/10000.txt'
songs_metadata = 'data/song_data.csv'

song_df_a = pandas.read_table(triplets, header=None)
song_df_a.columns = ['user_id', 'song_id', 'listen_count']
song_df_b = pandas.read_csv(songs_metadata)

song_df1 = pandas.merge(song_df_a, song_df_b.drop_duplicates(['song_id']), on="song_id", how="left")
song_df1.head()
song_df1 = song_df1.head(20000)

# Merge song title and artist_name columns to make a new column
song_df1['song'] = song_df1['title'].map(str) + " - " + song_df1['artist_name']

song_gr = song_df1.groupby(['song']).agg({'listen_count': 'count'}).reset_index()
grouped_sum = song_gr['listen_count'].sum()
song_gr['percentage'] = song_gr['listen_count'].div(grouped_sum) * 100
song_gr.sort_values(['listen_count', 'song'], ascending=[0, 1])

print("Total no of songs:", len(song_df1))
u = song_df1['user_id'].unique()
print("The no. of unique users:", len(u))

# Train data
train, test_data = train_test_split(song_df1, test_size=0.20, random_state=0)
print(train.head(5))

# Create an instance of the class
# pm = Recommenders.popularity_recommender()
# pm.create_p(train, 'user_id', 'song')
# print(pm.pop_recommendations)
# Recommended songs list for a user
# user_id1 = u[5]
# print(pm.recommend_p(user_id1))
# user_id2 = u[8]
# print(pm.recommend_p(user_id2))

is_model = Recommenders.similarity_recommender()
is_model.create_s(train, 'user_id', 'song')
#
# # Print the songs for the user
# user_id1 = u[5]
# user_items1 = is_model.get_u_items(user_id1)
# print("------------------------------------------------------------------------------------")
# print("Songs played by first user %s:" % user_id1)
# print("------------------------------------------------------------------------------------")
# for user_item in user_items1:
#     print(user_item)
# print("----------------------------------------------------------------------")
# print("Similar songs recommended for the first user:")
# print("----------------------------------------------------------------------")
# # Recommend songs for the user using personalized model
# print(is_model.recommend_s(user_id1))
#
# user_id2 = u[7]
# # Fill in the code here
# user_items2 = is_model.get_u_items(user_id2)
# print("------------------------------------------------------------------------------------")
# print("Songs played by second user %s:" % user_id2)
# print("------------------------------------------------------------------------------------")
# for user_item in user_items2:
#     print(user_item)
# print("----------------------------------------------------------------------")
# print("Similar songs recommended for the second user:")
# print("----------------------------------------------------------------------")
# # Recommend songs for the user using personalized model
# is_model.recommend_s(user_id2)
#

# Get Spotify Device ID
def get_device_id(device_type):
    device_id = ""
    # Get list of devices
    devices = spotifyObject._get('me/player/devices')['devices']
    if len(devices) == 0:
        return 1
    for device in devices:
        if device['type'] == device_type:
            return device['id']
    return 2


def play_spotify(results):
    # current_market = spotifyObject.current_user()['country']
    current_market = 'ID'
    searchResult = spotifyObject.search(results[0][1], type='track', limit=1, market=current_market)
    try:
        track_uri = searchResult['tracks']['items'][0]['uri']
    except IndexError:
        print()
        print("Song is not available on spotify")
        return

    device_id = get_device_id("Computer")
    if (device_id == 1) or (device_id == 2):
        print()
        print("Can't play song since Spotify is inactive.")
        return

    data = {'uris': [track_uri]}
    url = 'me/player/play?device_id=' + device_id
    spotifyObject._put(url, payload=data)

    print()
    print("Playing " + results[0][1] + ' on spotify')


while True:
    print('')
    print('Welcome to our Music Recommendation System')
    print('1 - Get Recommendation based on song searched')
    print('2 - Get Recommendation based on your spotify top tracks')
    print('0 - Exit')
    options = int(input('User Input: '))

    if options == 1:
        song_to_search = input('\nInput song name to get recommendation: ')
        results = is_model.similar_items([song_to_search]).to_numpy()
        it = 1
        print('\nSongs:')
        for result in results:
            print(it, result[1])
            it += 1
        play_spotify(results)

    elif options == 2:
        toptracks = spotifyObject._get('me/top/tracks?time_range=long_term')['items']
        data = []

        for tracks in toptracks:
            temp = tracks['name'] + ' - ' + tracks['artists'][0]['name']
            data.append(temp)

        results = is_model.similar_items(data).to_numpy()
        it = 1
        print('\nRecommended Songs:')
        for result in results:
            print(it, result[1])
            it += 1

        current_market = 'ID'
        searchResult = spotifyObject.search(results[0][1], type='track', limit=1, market=current_market)
        try:
            track_uri = searchResult['tracks']['items'][0]['uri']
        except IndexError:
            print()
            print("Song is not available on spotify")
            continue

        device_id = get_device_id("Computer")
        if (device_id == 1) or (device_id == 2):
            print()
            print("Can't play song since Spotify is inactive.")
            continue

        data = {'uris': [track_uri]}
        url = 'me/player/play?device_id=' + device_id
        # url = 'me/player/play'
        spotifyObject._put(url, payload=data)

        print()
        print("Playing " + results[0][1] + ' on spotify')

    else:
        sys.exit(0)