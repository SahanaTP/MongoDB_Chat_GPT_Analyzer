import pymongo
import pipelines
import argparse
import getpass
import sys
import signal
import pprint
import urllib

class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        values = getpass.getpass()
        setattr(namespace, self.dest, values)


def setup_args(parser):
    if not parser:
        return False
    parser.add_argument('-u', '--username', help="Host User Name", const=1, default='labproject', nargs="?", type=str)
    parser.add_argument('-p', '--password', help="Host User Password", action=Password, nargs='?', dest='password',
                        const=1, required=True)
    parser.add_argument('-d', '--database', help="DB name", const=1, default='twitterdb', nargs="?", type=str)


def make_connection_to_mongo(username, password):
    client = None
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://" + username + ":" + password + "@newcluster.shnwxo0.mongodb.net/test")
        print(client.list_database_names())
    except pymongo.errors.ConnectionFailure as e:
        print("make_connection_to_mongo: Failed to connect to the mongo db server")
        return client
    else:
        return client


def close_connection_to_mongo(client):
    try:
        client.close()
    except Exception as e:
        print("close_connection_to_mongo: Failed to close connection to mongo db server")
    else:
        print("close_connection_to_mongo: Successfully closed connection to mongo db server")


def create_index(collection_name, field_name):
    try:
        col = db[collection_name]
        index_key = col.create_index(field_name)
        print(f'created index on {collection_name} collection - {index_key}'.format(collection_name=collection_name,
                                                                                    index_key=index_key))
    except Exception as e:
        print("create_index: Failed to create index on {collection_name}".format(collection_name=collection_name))
        return False
    return True


def create_index_in_mongo(idx_dict):
    for key, value in idx_dict.items():
        rc = create_index(key, value)
        if not rc:
            return False

    return True


def print_docs(documents):
    for x in documents:
        pprint.pprint(x)


def run_mql_aggregate_queries(collection_name, pipeline):
    try:
        col = db[collection_name]
        docs = col.aggregate(pipeline)
        print_docs(docs)
    except Exception as e:
        print("run_mql_aggregate_queries: Failed to to run")
        return False
    else:
        return True


def get_most_viral_tweet():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("get_most_viral_tweet")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_most_used_hashtags():
    col = "hashtags"
    pipeline = pipelines.query_pipeline.get("most_used_hashtag")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_most_used_source():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("most_used_source")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_most_mentioned_user():
    col = "user_mentions"
    pipeline = pipelines.query_pipeline.get("most_mentioned_user")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_most_actv_usrs_in_desc_order():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("most_actv_usrs_in_desc_order")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_most_liked_tweet_abt_chatgpt():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("most_liked_tweet_abt_chatgpt")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_most_used_media_type():
    col = "media"
    pipeline = pipelines.query_pipeline.get("most_used_media_type")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_users_with_more_No_of_retweets():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("users_with_more_No_of_retweets")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_most_used_language():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("most_used_language")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_number_of_Tweets_on_ChatGPT():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("number_of_Tweets_on_ChatGPT")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_most_retweeted_in_each_lang():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("most_retweeted_in_each_lang")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True


def get_number_of_tweets_in_a_day():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("number_of_tweets_in_a_day")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True

def get_most_retweeted_tweet_with_the_comments():
    col = "tweets"
    pipeline = pipelines.query_pipeline.get("most_retweeted_tweet_with_the_comments")
    rc = run_mql_aggregate_queries(col, pipeline)
    if not rc:
        return False

    return True

def _chatgpt_exit():
    pass


def method_help():
    print("\n")
    print("----------------------------------------")
    print("    method_id        |  method_type")
    print("----------------------------------------")
    for key, value in method_callback.items():
        print("         {idx}           | {help} ".format(idx=key, help=value.get('help')))
    print("----------------------------------------")
    print("\n")


method_callback = \
    {
        '1': {'func_p': get_most_viral_tweet, 'help': 'Get most viral tweet'},
        '2': {'func_p': get_most_used_hashtags, 'help': 'Get most used hashtags'},
        '3': {'func_p': get_most_used_source, 'help': 'Get most used source'},
        '4': {'func_p': get_most_mentioned_user, 'help': 'Get most mentioned user'},
        '5': {'func_p': get_most_actv_usrs_in_desc_order, 'help': 'Get most active users in descending order'},
        '6': {'func_p': get_most_liked_tweet_abt_chatgpt, 'help': 'Get most liked tweet about chatgpt'},
        '7': {'func_p': get_most_used_media_type, 'help': 'Get most used media type'},
        '8': {'func_p': get_users_with_more_No_of_retweets, 'help': 'Get Users with more No of retweets'},
        '9': {'func_p': get_most_used_language,
              'help': 'Get most used language to tweet about chat GPT '},
        '10': {'func_p': get_number_of_Tweets_on_ChatGPT, 'help': 'number of Tweets on Chat GPT'},
        '11': {'func_p': get_most_retweeted_in_each_lang, 'help': 'Get most retweeted tweet in each language'},
        '12': {'func_p': get_number_of_tweets_in_a_day, 'help': 'Get number of tweets in a day on ChatGpt'},
        '13': {'func_p': get_most_retweeted_tweet_with_the_comments,
               'help': 'Get most retweeted tweet with the comments'},

        # Dummy exit option
        'exit': {'func_p': _chatgpt_exit, 'help': 'Exits program'}
    }


def _sjsu_chatgpt_analyzer(args):
    global db
    number_of_queries = 0

    client = make_connection_to_mongo(args.username, urllib.parse.quote( args.password))
    if not client:
        print("Failed to make connection to mongo server")
        sys.exit(0)

    db = client[args.database]

    def signal_handler(sig, frame):
        if client:
            close_connection_to_mongo(client)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # create index on popular fields
    col_field_idx_dict = {"tweets": "Tweetid", "media": "Tweetid", "hashtags": "Tweetid", "users": "username",
                          "user_mentions": "Tweetid"}
    create_index_in_mongo(col_field_idx_dict)

    while True:
        method_help()
        method_name = input("Enter the method_name: ")
        if method_name == 'exit':
            break
        elif method_name == "":
            pass
        elif (method_callback.get(method_name) and
              method_callback.get(method_name).get('func_p') and
              method_name != 'exit'):
            print(" ##################################### {name} ##################################### \n".
                  format(name=method_callback.get(method_name).get('help')))

            rc = method_callback[method_name]['func_p']()
            print("#" * 100)
            if not rc:
                print("Failed to execute method_name {}".format(method_name))
        else:
            print("Invalid option {}".format(method_name))
        number_of_queries += 1

    close_connection_to_mongo(client)
    print("Thank you for using ChatGpt Analyzer! Number of queries executed {}".format(number_of_queries))


def run_mql_aggregate_queries(collection_name, pipeline):
    try:
        col = db[collection_name]
        docs = col.aggregate(pipeline)
        print_docs(docs)
    except Exception as e:
        print("run_mql_aggregate_queries: Failed to to run")
        return False
    else:
        return True


if __name__ == "__main__":
    # username = "sahanatp"
    # password = "Welcome%40123"
    parser = argparse.ArgumentParser(description='Welcome to SJSU ChatGpt Analyzer')
    setup_args(parser)
    args = parser.parse_args()


    _sjsu_chatgpt_analyzer(args)
