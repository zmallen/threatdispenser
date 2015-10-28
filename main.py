import twitter
import config
import random
#http://stackoverflow.com/questions/17244240/getting-mentions-and-dms-through-twitter-stream-api-1-1-using-twython
auth = twitter.OAuth(
    consumer_key = config.token, 
    consumer_secret = config.secret,  
    token = config.access_token,  
    token_secret = config.access_secret 
)
t = twitter.Twitter(auth=auth)
singular = []
prepend = ['Threat', 'Cyber', 'Cloud']
with open('singular.txt', 'r') as fd:
    singular = fd.readlines()
stream = twitter.stream.TwitterStream(auth=auth,domain='userstream.twitter.com')

def is_mentioned(entities):
    for entity in entities:
        if entity['screen_name'] == 'threatdispenser':
            return True
    return False

def process(msg):
    if 'text' in msg:
        lower = msg['text'].lower()
        mentioned = is_mentioned(msg['entities']['user_mentions'])
        if mentioned and 'dispense startup' in lower:
            screen_name = msg['user']['screen_name']
            msg_id = msg['id']
            choice_prepend = random.choice(prepend)
            choice_singular = random.choice(singular).title()
            response = 'Hey @%s, I suggest: %s%s' % (screen_name,choice_prepend,choice_singular)
            t.statuses.update(status=response, in_reply_to_status_id=msg_id)

def main():
    for msg in stream.user():
        process(msg)                

if __name__=='__main__':
    main()
