import requests
from bs4 import BeautifulSoup

# # # TV SHOW
# # Creating the request
# headers = {"Accept-Encoding": "identity"}
# page = requests.get("https://www.imdb.com/title/tt0903747/", headers=headers)
# soup = BeautifulSoup(page.text, "html.parser")

# # TV show title
# for title in soup.select(".title_wrapper h1"):
#     print(title.text)

# # TV show release date
# for runtime in soup.select(".title_wrapper .subtext a:not(.title_wrapper .subtext a:last-child)"):
#     txt = runtime.text.strip()
#     print(txt)


# # # MOVIE
# # Creating the request
# headers = {"Accept-Encoding": "identity"}
# page = requests.get("https://www.imdb.com/title/tt0371746/", headers=headers)
# soup = BeautifulSoup(page.text, "html.parser")

# # Movie title
# for title in soup.select(".title_wrapper h1"):
#     print(title.text)

# # Movie runtime
# for runtime in soup.select(".title_wrapper .subtext time"):
#     txt = runtime.text.strip()
#     print(txt)

# # Movie release date
# for release_date in soup.select(".title_wrapper .subtext a:last-child"):
#     txt = release_date.text.strip()
#     print(txt)

# # Movie review
# for review in soup.select("#titleUserReviewsTeaser .user-comments"):
#     # username = review.select("span .comment-meta a").text
#     # publish date
#     # number votes
#     # stars = review.select(".tinystarbar")["title"]
#     title = review.select("span strong").text
#     description = review.select("span span p").text
#     print(title, description, username, stars)


# # Movie plot keywords
# for keyword in soup.select("#main_bottom #titleStoryLine .see-more > a span"):
#     print(keyword.text)


# # ACTOR
# Creating the request
headers = {"Accept-Encoding": "identity"}
page = requests.get("https://www.imdb.com/name/nm0000375", headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

print("\n-----------------------\n")

# Actor name
for name in soup.select(".name-overview-widget__section .header span"):
    print("Name: ", name.text)

# Actor birthplace
for birthplace in soup.select("#name-born-info > a"):
    print("Birthplace: ", birthplace.text)

# Actor birthday
for birthday in soup.select("#name-born-info time"):
    print("Birthday: ", birthday["datetime"])

print("Known For:", end=" ")
for movie in soup.select("#knownfor .knownfor-title .knownfor-title-role a"):
    print(movie["title"], end=", ")
print("\n\n")
