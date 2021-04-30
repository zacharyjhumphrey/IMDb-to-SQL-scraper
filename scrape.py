import requests
import regex
from bs4 import BeautifulSoup

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
    soup = BeautifulSoup(page.text, "html.parser")

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


    # Movie review
    try: 
        print("Plot Keywords: ", end="")
        for keyword in soup.select("#main_bottom #titleStoryLine .see-more > a span"):
            print(keyword.text, end=", ")
        print("\n")
    except:
        print(f'ERROR: Movie Plot Keywords of {imdbId}')
    for review in soup.select("#titleUserReviewsTeaser .user-comments"):
        print('found review')
        # username = review.select("span .comment-meta a").text
        # publish date
        # number votes
        # stars = review.select(".tinystarbar")["title"]
        # title = review.select("span strong").text
        # description = review.select("span span p").text
        # print(title, description, username, stars)

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
    # @TASK: Needs to be split up into city, state and country
    # Examples: 
    # Manhattan, New York City, New York, USA
    # Melbourne, Victoria, Australia
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

# # MAIN -----------------------
# # Scrape Actors
# actor_file = open("actors.txt", "r")
# for actor in actor_file: 
#     scrapeActor(actor.strip())
# actor_file.close()

# # Scrape TV Shows
# tv_show_file = open("tv_shows.txt", "r")
# for show in tv_show_file: 
#     scrapeTVShow(show.strip())
# tv_show_file.close()

# Scrape Movies
movie_file= open("movies.txt", "r")
for movie in movie_file: 
    scrapeMovie(movie.strip())
movie_file.close()
