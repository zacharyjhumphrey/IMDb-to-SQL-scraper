import requests
import regex
from bs4 import BeautifulSoup
import cx_Oracle
from review import Review 
from actor import Actor, Director, Writer

class Movie:
    # static
    query = []
    acts_in_movie = [] # movie id - actor id
    writes_movie = [] # movie id- writer id
    directs_movie = [] # movie id - director id
    keyword_queries = []

    # public
    id = ""
    title = ""
    runtime = ""
    release_date = ""
    keywords = []
    reviews = []
    actors = []
    writers = []
    directors = []

    num_reviews = 3

    def __init__(self, id):
        self.id = id

        self.scrape()
        self.toSQL()
        # self.printObj()

    def scrape(self):
        # Creating the request
        headers = {"Accept-Encoding": "identity"}
        page = requests.get(f"https://www.imdb.com/title/{self.id}", headers=headers)
        reviews_page = requests.get(f"https://www.imdb.com/title/{self.id}/reviews", headers=headers)
        soup = BeautifulSoup(page.text, "html.parser")
        review_soup = BeautifulSoup(reviews_page.text, "html.parser")

        # Movie title
        try:
            self.title = soup.select_one(".title_wrapper h1").text
        except Exception as err:
            print(f'ERROR: Movie Title of {self.id}')
            print(err)

        print(self.title)

        # Movie runtime
        try:
            self.runtime = soup.select_one(".title_wrapper .subtext time").text.strip()
        except Exception as err:
            print(f'ERROR: Movie Runtime of {self.id}')
            print(err)

        # Movie release date
        try:
            self.release_date = soup.select_one(".title_wrapper .subtext a:last-child").text.strip()
        except Exception as err:
            print(f'ERROR: Movie Release Date of {self.id}')
            print(err)

        # Movie plot keywords
        try:
            for keyword in soup.select("#main_bottom #titleStoryLine .see-more > a span"):
                self.keywords.append(keyword.text)
                Movie.keyword_queries.append([self.id, keyword.text])
        except Exception as err:
            print(f'ERROR: Movie Plot Keywords of {self.id}')
            print(err)

        # MOVIE CREW MEMBERS
        [directorsElem, writersElem, actorsElem] = soup.select(".plot_summary .credit_summary_item")
        
        # MOVIE ACTORS ----------------------
        for actor in actorsElem.select("a"):
            if "name" not in actor['href']:
                continue
            actor_id = actor['href'][6:15]

            Movie.acts_in_movie.append([self.id, actor_id])
            
            if actor_id not in Actor.total:
                current_actor = Actor(actor_id)
        
        # MOVIE DIRECTORS ----------------------
        for director in directorsElem.select("a"):
            if "name" not in director['href']:
                continue
            director_id = director['href'][6:15]

            Movie.directs_movie.append([self.id, director_id])

            if director_id not in Director.total:
                current_director = Director(director_id)
                self.directors.append(current_director)

        # MOVIE WRITERS ----------------------
        for writer in writersElem.select("a"):
            if "name" not in writer['href']:
                continue
            writer_id = writer['href'][6:15]

            Movie.writes_movie.append([self.id, writer_id])

            if writer_id not in Writer.total:
                current_writer = Writer(writer_id)
                self.writers.append(current_writer)

        # MOVIE REVIEWS ---------------------
        try:
            i = 0
            for review in review_soup.select("#main .lister-list .imdb-user-review:not(.with-spoiler)"):
                if (i >= self.num_reviews):
                    break
                
                # If the review does not have a star-rating, move on to the next review
                if not isinstance(review.select_one(".rating-other-user-rating span:not(.point-scale)"), str):
                    continue

                username = review.select_one(".display-name-link a").text
                stars = review.select_one(
                    ".rating-other-user-rating span:not(.point-scale)").text
                publish_date = review.select_one(".review-date").text
                content = review.select_one(".content .text").text

                num_votes_raw = review.select_one(".actions").text.strip()
                num_votes_with_comma = regex.search(r'(\d|,)+', num_votes_raw)[0]
                num_votes = num_votes_with_comma.replace(",", "")

                Review(username, self.id, publish_date, content, stars, num_votes)

                i += 1

                self.reviews.append(new_review)
        except Exception as err:
            print(f'ERROR: Movie Reviews of {self.id}')
            print(err)

    def toArray(self):
        return [self.id, self.title, self.runtime, None]

    def toSQL(self):
        Movie.query.append(self.toArray())

    def printObj(self):
        print(f'Id: {self.id}')
        print(f'Title: {self.title}')
        print(f'Release Date: {self.release_date}')
        print(f'Runtime: {self.runtime}')

        print("Keywords: ", end="")
        for keyword in self.keywords:
            print(f'{keyword}, ', end="")
        print()

        i = 1
        for review in self.reviews:
            print(f'Review {i}: ')
            review.printObj()
            i += 1
        print()

# REVIEW ---------------------------------
class Review:
    # static
    query = []

    # public
    ssn_number = 0

    def __init__(self, username, m_id, publish_date, content, stars, num_votes):
        self.movie_id = m_id
        self.ssn_number = num
        self.toSQL()
        self.username = username
        self.publish_date = publish_date 
        self.content = content
        self.stars = stars
        self.num_votes = num_votes

    def toSQL(self):
        Season.query.append([self.username, self.id, sel.fpublish_date, self.content, self.stars, self.num_votes])
