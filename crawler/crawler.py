import tweepy
import os
import json

def load_tweet_id(load_path):
    with open(load_path, 'r') as f:
        tweet_id_lst = []
        for line in f.readlines():
            tweet_id_lst += line.strip().split(',')
        print("load tweet ids in file", load_path.split('/')[-1])
        print("total number of tweets", len(tweet_id_lst))
        lookup_lst = []
        i, j = 0, 100
        while i < len(tweet_id_lst):
            lookup_lst.append(tweet_id_lst[i:j])
            i = j
            j += 100
            if j > len(tweet_id_lst):
                j = len(tweet_id_lst)
        return lookup_lst

def crawl_tweet(client, id_lst, save_path):
    tweet_fields = ['attachments', 'author_id', 'context_annotations', 'conversation_id', 'created_at', 'entities',
                    'geo', 'id', 'in_reply_to_user_id', 'lang', 'public_metrics', 'possibly_sensitive',
                    'referenced_tweets', 'reply_settings', 'source', 'text', 'withheld']
    resp = client.get_tweets(id_lst, tweet_fields=tweet_fields)
    if resp.data:
        for tweet in resp.data:
            with open(save_path + str(tweet.id) + '.json', 'w') as f:
                json.dump(tweet.data, f)
        print("number of tweets retrieved", len(resp.data))
    if resp.errors:
        print("number of errors", len(resp.errors))
    #     for error in resp.errors:
    #         print(error['title'], '-', error['detail'])

if __name__ == '__main__':
    bearer_token = 'AAAAAAAAAAAAAAAAAAAAANXSbwEAAAAAFppfS2hZqkZNRHsUKkI4O5DB6lU%3D5WDiMUPyaWje3YxErzslgazJfmDZFN1iyoAEBEyLyVdPKZm5rs'
    client = tweepy.Client(bearer_token, wait_on_rate_limit=True)

    id_load_path = ['tweet_data/train.data.txt', 'tweet_data/dev.data.txt', 'tweet_data/covid.data.txt']
    tweet_save_path = ['tweet_data/train_tweet/', 'tweet_data/dev_tweet/', 'tweet_data/covid_tweet/']
    for load_path, save_path in zip(id_load_path, tweet_save_path):
        load_path = os.path.dirname(__file__) + '/../' + load_path
        save_path = os.path.dirname(__file__) + '/../' + save_path
        lookup_lst = load_tweet_id(load_path)
        for id_lst in lookup_lst:
            crawl_tweet(client, id_lst, save_path)