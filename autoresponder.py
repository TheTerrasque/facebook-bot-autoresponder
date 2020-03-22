# Need more info? Check out the blogpost:
# how-to-make-a-bot-that-automatically-replies-to-comments-on-facebook-post

"""
NEED MORE INFO? CHECK OUT THE BLOGPOST
https://vandevliet.me/bot-automatically-responds-comments-facebook/
"""

from time import sleep
from datetime import datetime
import facebook

from lib.settings import get_settings
from lib.db import FacebookComment, FacebookReply

SETTINGS = get_settings()

APP_ID = SETTINGS["facebook"]["app"]["app_id"]
APP_SECRET = SETTINGS["facebook"]["app"]["app_secret"]

PAGE_ID = SETTINGS["facebook"]["app"]["page_id"]
POST_ID_TO_MONITOR = SETTINGS["facebook"]["app"]["post_id_to_monitor"]
LONG_LIVED_ACCESS_TOKEN = SETTINGS["facebook"]["app"]["long_lived_access_token"]

COMBINED_POST_ID_TO_MONITOR = '%s_%s' % (PAGE_ID, POST_ID_TO_MONITOR)

def comment_on_comment(graph, reply):
    print("Let's comment!")
    # like the comment
    #graph.put_like(object_id=comment_id)

    graph.put_object(parent_object=reply.postid, 
        connection_name='comments',
        message=reply.message)
    
    reply.responded = datetime.utcnow()
    reply.save()


def handle_comments(comments):
     for comment in comments['data']:
            if not FacebookComment.get(FacebookComment.postid == comment['id']):
                FacebookComment.create(
                    postid=comment['id'], 
                    added=datetime.utcnow(),
                    fromname = comment['from']['name'],
                    fromid = comment['from']['id'],
                    message = comment['message'],
                    appid = APP_ID
                )


def monitor_fb_comments():
    # create graph
    graph = facebook.GraphAPI(LONG_LIVED_ACCESS_TOKEN)
    # that infinite loop tho
    while True:
        print('I spy with my little eye...🕵️ ')
        # get the comments
        comments = graph.get_connections(COMBINED_POST_ID_TO_MONITOR,
                                         'comments',
                                         order='chronological')

        handle_comments(comments)

        # while there is a paging key in the comments, let's loop them and do exactly the same
        # if you have a better way to do this, PRs are welcome :)
        while 'paging' in comments:
            comments = graph.get_connections(COMBINED_POST_ID_TO_MONITOR,
                                             'comments',
                                             after=comments['paging']['cursors']['after'],
                                             order='chronological')
            handle_comments(comments)

        for reply in FacebookReply.select().where(FacebookReply.responded == None & FacebookReply.appid == APP_ID):
            comment_on_comment(reply)
        sleep(5)

# started at the bottom, etc
if __name__ == '__main__':
    monitor_fb_comments()
