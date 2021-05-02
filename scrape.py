import requests
import regex
from bs4 import BeautifulSoup
import cx_Oracle
from movie import Movie, Review
from tv_show import TVShow, Season
from actor import Actor, Director, Writer

lib_dir = r"C:\instantclient_19_10"
test_movies = 1

try:
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    print("Error connecting: cx_Oracle.init_oracle_client()")
    print(err)
    sys.exit(1)

conn = cx_Oracle.connect('system', 'raspberry1', "localhost/xe")

c = conn.cursor()

# # ------------- TEST ---------------
# # Scrape TV Shows
# tv_show_file = open("tv_shows.txt", "r")
# for show in tv_show_file: 
#     TVShow(show.strip())
# tv_show_file.close()
TVShow('tt2403776')
# Movie('tt4154796')
# # Scrape Movies
# movie_file= open("movies.txt", "r")
# for movie in movie_file: 
#     Movie(movie.strip())
# movie_file.close()

print('Number of tuples:')
print(len(TVShow.query) + len(Movie.query) + len(Actor.query) +
      len(Director.query) + len(Writer.query) + len(Review.query) + len(Actor.known_for_queries) + len(Movie.keyword_queries) + len(TVShow.genre_queries) + len(Season.query) + len(Movie.acts_in_movie) + len(TVShow.acts_in_tv) + len(Movie.writes_movie) + len(Movie.directs_movie))

# # Movies, tv shows, actors, writers and directors
c.executemany("INSERT INTO tv_show VALUES(: id, : title)",
              TVShow.query, batcherrors=True)
c.executemany("INSERT INTO movie VALUES(: id, : title, : runtime, : rdate)",
              Movie.query, batcherrors=True)
c.executemany("INSERT INTO actor VALUES(:id, :wid, :did, :fname, :lname, :bdate, :city, :country, :starmeter)", Actor.query)
c.executemany(
    "INSERT INTO director VALUES(:id, :wid, :did, :fname, :lname, :bdate, :city, :country, :starmeter)", Director.query)
c.executemany(
    "INSERT INTO writer VALUES(:id, :wid, :did, :fname, :lname, :bdate, :city, :country, :starmeter)", Writer.query)
c.executemany(
    "INSERT INTO review VALUES(: username, : movieid, : publishdate, : content, : stars, : numvotes)", Review.query)


# Keywords, genres and known_for
c.executemany("INSERT INTO known_for VALUES(:1, :2)", Actor.known_for_queries)

c.executemany("INSERT INTO plot_keywords VALUES(:a, :b)", Movie.keyword_queries)

c.executemany("INSERT INTO genre VALUES(:tvid, :gen)", TVShow.genre_queries)
c.executemany("INSERT INTO season VALUES(:c, :d)", Season.query)


# Person to person relationships
c.executemany("UPDATE actor SET w_id=: e WHERE imdb_id=: f", Actor.isWriter)
c.executemany("UPDATE writer SET a_id=: h WHERE imdb_id=: i", Writer.isActor)

c.executemany("UPDATE actor SET d_id=:j WHERE imdb_id=:k", Actor.isDirector)
c.executemany("UPDATE director SET a_id=:l WHERE imdb_id=:m", Writer.isActor)

c.executemany("UPDATE writer SET d_id=:n WHERE imdb_id=:o", Actor.isWriter)
c.executemany("UPDATE director SET w_id=:z WHERE imdb_id=:y", Writer.isActor)

# M to N relationships
c.executemany("INSERT INTO acts_movie VALUES(: movieid, : actorid)",
              Movie.acts_in_movie)
c.executemany("INSERT INTO acts_tv VALUES(: movieid, : actorid)",
              TVShow.acts_in_tv)
c.executemany(
    "INSERT INTO writes_movie VALUES(: movieid, : writerid)", Movie.writes_movie)
c.executemany(
    "INSERT INTO directs_movie VALUES(: movieid, : directorid)", Movie.directs_movie)

for error in c.getbatcherrors():
    print("Error", error.message, "at row offset", error.offset)
conn.commit()

conn.close()
