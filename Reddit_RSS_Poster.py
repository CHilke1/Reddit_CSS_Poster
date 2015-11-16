## https://pythonhosted.org/feedparser/date-parsing.html
## https://github.com/reddit/reddit/wiki/API
import feedparser
import praw
import time
from appdata import OAuth, userdata
import requests
import requests.auth
import re

class Filereader(object):
	def __init__(self):
		pass

	def get_file(self, filename):			
		argfile = str(filename)
		argfile = str(filename)
		try:
			file = open(argfile, "r")
		except IOError:
			print("cannot open", argfile)
		f = file.readlines()
		file.close()
		return f

class Feed(object):
	def __init__(self, URL):
		self.f = feedparser.parse(URL)
		self.num = 0

	def get_title(self):
		return self.f.feed.title
		
	def get_description(self):
		return self.f.feed.description
		
	def get_entry_length(self):
		self.entry_length = len(self.f.entries)
		return self.entry_length
		
	def get_entry(self, index):
		feedinfo = {}
		feedinfo['title'] = self.f.entries[index].title
		feedinfo['link'] = self.f.entries[index].link
		feedinfo['description'] = self.f.entries[index].description
		feedinfo['published'] = self.f.entries[index].published
		feedinfo['published_parsed'] = self.f.entries[index].published_parsed
		feedinfo['id'] = self.f.entries[index].id
		feedinfo['id'] = self.f.entries[index].id
		feedinfo['summary'] = self.f.entries[index].summary
		return feedinfo
		
class Reddit(object):
	def __init__(self, user_agent):
		self.user_agent = user_agent
		self.CLIENT_ID = OAuth['client_id']
		self.CLIENT_SECRET = OAuth['client_secret']
		self.login = userdata['login']
		self.password = userdata['password']
		self.subreddit = "reddit_api_test"
		
	def getAccessToken(self):
		response = requests.post("https://www.reddit.com/api/v1/access_token", auth = requests.auth.HTTPBasicAuth(self.CLIENT_ID, self.CLIENT_SECRET), data = {"grant_type": "password", "username": self.login, "password": self.password}, headers = {"User-Agent": self.user_agent})
		response = dict(response.json())
		return response["access_token"]

	def getPraw(self):
		r = praw.Reddit(user_agent = self.user_agent, oauth_client_id = self.CLIENT_ID, oauth_client_secret = self.CLIENT_SECRET, oauth_redirect_uri = "http://127.0.0.1:65010/authorize_callback")
		r.set_access_credentials({'identity', 'submit', 'read'}, self.getAccessToken() )
		return r

	def submitPost(self, r, title, body):
		self.title = title
		authenticated_user = r.get_me()
		try: 
			r.submit(subreddit, title, text=body)
		except:
			print("try again later")
	
def getDate():
	return time.gmtime()
	
def stripHTML(data):
	clean = re.sub("<.*?>", "", str(data))
	return clean
	
def getFeeds():
	reader = Filereader()
	files = reader.get_file("sites.txt")
	allrss = []
	for file in files:
		print(str(file))
		rss = []
		f = Feed(file)
		rss.append(f.get_title())
		rss.append(f.get_description())
		for num in range(0, 3):
			rss.append(f.get_entry(num))
		allrss.append(rss)
	shows = (allrss)
	return shows
			
def writeFeeds(feeds):
	reddit = Reddit("Update Page 1.0 by /u/TheHipcrimeVocab")
	for feed in feeds:
		site = feed
		print(site[0] + "\n")
		print(site[1] + "\n")
		for i in range(2, 4):
			show = site[i]
			title = str(site[0]) + " " + str(show['title'])
			print(title + "\n")
			link = "[" + show['title'] + "](" + show['link'] + ")"
			description = link + " - " + stripHTML(show['summary']) + "\n"
			print(description)
			today = getDate()
			if today > show['published_parsed']:
				print("older\n")
			r = reddit.submitPost(reddit.getPraw(), title, description)
			time.sleep(660) #Reddit allows no more than 1 post every 10 minutes
def main():
	feeds = getFeeds()
	writeFeeds(feeds)

if __name__ == "__main__":
	main()
	
	