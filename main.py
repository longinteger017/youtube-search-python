from youtubesearchpython import *
import pprint as pp
import json
import collections
from collections import Counter
import logging
import threading
import time

#TODO
## GET ALL VIDEOS
# get all videos from a certain keyword
# save: title, views, published, thumbnail url,


## YOUTUBER RANKING in NICHE
# count youtuber
# calculate avg view based on all vidoes
# calculate ratio  avg views / subscriber count

def save_details(search_result):
    yt_details = {"channels":{}}

    import pdb
    # print(type(json.loads(result)))
    print("test", search_result)
    for i in search_result:
        print(i['channel']['name'])
        yt_details['channels'][i['channel']['name']] = i['channel']['name']
        # yt_details['channels'][yt_details['channels']['name']] = 1
    print(yt_details)
    return yt_details

def main2():
    '''
    Searches for all types of results like videos, channels & playlists in YouTube.
    'type' key in the JSON/Dictionary may be used to differentiate between the types of result.
    '''
    videosSearch = VideosSearch('computer science', limit=40, language='en', region='US')
    video_result = videosSearch.result(mode=ResultMode.json)
    result = json.loads(video_result)['result']

    count = collections.Counter([user['channel']['name'] for user in result])
    pp.pprint(count)

    result = json.loads(video_result)['result']
    count = collections.Counter([user['channel']['name'] for user in result])
    pp.pprint(count)
    # f = open('output.json', 'w')
    # f.write(result)

    # video = Video.get('https://www.youtube.com/watch?v=9Ov41bcjeIc', mode = ResultMode.json)
    # videoInfo = Video.getInfo('https://www.youtube.com/watch?v=9Ov41bcjeIc', mode = ResultMode.json)
    # pp.pprint(video)
    # f.write(json.dumps(video))


    # f.close()

    # save_details(result)
    # print(result)


dict_for_df = {"view_count": [], "title": [], "pub_time": [], "duration": [], "channel_name":[], "channel_id": [], "channel_link": [], "thumbnails": []}
def get_results(kw):
    search_results = []
    counter_results = Counter()
    search = VideosSearch(kw)

    # loop through pages of result of a kw
    try:
        for page in range(0,100):
            try:
                data = search.result()['result'][0]
                dict_for_df['view_count'].append(data['viewCount']['text'])
                dict_for_df['title'].append(data['title'])
                dict_for_df['pub_time'].append(data['publishedTime'])
                dict_for_df['duration'].append(data['duration'])
                dict_for_df['channel_name'].append(data['channel']['name'])
                dict_for_df['channel_id'].append(data['channel']['id'])
                dict_for_df['channel_link'].append(data['channel']['link'])
                dict_for_df['thumbnails'].append(data['thumbnails'][0]['url'])
                # print("result", pp.pprint(search.result()['result'][0]))
            except Exception as e:
                print(f"Error occured while appending data: {e}")
                print("Error occurec at data:")
                pp.pprint(data)
            search_result = search.result()['result']
            print(page, len(search_result))
            if len(search_result) > 0:
                search.next()
                search_results = search_results + search_result
                count = collections.Counter([user['channel']['name'] for user in search_results])
                # print("counter ", json.dumps(dict(count)))
                counter_results = counter_results + count
            else:
                break

        pp.pprint(dict_for_df)
        final = dict(counter_results)
        sorted_list = sorted(search_results, key=lambda d: d['channel']['name'])
        # print(dict(sorted(final.items(), key=lambda item: item[1])))
        # pp.pprint(sorted_list)
    except Exception as e:
        print(f"Error occured while looping through pages: {e}")

    return sorted_list, count, dict_for_df

def the_coordinator(kws):
    occurence_counter = Counter()
    try:
        for kw in kws:
            suggestions = Suggestions(language='en', region='US')
            suggestion_list = json.loads(suggestions.get(kw, mode=ResultMode.json))['result']
            final_list = []
            for kw_sugg in suggestion_list:
                print(kw_sugg)
                videosresults_by_kw, occurences_of_yt, dict_for_df = get_results(kw_sugg)
                final_list = final_list + videosresults_by_kw
                occurence_counter = occurence_counter + occurences_of_yt

            # print(final_list)
            counter_dict = dict(sorted(dict(occurence_counter).items(), key=lambda item: item[1]))


        f = open('output_list.json', 'w')
        f.write('[')
        for line in final_list:
            f.write(json.dumps(line))
            f.write(",")
        f.write(']')

        with open('output_dict.json', 'w') as fp:
            json.dump(counter_dict, fp)

        with open('dict_for_df.json', 'w') as fp:
            json.dump(dict_for_df, fp)
    except Exception as e:
        print(f"Error occured: {e}")

def init_logger():
    # Gets or creates a logger
    logger = logging.getLogger(__name__)

    # set log level
    logger.setLevel(logging.WARNING)

    # define file handler and set formatter
    file_handler = logging.FileHandler('main.log')
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    file_handler.setFormatter(formatter)

    # add file handler to logger
    logger.addHandler(file_handler)

    # Logs
    # logger.debug('A debug message')
    # logger.info('An info message')
    # logger.warning('Something is not right.')
    # logger.error('A Major error has happened.')
    # logger.critical('Fatal error. Cannot continue')
    return logger
def main():
    logger = init_logger()

    kws = []

    with open('keywords.txt', "r") as f:
        for line in f:
            kws.append(line)
        logger.info('Keywords have been created successfully.')
    logger.debug("start initiator")
    the_coordinator(kws)

main()