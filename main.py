from youtubesearchpython import *
import pprint as pp
import json
import collections
from collections import Counter
import logging
import logging.config
import threading
import time
from datetime import datetime
import init_database as db_helper
import pandas as pd
import traceback
import re
import sys
import pdb
from multiprocessing import Pool


# TODO
## GET ALL VIDEOS
# get all videos from a certain keyword
# save: title, views, published, thumbnail url,


## YOUTUBER RANKING in NICHE
# count youtuber
# calculate avg view based on all vidoes
# calculate ratio  avg views / subscriber count

def save_details(search_result):
    yt_details = {"channels": {}}

    import pdb
    # print(type(json.loads(result)))
    print("test", search_result)
    for i in search_result:
        print(i['channel']['name'])
        yt_details['channels'][i['channel']['name']] = i['channel']['name']
        # yt_details['channels'][yt_details['channels']['name']] = 1
    print(yt_details)
    return yt_details


# def main2():
#     '''
#     Searches for all types of results like videos, channels & playlists in YouTube.
#     'type' key in the JSON/Dictionary may be used to differentiate between the types of result.
#     '''
#     videosSearch = VideosSearch('computer science', limit=40, language='en', region='US')
#     video_result = videosSearch.result(mode=ResultMode.json)
#     result = json.loads(video_result)['result']
#
#     count = collections.Counter([user['channel']['name'] for user in result])
#     pp.pprint(count)
#
#     result = json.loads(video_result)['result']
#     count = collections.Counter([user['channel']['name'] for user in result])
#     pp.pprint(count)
#     # f = open('output.json', 'w')
#     # f.write(result)
#
#     # video = Video.get('https://www.youtube.com/watch?v=9Ov41bcjeIc', mode = ResultMode.json)
#     # videoInfo = Video.getInfo('https://www.youtube.com/watch?v=9Ov41bcjeIc', mode = ResultMode.json)
#     # pp.pprint(video)
#     # f.write(json.dumps(video))
#
#     # f.close()
#
#     # save_details(result)
#     # print(result)


dict_for_df = {"view_count": [], "title": [], "pub_time": [], "duration": [], "channel_name": [], "channel_id": [],
               "channel_link": [], "thumbnails": []}


def get_results(kw, config_data):
    search_results = []
    counter_results = Counter()
    search = VideosSearch(kw)

    # loop through pages of result of a kw
    try:
        for page in range(0, config_data['limit_of_pages_per_kw']):
            try:
                if len(search.result()['result']) > 0:
                    # print("RESULT:", search.result()['result'])
                    data = search.result()['result'][0]
                    dict_for_df['title'].append(data['title'])
                    dict_for_df['channel_id'].append(data['channel']['id'])
                    dict_for_df['channel_link'].append(data['channel']['link'])
                    dict_for_df['channel_name'].append(data['channel']['name'])
                    if data['viewCount']['text'] is None:
                        dict_for_df['view_count'].append(0)
                    elif "views" in data['viewCount']['text']:
                        if data['viewCount']['text'] == "No views" or data['viewCount']['text'] == "" or \
                                data['viewCount']['text'] is None:
                            dict_for_df['view_count'].append(0)
                        else:
                            dict_for_df['view_count'].append(int(re.sub("[^0-9]", "", data['viewCount']['text'])))

                    dict_for_df['duration'].append(data['duration'])
                    dict_for_df['pub_time'].append(data['publishedTime'])
                    dict_for_df['thumbnails'].append(data['thumbnails'][0]['url'])
                    # print("result", pp.pprint(search.result()['result'][0]))
                else:
                    continue
            except Exception as e:
                print(f"Error occured while appending data: {e}")
                logging.error(f"Error occurred while scraping: {data}")
                pp.pprint(data)

            search_result = search.result()['result']
            print(page, len(search_result))

            try:
                if len(search_result) > 0:
                    search.next()
                    search_results = search_results + search_result
                    count = collections.Counter([user['channel']['name'] for user in search_results])
                    counter_results = counter_results + count
                else:
                    break
            except Exception as e:
                print("Exception while executing get_results:")
                print("-" * 60)
                traceback.print_exc(file=sys.stdout)
                print("-" * 60)
                logging.error(f"Exception while executing next(): {e}")

        final = dict(counter_results)
        sorted_list = sorted(search_results, key=lambda d: d['channel']['name'])
        # print(dict(sorted(final.items(), key=lambda item: item[1])))
        # pp.pprint(sorted_list)
    except Exception as e:
        print("Exception while executing get_results:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)
        logging.error(f"Exception while executing get_results: {e}")
        pass

    return sorted_list, count, dict_for_df


def the_coordinator(kw):
    occurence_counter = Counter()
    ############################################################
    ## INIT PHASE
    ############################################################
    with open("config.json", 'r') as configs:
        config_data = json.load(configs)

    db_conn = db_helper.create_connection(config_data['DB_PATH'])
    try:
        # multiprocessing
        suggestions = Suggestions(language='en', region='US')
        suggestion_list = json.loads(suggestions.get(kw, mode=ResultMode.json))['result']
        final_list = []

        for kw_sugg in suggestion_list:
            print(f"Suggested KW for <{kw}> ==> <{kw_sugg}>")
            videosresults_by_kw, occurences_of_yt, dict_for_df = get_results(kw_sugg, config_data)
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

        with open('count_youtuber_occurencies.json', 'w') as fp:
            json.dump(counter_dict, fp)

        # with open('dict_for_df.json', 'w') as fp:
        #     json.dump(dict_for_df, fp)

        result_df = pd.DataFrame.from_dict(dict_for_df)
        result_df.to_sql(name='coworking', if_exists='append', con=db_conn, index=False)

    except Exception as e:
        print("Exception while executing get_results:")
        print("-" * 60)
        traceback.print_exc(file=sys.stdout)
        print("-" * 60)
        logging.error(f"Error occured in the_coordinator: {e}")


def init_logger():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y--%H:%M:%S")
    filename = "logs/main_" + dt_string + ".log"
    logging.basicConfig(format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=filename,
                        level=logging.DEBUG)


def create_kw_list(kw_file):
    kw_list = []

    with open(kw_file, "r", encoding="utf-8") as f:
        for line in f:
            kw_list.append(line.strip())
        logging.info('Keywords have been created successfully.')

    return kw_list


def main():
    init_logger()
    kws = create_kw_list("keywords/keywords1.txt")
    logging.info("start initiator")

    pool = Pool(8)  # Create a multiprocessing Pool
    pool.map(the_coordinator, kws)  # process data_inputs iterable with pool
    pool.close()  # no more tasks
    pool.join()  # wrap up current tasks

    print("+" * 28)
    print("+++ FINISHED COORDINATOR +++")
    print("+" * 28)


if __name__ == '__main__':
    main()

# json.loads("/output_files/dict_for_df")
