import oauth2 as oauth
import urllib.request as urllib
import sys
import json
import statistics

# See assignment1.html instructions or README for how to get these credentials

api_key = "5HsPSR1QwNBGEm2vpvNJzv1oU"
api_secret = "XQhDaWyu0asN79AFUaEwFYfQntAXc78FLLeEjShbnit7q0aUlb"
access_token_key = "113123131-4n40UA3eR0IQHbUaMNWpjsj4PRRg7KA9yOP5gRS8"
access_token_secret = "ZeD8VQKGwoNqw0QjaxioZ5iyPI9iutzwdLgM1s3BAZTmV"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def getScoreOfText(text, scores):
    text_splitted = text.split(" ")
    total_score = 0
    for word in text_splitted:
        if word in scores:
            total_score = total_score + scores[word]
    return(total_score)

def getSentimentOfText(tweet_file):
    sent_file = open("word_sent_en.txt")
    scores = {} # initialize an empty dictionary
    for line in sent_file:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.
        #print scores.items() # Print every (term, score) pair in the dictionary
    i = 0
    sent_dict = {}
    for line in tweet_file:
        tweet = json.loads(line)
        for twtsts in tweet['statuses']:
            sent_dict[twtsts['text']] = getScoreOfText(twtsts['text'], scores)
    return sent_dict

def fetchAndSaveSamples(hashtag):
  lang = "en"
  url = "https://api.twitter.com/1.1/search/tweets.json?q=%23" + hashtag + "&result_type=recent&lang=" + lang + "&count=100"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  saida = open("twitter_out.txt", "wb")
  for line in response:
    saida.write(line)
  saida.close()
  sizeLine = len(json.loads( [line for line in open("twitter_out.txt")][0] )['statuses'])
  #print("\nsizeLine: " + str(sizeLine) + "\n")
  if sizeLine == 0:
    return False
  else:
    return True
