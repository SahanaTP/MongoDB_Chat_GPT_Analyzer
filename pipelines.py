
# pipelines to get the query results, add your pipeline here
query_pipeline = {
    "get_most_viral_tweet": [
        {
            "$match":
                {
                    "Tweettext": {'$regex': 'chatgpt', "$options": 'i'}
                }
        },
        {
            "$addFields": {
                "viralcount": {
                    "$add": ["$replyCount", "$retweetCount", "$likeCount", "$quoteCount"]
                }
            }
        },
        {
            "$sort": {"viralcount": -1}
        },
        {
            "$limit": 1
        }
    ],
    "most_used_hashtag":
        [
            {
                "$group":
                    {
                        "_id": "$hashtag",
                        "NumberOfTimesUsed": {"$sum": 1}
                    }
            },
            {
                "$sort": {"NumberOfTimesUsed": -1}
            },
            {
                "$limit": 10
            }
        ],
    "most_used_source":
        [
            {
                "$group":
                    {
                        "_id": "$Used_source",
                        "NumberOfTimesUsed": {"$sum": 1}
                    }
            },
            {
                "$sort": {"NumberOfTimesUsed": -1}
            },
            {
                "$limit": 10
            }
        ],
    "most_mentioned_user": [
        {
            "$group":
                {
                    "_id": "$username",
                    "totalNumberOfTweets": {"$sum": 1}
                }
        },
        {
            "$sort": {"totalNumberOfTweets": -1}
        },
        {
            "$limit": 10
        }
    ],
    "most_actv_usrs_in_desc_order":
        [
            {
                "$group":
                    {
                        "_id": "$username",
                        "totalNumberOfTweets": {"$sum": 1}
                    }
            },
            {
                "$sort": {"totalNumberOfTweets": -1}
            },
            {
                "$limit": 10
            }
        ],
    "most_liked_tweet_abt_chatgpt":
        [
            {
                "$match":
                    {
                        "Tweettext": {'$regex': 'chatgpt', "$options": 'i'}
                    }
            },
            {
                "$sort":
                    {
                        "likeCount": -1
                    }
            },
            {
                "$limit": 1
            }
        ],
    "most_used_media_type": [
        {
            "$group":
                {
                    "_id": "$mediaType",
                    "NumberOfTimesUsed": {"$sum": 1}
                }
        },
        {
            "$sort": {"NumberOfTimesUsed": -1}
        }
    ],
    "users_with_more_No_of_retweets":
        [
            {
                "$group":
                    {
                        "_id": "$username",
                        "retweetCount":
                            {
                                "$sum": "$retweetCount"
                            }
                    }
            },
            {
                "$sort":
                    {
                        "retweetCount": -1
                    }
            },
            {
                "$limit": 10
            }
        ],
    "most_used_language":
        [
            {
                "$group":
                    {
                        "_id": "$Lang",
                        "totalNumberOfTweets": {"$sum": 1}
                    }
            },
            {
                "$sort": {"totalNumberOfTweets": -1}
            }
        ],
    "number_of_Tweets_on_ChatGPT":
        [
            {
                "$match":
                    {
                        "Tweettext": {'$regex': 'chatgpt', "$options": 'i'}
                    }
            },
            {
                "$count": "num_of_tweets_on_chatgpt"
            }
        ],
    "most_retweeted_in_each_lang":
        [
            {
                "$sort":
                    {
                        "retweetCount": 1,
                    }
            },
            {
                "$group":
                    {
                        "_id": "$Lang",
                        "Tweetid": {"$last": "$Tweetid"},
                        "Tweettext": {"$last": "$Tweettext"},
                        "username": {"$last": "$username"},
                        "retweetCount": {"$last": "$retweetCount"}
                    }
            },
            {
                "$sort":
                    {
                        "retweetCount": -1,
                    }
            },
        ],
    "number_of_tweets_in_a_day":
        [
            {
                "$group":
                    {
                        "_id":
                            {
                                "$dateToString": {"format": "%Y-%m-%d", "date": "$createdtime"}
                            },
                        "tweet_count": {"$sum": 1}
                    }
            },
            {
                "$project":
                    {
                        "_id": 0,
                        "tweeted_date": "$_id",
                        "tweet_count": 1
                    }
            },
            {
                "$sort":
                    {
                        "tweeted_date": 1
                    }
            }
        ],
    "most_retweeted_tweet_with_the_comments":
        [
            {
                "$project":
                    {
                        "Tweetid": 1,
                        "Tweettext": 1,
                        "username": 1,
                        "quoteCount": 1
                    }
            },
            {
                "$sort": {"quoteCount": -1}
            },
            {
                "$limit": 10
            }
        ]
}
