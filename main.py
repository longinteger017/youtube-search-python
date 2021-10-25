from youtubesearchpython import *
import asyncio
import pprint as pp
import json
import collections
import itertools
from collections import Counter

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

def get_results(kw):
    search_results = []
    counter_results = Counter()
    search = VideosSearch(kw)
    for page in range(0,1):
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

    final = dict(counter_results)
    sorted_list = sorted(search_results, key=lambda d: d['channel']['name'])
    print("11")
    print(dict(sorted(final.items(), key=lambda item: item[1])))
    # pp.pprint(sorted_list)

    return sorted_list, count

def main(kws):
    occurence_counter = Counter()
    for kw in kws:
        suggestions = Suggestions(language='en', region='US')
        suggestion_list = json.loads(suggestions.get(kw, mode=ResultMode.json))['result']
        final_list = []
        for kw_sugg in suggestion_list:
            print(kw_sugg)
            videosresults_by_kw, occurences_of_yt = get_results(kw_sugg)
            final_list = final_list + videosresults_by_kw
            occurence_counter = occurence_counter + occurences_of_yt

        print(final_list)
        counter_dict = dict(sorted(dict(occurence_counter).items(), key=lambda item: item[1]))

    f = open('output_list.json', 'w')
    f.write('[')
    for line in final_list:
        f.write(json.dumps(line))
        f.write(",")
    f.write(']')

    with open('output_dict.json', 'w') as fp:
        json.dump(counter_dict, fp)

kws1 = ['computer science','computer engineering','data engineering','software engineering',
              'programming','software engineering internship','coding','programmer beginner','data science', 'python programming']
kws = ['computer science', 'software engineering internship']

main(kws)
# get_results("computer science")
#