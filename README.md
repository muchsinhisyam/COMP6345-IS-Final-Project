<p align="center"><img src="https://i.pinimg.com/originals/0f/60/19/0f6019e15f1d8ae07e7e8ea16d242676.png" width="400"></p>

## About Us (Developers)

This project was made for COMP6345 Intelligent System Class project. 
Group members (L4AC/Group 8):

- Alifio Rasyid - 2201798295 [(Github)](https://github.com/alibanana)
- Jason Sianandar - 2201796440 [(Github)](https://github.com/ExtGmrJasonZ)
- Muchsin Hisyam - 2201797430 [(Github)](https://github.com/muchsinhisyam)

## About This Project
We build a music recommendation system using Python Machine Learning based on user's input, user's Spotify preferences data (e.g. user's most played song on Spotify), or most popular songs on the datasets. After the system recommend

## Packages and Libraries used
- ### Numpy:
Numpy is a Python library used for working with arrays. It also has functions for working in domain of linear algebra, fourier transform, and matrices.
- ### Pandas:
Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language.
- ### Sklearn:
Sklearn is a set of python modules for machine learning and data mining.
- ### Spotipy:
Spotipy is an API Library of Spotify app.

## Algorithms used:

- ### Content-Based Recommendation Systems (CBRS)
Content-Based Recommendation Systems is a method or algorithm recommends items based on its features and the similarity between elements of other items. Assume a user has already seen a movie from the genre of Comedy, CBRS will recommend movies that also belong to the Comedy genre.
- ### Collaborative-Filtering Recommendation System (CFRS)
Collaborative-Filtering Recommendation System is a method or algorithm recommends items similar to what the user has already chosen. We are going to use the Pearson Correlation to calculate the relationship between similar tracks.


## Datasets Links:

- [https://static.turi.com/datasets/millionsong/10000.txt](https://static.turi.com/datasets/millionsong/10000.txt)
- [https://static.turi.com/datasets/millionsong/song_data.csv](https://static.turi.com/datasets/millionsong/song_data.csv)

## Features

- Recommend songs based on user's input.
- Recommend songs based on user's Spotify preferences data (e.g. user's most played song on Spotify).
- Recommend songs based on popularity in the datasets data.

## How Our Program Works

1. So we have 2 datasets, the 1st one contains of user_id. song_id, and listen_count. The 2nd one is the metadata such as song name, artist.
2. We merge the both datasets.
3. So we take 20k songs out of 2M songs from datasets
4. Since we have a bunch of user's data, we used Collaborative Filtering Recommendation Systems in order to search the similar songs in the dataset. 
5. So, we provide 2 options to generate the song recommendation. 1st one is by user's input (input Song Name - Artist Name), the 2nd one is from user's Spotify preferences (user's most played song on spotify).
6. So if user choose option 1, the program compare the 'input_song' from the user input with the merged dataset, and give the recommendation songs based on the results of the Collaborative Filtering. 
7. If the user choose option 2, the program compare the spotify preferences (user's most played song on spotify)  with the merged dataset, and give the recommendation songs based on the results of the Collaborative Filtering.
8. Then in both options, the top  recommended song will be automaticaly played in spotify (if the spotify active, otherwise the program will print 'Spotify is inactive').

## Demo Video (YouTube):
[https://youtu.be/guNUF8gkDIM](https://youtu.be/guNUF8gkDIM)
