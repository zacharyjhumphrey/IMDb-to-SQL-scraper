import requests
import regex
from bs4 import BeautifulSoup
import cx_Oracle
from review import Review

class Actor:
    # static 
    query = []
    isWriter = []
    isDirector = []
    total = set([])  # set of actor id's
    known_for_queries = []

    # public
    fname = None
    lname = None
    birthplace = None 
    birthdate = None 
    city = None
    country = None
    known_for = [] # array of movie titles
    starmeter_rank = -1 # if null, star is not famous enough

    def __init__(self, id):
        self.id = id

        self.scrape()
        self.toSQL()

    def toArray(self):
        return [
            self.id, 
            None, # self.id if self.id in Writer.total else None,
            None, # self.id if self.id in Director.total else None, 
            self.fname, 
            self.lname, 
            None, 
            self.city, 
            self.country, 
            None
        ]

    def toSQL(self):
        if self.id in Director.total:
            Actor.isDirector.append((self.id, self.id))
            Director.isActor.append((self.id, self.id))
        elif self.id in Writer.total:
            Actor.isWriter.append((self.id, self.id))
            Writer.isActor.append((self.id, self.id))
        
        # @BUG: Logic is probably wrong here
        Actor.total.add(self.id)
        Actor.query.append(self.toArray())

    def scrape(self):
        # Creating the request
        headers = {"Accept-Encoding": "identity"}
        page = requests.get(f"https://www.imdb.com/name/{self.id}", headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        # Actor name
        try:
            name = soup.select_one("#name-overview-widget .header span")
            [self.fname, self.lname] = regex.split(' ', name.text, 1)
        except Exception as err:
            print(f'ERROR: Name of {self.id}')
            print(err)

        # Actor birthplace
        # @TASK: Split into location and country
        try:
            birthplace = soup.select_one('#name-born-info > a')
            if birthplace is not None:
                birthplace_split = birthplace.text.rsplit(', ', 1)
                self.birthplace = birthplace.text

                if len(birthplace_split) < 2:
                    country = birthplace.text
                else: 
                    [self.city, self.country] = birthplace_split
        except Exception as err:
            print(f'ERROR: Birthplace of {self.id}')
            print(err)

        # Actor birthday
        try:
            birthday = soup.select_one('#name-born-info time')
            if birthday is not None:
                self.birthdate = birthday["datetime"]
        except Exception as err:
            print(f'ERROR: Birthday of {self.id}')
            print(err)

        # Known for
        try:
            known_for = soup.select( "#knownfor .knownfor-title .knownfor-title-role a")

            if known_for is not None:
                for movie in known_for:
                    self.known_for.append(movie["title"])
                    Actor.known_for_queries.append([self.id, movie["title"]])
            
        except Exception as err:
            print(f'ERROR: Known for of {self.id}')
            print(err)
    
    def printObj(self):
        print(f'Id: {self.id}')
        print(f'First Name: {self.fname}')
        print(f'Last Name: {self.lname}')
        print(f'Birthdate: {self.birthdate}')
        print(f'Birthplace: {self.birthplace}')
        print(f'\tCity: {self.city}')
        print(f'\tCountry: {self.country}')
        print(f'Starmeter Rank: {self.starmeter_rank}')
        print()


# WRITER ------------------------------------------------------------------------
class Writer:
    # static
    query = []
    isActor = []
    isDirector = []
    total = set([])

    # public
    fname = None
    lname = None
    birthplace = None
    birthdate = None
    city = None
    country = None
    known_for = []  # array of movie titles
    starmeter_rank = -1  # if null, star is not famous enough

    def __init__(self, id):
        self.id = id

        self.scrape()
        self.toSQL()

    def toArray(self):
        return [
            self.id,
            None,  # self.id if self.id in Actor.total else None,
            None,  # self.id if self.id in Director.total else None,
            self.fname,
            self.lname,
            None,
            self.city,
            self.country,
            None
        ]

    def toSQL(self):
        if self.id in Actor.total:
            Writer.isActor.append((self.id, self.id))
            Actor.isWriter.append((self.id, self.id))
        elif self.id in Director.total:
            Writer.isDirector.append((self.id, self.id))
            Director.isWriter.append((self.id, self.id))

        # @BUG: Logic is probably wrong here
        Writer.total.add(self.id)
        Writer.query.append(self.toArray())

    def scrape(self):
        # Creating the request
        headers = {"Accept-Encoding": "identity"}
        page = requests.get(
            f"https://www.imdb.com/name/{self.id}", headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        # Actor name
        try:
            name = soup.select_one("#name-overview-widget .header span")
            [self.fname, self.lname] = regex.split(' ', name.text, 1)
        except Exception as err:
            print(f'ERROR: Name of {self.id}')
            print(err)

        # Actor birthplace
        # @TASK: Split into location and country
        try:
            birthplace = soup.select_one('#name-born-info > a')
            if birthplace is not None:
                birthplace_split = birthplace.text.rsplit(', ', 1)
                self.birthplace = birthplace.text

                if len(birthplace_split) < 2:
                    country = birthplace.text
                else:
                    [self.city, self.country] = birthplace_split
        except Exception as err:
            print(f'ERROR: Birthplace of {self.id}')
            print(err)

        # Actor birthday
        try:
            birthday = soup.select_one('#name-born-info time')
            if birthday is not None:
                self.birthdate = birthday["datetime"]
        except Exception as err:
            print(f'ERROR: Birthday of {self.id}')
            print(err)

        # Known for
        try:
            known_for = soup.select(
                "#knownfor .knownfor-title .knownfor-title-role a")

            if known_for is not None:
                for movie in known_for:
                    self.known_for.append(movie["title"])
        except Exception as err:
            print(f'ERROR: Known for of {self.id}')
            print(err)

    def printObj(self):
        print(f'Id: {self.id}')
        print(f'First Name: {self.fname}')
        print(f'Last Name: {self.lname}')
        print(f'Birthdate: {self.birthdate}')
        print(f'Birthplace: {self.birthplace}')
        print(f'\tCity: {self.city}')
        print(f'\tCountry: {self.country}')
        print(f'Starmeter Rank: {self.starmeter_rank}')
        print()


# DIRECTOR ------------------------------------------------------------------------
class Director:
    # static
    query = []
    isActor = []
    isWriter = []
    total = set([])

    # public
    fname = None
    lname = None
    birthplace = None
    birthdate = None
    city = None
    country = None
    known_for = []  # array of movie titles
    starmeter_rank = -1  # if null, star is not famous enough

    def __init__(self, id):
        self.id = id

        self.scrape()
        self.toSQL()

    def toArray(self):
        return [
            self.id,
            None, # self.id if self.id in Actor.total else None,
            None, # self.id if self.id in Writer.total else None,
            self.fname,
            self.lname,
            None,
            self.city,
            self.country,
            None
        ]

    def toSQL(self):
        if self.id in Actor.total:
            Director.isActor.append((self.id, self.id))
            Actor.isDirector.append((self.id, self.id))
        elif self.id in Writer.total:
            Director.isWriter.append((self.id, self.id))
            Writer.isDirector.append((self.id, self.id))

        # @BUG: Logic is probably wrong here
        Director.total.add(self.id)
        Director.query.append(self.toArray())

    def scrape(self):
        # Creating the request
        headers = {"Accept-Encoding": "identity"}
        page = requests.get(
            f"https://www.imdb.com/name/{self.id}", headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")

        # Actor name
        try:
            name = soup.select_one("#name-overview-widget .header span")
            [self.fname, self.lname] = regex.split(' ', name.text, 1)
        except Exception as err:
            print(f'ERROR: Name of {self.id}')
            print(err)

        # Actor birthplace
        # @TASK: Split into location and country
        try:
            birthplace = soup.select_one('#name-born-info > a')
            if birthplace is not None:
                birthplace_split = birthplace.text.rsplit(', ', 1)
                self.birthplace = birthplace.text

                if len(birthplace_split) < 2:
                    country = birthplace.text
                else:
                    [self.city, self.country] = birthplace_split
        except Exception as err:
            print(f'ERROR: Birthplace of {self.id}')
            print(err)

        # Actor birthday
        try:
            birthday = soup.select_one('#name-born-info time')
            if birthday is not None:
                self.birthdate = birthday["datetime"]
        except Exception as err:
            print(f'ERROR: Birthday of {self.id}')
            print(err)

        # Known for
        try:
            known_for = soup.select(
                "#knownfor .knownfor-title .knownfor-title-role a")

            if known_for is not None:
                for movie in known_for:
                    self.known_for.append(movie["title"])
        except Exception as err:
            print(f'ERROR: Known for of {self.id}')
            print(err)

    def printObj(self):
        print(f'Id: {self.id}')
        print(f'First Name: {self.fname}')
        print(f'Last Name: {self.lname}')
        print(f'Birthdate: {self.birthdate}')
        print(f'Birthplace: {self.birthplace}')
        print(f'\tCity: {self.city}')
        print(f'\tCountry: {self.country}')
        print(f'Starmeter Rank: {self.starmeter_rank}')
        print()
