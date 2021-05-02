import requests
import regex
from bs4 import BeautifulSoup
import cx_Oracle
from actor import Actor

class TVShow: 
    # static 
    query = []
    acts_in_tv = []
    genre_queries = []

    # public 
    id = ""
    title = ""
    genres = []
    num_actors = 3

    def __init__(self, id): 
        self.id = id

        self.scrape()
        self.toSQL()
        # self.printObj()

    def toArray(self):
        return [self.id, self.title]

    def toSQL(self):
        self.query.append(self.toArray())

    def scrape(self):
        # Creating the request
        headers = {"Accept-Encoding": "identity"}
        page = requests.get(
            f"https://www.imdb.com/title/{self.id}", headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        print("\n-----------------------")

        # TV show title
        try:
            self.title = soup.select_one(".title_wrapper h1").text.strip()
        except Exception as err:
            print(f'ERROR: TV Show Title of {self.id}')
            print(err)
            
        print(self.title)

        # TV show genres
        try:
            for genre in soup.select(".title_wrapper .subtext a:not(:last-child)"):
                txt = genre.text.strip()
                TVShow.genre_queries.append([self.id, txt])
        except Exception as err:
            print(f'ERROR: TV Show genres of {self.id}')
            print(err)
        
        # TV Actors -----------------------
        i = 0
        for actor in soup.select("#titleCast td:not(.primary_photo) a"):
            if i > 3:
                break
            if "name" not in actor['href']:
                continue 
        
            actor_id = actor['href'][6:15]
            TVShow.acts_in_tv.append([self.id, actor_id])

            if actor_id not in Actor.total:
                current_actor = Actor(actor_id)

            i+=1
    
    def printObj(self): 
        print(f"Title: {self.title}")

        print('Genres: ', end='')
        for genre in self.genres: 
            print(genre, end=", ")
        print()

        print()

# SEASON ---------------------------------
class Season:
    # static 
    query = []

    # public 
    ssn_number = 0

    def __init__(self, num):
        self.ssn_number = num
        self.toSQL()

    def toSQL(self):
        Season.query.append((self.id, ssn_number))

    
