This is a small helper program that simplifies scraping anime information from the website "myanimelist.net". The user only needs to provide the name of the anime that they would like information on and the tool will create an object full of data for the show.

The current list of data that is being stored is the following:
* Title
* URL
* Episode Count (both for completed and still airing shows)
* Runtime (runtime for each episode)
* Airdate (time when the show aired)
* Status (Completed/Airing/Not Yet Aired)
* Time to Watch (time it takes to watch the full series)
* Studios (list of studios involved in making the show)
* Genres (list of genres)
* User Rating
* User Ranking
* User Popularity
* Similar Shows (dictionary of recomended shows and their links)

I leave it up to the site to do best effort on anime matching. If a show cannot be found, an  `error` parameter will be set to true.

## Installation
Two simple ways to use this package as is:

### Install via pip
Run the following command to install to your environment (includes dependencies):
`pip install git+git://github.com/fuzzylimes/mal-scraper.git`

### Install via setup.py
* Clone the repo from github
* Navigate into the folder and run `pip install .`

## Usage
There are two main items that the package can be used for: retrieving specific infomration about a show, and collecting information about the top rated shows on the website (by its users).

### MAL Object
The primary feature of this package is the ability to scrape a bunch of information for a given show. *Currently this works ONLY for anime searches, not managa*.

#### Importing the package
The package can be imported by including like so:
```python
import malScraper as mal
```

### Creating a MAL object
To use the tool, you simply need to create a new MAL object by passing in the title of the anime you want to collect data on. So if you're trying to collect the information for 'One Punch Man', you would set a new varaible like so:
```python
search = mal.MAL('One Punch Man')
```

This will create your initial MAL object. From this point, you can either access the object's paramters directly, or you can retrieve them all at once in a JSONized format by using the .JSON value:
```python
IN [1]: print(search.JSON)
OUT[1]:
{'title': 'Tiger & Bunny', 'url': 'https://myanimelist.net/anime/9941/Tiger___Bunny', 'episode_count': '25', 'runtime': '24 min. per ep.', 'airdate': 'Apr 3, 2011 to Sep 18, 2011', 'status': 'Finished Airing', 'time_to_watch': '10 hours, 0 minutes', 'studios': ['Sunrise'], 'genres': ['Action', 'Mystery', 'Comedy', 'Super Power'], 'user_rating': '8.081 (scored by 52,114 users)', 'usr_rank': '#4602', 'user_popularity': None, 'similar_shows': {'Boku no Hero Academia': '/anime/31964/Boku_no_Hero_Academia', 'One Punch Man': '/anime/30276/One_Punch_Man', 'Samurai Flamenco': '/anime/19365/Samurai_Flamenco', 'Gatchaman Crowds': '/anime/18229/Gatchaman_Crowds', 'Darker than Black: Kuro no Keiyakusha': '/anime/2025/Darker_than_Black__Kuro_no_Keiyakusha', 'Zetman': '/anime/11837/Zetman', 'Witchblade': '/anime/935/Witchblade', 'GetBackers': '/anime/132/GetBackers', 'Heroman': '/anime/4334/Heroman', 'Ginga Kikoutai Majestic Prince': '/anime/15863/Ginga_Kikoutai_Majestic_Prince'}} 
```

The list of MAL object parameters are as follows:
```python
self.title
self.url
self.episode_count
self.runtime
self.airdate
self.status
self.time_to_watch
self.user_rating
self.user_rank
self.user_popularity
self.similar_shows
self.studios
self.genres
self.JSON 
```

#### Get Specific Episode
Once you've created a MAL object for a show, you can get info about a particular episode by using the `GetSpecificEpisode` method. Simply provide the episode number you would like more infomration on. This will return a dictionary with two values: `air_date`, the day that the episode premired, and `summary`, the summary for the specific episode. Both of these values will be filled in _if available_.

Here's an exmaple of how to use it:
```python
IN [1]: search.GetSpecificEpisode('3')
OUT[1]:
{'air_date': 'Apr 19, 2017(JST)',
 'summary': "Boruto's classmate, Metal Lee, is very diligent and is skilled at taijutsu. Unfortunately, he gets nervous easily and is unable to do his best when people are watching him. One day one of his classmates, Shikadai Nara,says something that enrages Metal, who attacks Shikadai the next day. Caught in the middle, Boruto notices that Metal's chakra is warped, just like Denki's.\n\n(Source: Crunchyroll)\n"}
```

### Get Top Rated Shows
The package also allows the user to retrieve the top rated anime. The user can either call the method without passing any parameters, or include an integer for the number of shows they'd like returned. If no value is provided, the top 5 shows will be returned.

To retrieve, use the `GetTop()` method.
```python
mal.GetTop()
or
mal.GetTop(10)
```

This will return an dictionary of show objects with `title` and `url`, like so:
```python
{1: {'title': 'Gintama.: Shirogane no Tamashii-hen', 'url': 'https://myanimelist.net/anime/36838/Gintama__Shirogane_no_Tamashii-hen'}, 2: {'title': 'Fullmetal Alchemist: Brotherhood', 'url': 'https://myanimelist.net/anime/5114/Fullmetal_Alchemist__Brotherhood'}, 3: {'title': 'Kimi no Na wa.', 'url': 'https://myanimelist.net/anime/32281/Kimi_no_Na_wa'}, 4: {'title': 'Gintama°', 'url': 'https://myanimelist.net/anime/28977/Gintama°'}, 5: {'title': 'Steins;Gate','url': 'https://myanimelist.net/anime/9253/Steins_Gate'}}
```