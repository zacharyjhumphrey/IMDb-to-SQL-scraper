class Review:
    username = ""
    id = ""
    publish_date = ""
    content = ""
    stars = -1
    num_votes = -1

    def __init__(self, id, publish_date, stars, content, num_votes):
        self.id = id
        self.publish_date = publish_date
        self.stars = stars
        self.content = content
        self.num_votes = num_votes

    def toSQL(self):
        print('putting object in SQL database')

    def printObj(self):
        print(f'Username: {self.username}')
        print(f'Id: {self.id}')
        print(f'Publish Date: {self.publish_date}')
        print(f'Content: {self.content}')
        print(f'Stars: {self.stars}')
        print(f'Number of votes: {self.num_votes}')
