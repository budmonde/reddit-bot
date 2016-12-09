import re
import praw
from praw.models import MoreComments

USER_AGENT = "Comment Extraction (by /u/ml6867"
CLIENT_ID = "ja-KqPQt1MqfHA"
CLIENT_SECRET = "g9Fxo0qtMS_a10Hak0h-DaYKvWE"
USERNAME = "ml6867"
PASSWORD = "ml6867"

reddit = praw.Reddit(user_agent=USER_AGENT,
                     client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     username=USERNAME,
                     password=PASSWORD)


def expand(comments):
  temp = []
  for comment in comments:
    if isinstance(comment, MoreComments):
      temp.extend(expand_helper(comment))
  comments.extend(temp)
  return comments

def expand_helper(more_comment):
  assert isinstance(more_comment, MoreComments)
  comments = more_comment.comments()
  temp = []
  for i in comments:
    if isinstance(i, MoreComments):
      print "expanding"
      temp.extend(expand_helper(i))
  comments.extend(temp)
  return comments

def is_legit_comment(comment):
  if comment == "":
    #print "empty comment"
    return False
  if comment == "[deleted]":
    #print "deleted comment"
    return False
  return True

def parse_comment(comment):
  comment_ascii =  ''.join([i if ord(i) < 128 else ' ' for i in comment])
  comment_nospace = ' '.join(comment_ascii.split())
  return comment_nospace

def parse_title(title):
  title_legal = ''.join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
  return title_legal
  

k = 0
VERBOSE = False
subreddit = reddit.front.top(limit=100, time_filter='all')
for submission in subreddit:
#for submission in subreddit.top(limit=100, time_filter='all'):

  k += 1
  print "#########"
  print "###", k, "###", parse_title(submission.title)
  print "#########"

  with open("../data/" + submission.id + ".txt", "w") as f:

    all_comments = expand(submission.comments.list())

    cnt = 0
    for comment in all_comments:
      if not isinstance(comment, MoreComments):
        if is_legit_comment(parse_comment(comment.body)):
          #f.write("""str(comment.ups) + " " + """parse_comment(comment.body) + "\n")
          f.write(parse_comment(comment.body) + "\n")
          if VERBOSE:
            print parse_comment(comment.body) + "\n"
          cnt += 1
    print "#####"
    print cnt
    VERBOSE = False

