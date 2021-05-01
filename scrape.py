import requests
import regex
from bs4 import BeautifulSoup
import cx_Oracle

# dsn_tns = cx_Oracle.makedsn(r'DESKTOP-40182OD', '1521', service_name='XE') # if needed, place an 'r' before any parameter in order to address special characters such as '\'.
conn = cx_Oracle.connect('zach', 'password', "localhost/orclpdb1") # if needed, place an 'r' before any parameter in order to address special characters such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

# c = conn.cursor()
# c.execute('select * from database.table') # use triple quotes if you want to spread your query across multiple lines
# for row in c:
#     print (row[0], '-', row[1]) # this only shows the first two columns. To add an additional column you'll need to add , '-', row[2], etc.
# #conn.close()
num_reviews = 3

# How to handle different types of people

# # TV SHOW -----------------------
def scrapeTVShow(imdbId):
    # Creating the request
    headers = {"Accept-Encoding": "identity"}
    page = requests.get(f"https://www.imdb.com/title/{imdbId}", headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    print("\n-----------------------\n")

    # TV show title
    try: 
        title = soup.select_one(".title_wrapper h1")
        print(f"Title: {title.text}")
    except:
        print(f'ERROR: TV Show Title of {imdbId}')

    # TV show genre
    try: 
        print('Genres: ', end='')
        for genre in soup.select(".title_wrapper .subtext a:not(:last-child)"):
            txt = genre.text.strip()
            print(txt, end=', ')
    except:
        print(f'ERROR: TV Show genres of {imdbId}')
    print("\n\n")

# # MOVIE -----------------------
def scrapeMovie(imdbId):
    # Creating the request
    headers = {"Accept-Encoding": "identity"}
    page = requests.get(f"https://www.imdb.com/title/{imdbId}", headers=headers)
    reviews_page = requests.get(f"https://www.imdb.com/title/{imdbId}/reviews", headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    review_soup = BeautifulSoup(reviews_page.text, "html.parser")

    print("\n-----------------------\n")

    # Movie title
    try: 
        title = soup.select_one(".title_wrapper h1").text
        print(f"Title: {title}")
    except:
        print(f'ERROR: Movie Title of {imdbId}')

    # Movie runtime
    try: 
        runtime = soup.select_one(".title_wrapper .subtext time").text.strip()
        print(f"Runtime: {runtime}")
    except:
        print(f'ERROR: Movie Runtime of {imdbId}')


    # Movie release date
    try: 
        release_date = soup.select_one(".title_wrapper .subtext a:last-child").text.strip()
        print(f"Release date: {release_date}")
    except:
        print(f'ERROR: Movie Release Date of {imdbId}')

    # Movie plot keywords
    try: 
        print("Plot Keywords: ", end="")
        for keyword in soup.select("#main_bottom #titleStoryLine .see-more > a span"):
            print(keyword.text, end=", ")
        print("\n")
    except:
        print(f'ERROR: Movie Plot Keywords of {imdbId}')

    try: 
        print('Reviews: ', end="")
        i = 0
        for review in review_soup.select("#main .lister-list .imdb-user-review:not(.with-spoiler)"):
            if (i >= num_reviews): 
                break

            username = review.select_one(".display-name-link a").text 
            stars = review.select_one(".rating-other-user-rating span:not(.point-scale)").text
            publish_date = review.select_one(".review-date").text
            content = review.select_one(".content .text").text 
            num_votes_raw = review.select_one(".actions").text.strip()

            num_votes_with_comma = regex.search(r'(\d|,)+', num_votes_raw)[0]
            num_votes = num_votes_with_comma.replace(",", "")

            print(f'Username: {username}')
            print(f'Stars: {stars}')
            print(f'Publish Date: {publish_date}')
            print(f'Content: {content}')
            print(f'Number of votes: {num_votes}')
            print('\n')

            i+=1
    except:
        print(f'ERROR: Movie Reviews of {imdbId}')

    print("\n\n")

# # ACTOR -----------------------
def scrapeActor(imdbId): 
    # Creating the request
    headers = {"Accept-Encoding": "identity"}
    page = requests.get(f"https://www.imdb.com/name/{imdbId}", headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    print("\n-----------------------\n")

    # Actor name
    try: 
        name = soup.select_one(".name-overview-widget__section .header span")
        [fname, lname] = regex.split(' ', name.text, 1)
        print("First name:", fname)
        print("Last name:", lname)
    except:
        print(f'ERROR: Name of {imdbId}')

    # Actor birthplace
    # @TASK: Split into location and country
    try: 
        birthplace = soup.select_one('#name-born-info > a')
        print("Birthplace:", birthplace.text)
    except:
        print(f'ERROR: Birthplace of {imdbId}')

    # Actor birthday
    try: 
        birthday = soup.select_one('#name-born-info time')
        print("Birthday:", birthday["datetime"])
    except:
        print(f'ERROR: Birthday of {imdbId}')

    # Known for
    print("Known For:", end=" ")
    try: 
        for movie in soup.select("#knownfor .knownfor-title .knownfor-title-role a"):
            print(movie["title"], end=", ")
    except:
        print(f'ERROR: Known for of {imdbId}')
    print("\n\n")

# # # MAIN -----------------------
# # Scrape Actors
# actor_file = open("people.txt", "r")
# for actor in actor_file: 
#     scrapeActor(actor.strip())
# actor_file.close()

# # Scrape TV Shows
# tv_show_file = open("tv_shows.txt", "r")
# for show in tv_show_file: 
#     scrapeTVShow(show.strip())
# tv_show_file.close()

# Scrape Movies
# movie_file= open("movies.txt", "r")
# for movie in movie_file: 
#     scrapeMovie(movie.strip())
# movie_file.close()
