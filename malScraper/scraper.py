from lxml import html
from bs4 import BeautifulSoup
import urllib.request, re
import datetime
#import requests

ANIME_URL = 'https://myanimelist.net/anime.php?q='
TOP_URL = 'https://myanimelist.net/topanime.php'
TOP_SHORT_URL = 'https://goo.gl/kjgtTp'

class MAL(object):

    def __init__(self, title):
        try:
            # print("Starting search: " + GetTime())
            entry,title,url = self.FindAnime(title)
            # print("Completed search: " + GetTime())
            self.error = False
        except:
            self.error = True
        if not self.error:
            self.entry = entry
            self.title = title
            self.url = url
            # print("Episode search: " + GetTime())
            self.episode_count = self.EpisodeCount(entry)
            # print("Runtime search: " + GetTime())
            self.runtime = self.GetRuntime(entry)
            # print("Airdate search: " + GetTime())
            self.airdate = self.GetAirDate(entry)
            # print("Status search: " + GetTime())
            self.status = self.GetStatus(entry)
            # print("ttw search: " + GetTime())
            self.time_to_watch = self.TimeToWatch(self.episode_count, self.runtime)
            # print("Rating search: " + GetTime())
            self.user_rating = self.GetUserRating(entry)
            # print("Rank search: " + GetTime())
            self.user_rank = self.GetUserRank(entry)
            # print("Pop search: " + GetTime())
            self.user_popularity = self.GetUserPopularity(entry)
            # print("Similar search: " + GetTime())
            self.similar_shows = self.LikeShow(entry)
            # print("Compelted search: " + GetTime())
            self.studios = self.GetStudios(entry)
            self.genres = self.GetGenres(entry)
            self.episode_summary = self.GetSummary(entry)
            self.source = self.GetSource(entry)
            self.JSON = {
                'title': self.title,
                'url': self.url,
                'episode_count': self.episode_count,
                'episode_summary': self.episode_summary,
                'source': self.source,
                'runtime': self.runtime,
                'airdate': self.airdate,
                'status': self.status,
                'time_to_watch': self.time_to_watch,
                'studios': self.studios,
                'genres': self.genres,
                'user_rating': self.user_rating,
                'usr_rank': self.user_rank,
                'user_popularity': self.user_popularity,
                'similar_shows': self.similar_shows
            }

    def EpisodeCount(self, entry):
        episodes = self.FindItemInPage("Episodes:",entry)
        if episodes == "Unknown":
            return self.GetEpisodes(entry)
        return episodes
    
    def GetSummary(self, entry):
        return entry.find("span", itemprop="description").text

    def GetRuntime(self, entry):
        return self.FindItemInPage("Duration:",entry)

    def GetAirDate(self, entry):
        return self.FindItemInPage("Aired:",entry)

    def GetStatus(self, entry):
        return self.FindItemInPage("Status:",entry)

    def GetStudios(self, entry):
        return self.FindListInPage("Studios:",entry)

    def GetGenres(self, entry):
        return self.FindListInPage("Genres:",entry)

    def GetSource(self, entry):
        return self.FindItemInPage("Source:",entry)

    def GetUserRating(self, entry):
        return self.FindItemInPage("Score:",entry)

    def GetUserRank(self, entry):
        return self.FindItemInPage("Ranked:",entry)

    def GetUserPopularity(self, entry):
        self.FindItemInPage("Popularity:",entry)

    def TimeToWatch(self, episodes, runtime):
        if '/' in episodes:
            episodes = episodes.split('/')[0]
        runtime = runtime.split(' ')
        if runtime[1] == "hr.":
            eptime = int(runtime[0])*60 + int(runtime[2])
        else:
            eptime = int(runtime[0])
        totaltime = eptime * int(episodes)
        return self.FormatRuntime(totaltime)

    def LikeShow(self, entry):
        link = entry.find("div", id="horiznav_nav",style="margin: 5px 0 10px 0;")
        link = link.find("a", href=True, text="Recommendations")['href']
        soup = BeautifulSoup(self.GetPage(link),'lxml')
        ref = soup.find('div', class_="js-scrollfix-bottom-rel")
        ref2 = ref.findAll('div', style="margin-bottom: 2px;")
        msg = ''
        similar = {}
        for title in range(10):
            try:
                similar[str(ref2[title].find('a', href=re.compile('/anime/')).text)] = str(ref2[title].find('a', href=re.compile('/anime/'))['href'])
            except:
                return similar
        return similar

    def GetSpecificEpisode(self, episode):
        req = urllib.request.urlopen(self.url + '/episode/' + episode)
        soup = BeautifulSoup(req, 'lxml')
        a = soup.find(class_='pt8 pb8')
        b = a.text.split('\n')
        summary = '\n'.join(map(str.strip, b[2:]))
        air_date = soup.find("span", class_='fw-b', text='Aired: ').next_sibling
        return {
            'air_date': air_date,
            'summary': summary
        }

    ########################################################################################################################
    def FindAnime(self, title):
        search = title.replace(' ', '%20')
        # print("Starting full search: " + GetTime())
        soup = BeautifulSoup(self.GetPage(ANIME_URL+search+"&count=1"),'lxml')
        # print("Done search: " + GetTime())
        page = soup.find("a", class_='hoverinfo_trigger fw-b fl-l')
        # print("Getting specific page: " + GetTime())
        anime = BeautifulSoup(self.GetPage(page['href']),'lxml')
        # print("Done search: " + GetTime())
        return anime,anime.find("span",itemprop="name").text,page['href']

    def GetEpisodes(self, entry):
        l = entry.findAll('a', href=True)
        for url in l:
            if url.text == "Episodes":
                episodes = BeautifulSoup(self.GetPage(url['href']),'lxml')
                return episodes.find("span", class_='di-ib pl4 fw-n fs10').text.strip('(').strip(')')

    def FormatRuntime(self, runtime):
        hours, minutes = divmod(runtime,60)
        if hours > 0:
            days, hours = divmod(hours,24)
            if days > 0:
                return '{} day{}, {} hour{}, {} minute{}'.format(days, 's' if days > 1 else '', hours,
                                    's' if hours > 1 else '', minutes, 's' if ((minutes > 1) or (minutes == 0)) else '')
            else:
                return '{} hour{}, {} minute{}'.format(hours, 's' if hours > 1 else '', minutes,
                                                        's' if ((minutes > 1) or (minutes == 0)) else '')
        else:
            return '{} minute{}'.format(minutes, 's' if ((minutes > 1) or (minutes == 0)) else '')

    def GetPage(self, url):
        return urllib.request.urlopen(url)
        # return requests.get(url)

    def FindItemInPage(self, val,entry):
        item = entry.find("span", class_='dark_text', text=val)
        a = item.parent.text
        return a.split('\n')[2].strip(' ')

    def FindListInPage(self, val, entry):
        item = entry.find("span", class_='dark_text', text=val)
        a = item.parent.text
        b = a.split('\n')[2].split(', ')
        if len(b) == 1:
            b[0] = b[0].strip(' ')
        return b

    def BuildJson(self, title):
        results = {}
        soup = BeautifulSoup(self.GetPage(ANIME_URL+title+"&count=1"),'lxml')
        page = soup.find("a", class_='hoverinfo_trigger fw-b fl-l')
        anime = BeautifulSoup(self.GetPage(page['href']),'lxml')
        allItems = anime.findAll("span", class_='dark_text')
        for item in allItems:
            a = item.parent.text.split('\n')[1:3]
            if "English: " in a[0] or "Japanese: " in a[0]:
                b = a[0].split()
                a[0] = b[0]
                a[1] = ' '.join(b[1:])
            results[a[0]] = ' '.join(a[1].split())
        results['Description'] = anime.find("span", itemprop="description").text
        return results
########################################################################################################################

def GetTop(top=5):
    soup = BeautifulSoup(urllib.request.urlopen(TOP_URL),'lxml')
    shows = soup.findAll("a", class_="hoverinfo_trigger fl-l fs14 fw-b")
    top_shows = {}
    for show in range(top):
        top_shows[show+1] = {
            'title': shows[show].text,
            'url': shows[show]['href']
        }
    return top_shows

def GetTime():
    return str(datetime.datetime.now())

if __name__ == "__main__":
    new = MAL('Tiger & Bunny')
    print(new.error)
    print(new.airdate)
    print(new.episode_count)
    print(new.JSON)
