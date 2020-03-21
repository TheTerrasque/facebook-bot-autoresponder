# Need more info? Check out the blogpost:
# how-to-make-a-bot-that-automatically-replies-to-comments-on-facebook-post

"""
NEED MORE INFO? CHECK OUT THE BLOGPOST
https://vandevliet.me/bot-automatically-responds-comments-facebook/
"""

from time import sleep
import facebook

from lib.settings import get_settings

SETTINGS = get_settings()

APP_ID = SETTINGS["facebook"]["app"]["app_id"]
APP_SECRET = SETTINGS["facebook"]["app"]["app_secret"]

PAGE_ID = SETTINGS["facebook"]["app"]["page_id"]
POST_ID_TO_MONITOR = SETTINGS["facebook"]["app"]["post_id_to_monitor"]
LONG_LIVED_ACCESS_TOKEN = SETTINGS["facebook"]["app"]["long_lived_access_token"]

COMBINED_POST_ID_TO_MONITOR = '%s_%s' % (PAGE_ID, POST_ID_TO_MONITOR)

def handle_comments(comments):
     for comment in comments['data']:

            # if we can't find it in our comments database, it means
            # we haven't commented on it yet
            if not Posts().get(comment['id']):
                # comment_on_comment(graph, comment)

                # add it to the database, so we don't comment on it again
                Posts().add(comment['id'])


def monitor_fb_comments():
    # create graph
    graph = facebook.GraphAPI(LONG_LIVED_ACCESS_TOKEN)
    # that infinite loop tho
    while True:
        print('I spy with my little eye...🕵️ ')
        sleep(5)

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


# started at the bottom, etc
if __name__ == '__main__':
    monitor_fb_comments()
