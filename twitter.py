from BeautifulSoup import BeautifulSoup as Soup
import urllib
import mechanize
import getpass
import cookielib
import time
import random


br = mechanize.Browser()
cj = cookielib.LWPCookieJar()


def setup_browser():
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]


def login_twitter():
	response = br.open("https://twitter.com/login?lang=en")

	username = raw_input('Username or Email: ')
	password = getpass.getpass('Password: ')
	
	br.select_form(nr=1)
	br.form['session[username_or_email]'] = username
	br.form['session[password]'] = password
	br.submit()
	
	response = br.response()

	if 'error' in response.geturl():
		print 'The username and password do not match. Please try again.'
		login_twitter()


def tweet(tweet):
	response = br.open("https://twitter.com/intent/tweet")
	br.select_form(nr=1)
	br.form['status'] = str(tweet)
	br.submit()


def fill_tweets(how_many_tweets,max_time_between_tweets):
	tweets_posted = 0

	with open('tweets.txt','r') as input:
		tweets = input.read().split('!@#$%^&*()')
		tweets = [x.strip() for x in tweets]
		tweets = filter(None, tweets)

		if(len(tweets)!=0):
			for text in tweets:
				if(tweets_posted==how_many_tweets): 
					break
				tweet(text)
				tweets_posted +=1
				print 'I just tweeted: ' + text
				if(tweets_posted!=how_many_tweets): 
					time.sleep(int(random.random()*max_time_between_tweets))
			tweets = tweets[how_many_tweets:]

			with open('tweets.txt','w') as output:
				output.write(str('!@#$%^&*()'.join(tweets).replace('amp;','')))

def scrape_for_tweets(time_to_run):
	ret = []
	for time in range(time_to_run):

		html = urllib.urlopen('http://funtweets.com/random').read()
		soup = Soup(html)

		for i in soup.findAll('article',{'class':'tweet'}):
			div = i.findAll('div',{'class':'tweet-text'})
			for each in div:
				[s.extract() for s in each('a')]
				ret.append(each.text.strip())

	with open('tweets.txt','a') as output:
		for i in ret:
			try:
				output.write(i+'!@#$%^&*()')
			except:
				pass


def main():
	scrape_for_tweets(5)
	setup_browser()
	login_twitter()
	fill_tweets(20,10)


if __name__ == '__main__':
	main()
