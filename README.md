# How to run:
1. Fill the keyword lists in keywords.txt by adding them line by line
2. Run ```pip3 install -r requirements.txt```
3. Run ```python3 main.py```
4. Check database in sqlite database 'youtube_videos.db' by executing
```sqlite3 youtube_videos.db```


# TODOs
1. create a 'youtubers' table just for all youtubers where any scraped youtuber gets inserted
2. get subscriber count of youtuber in youtubers table
3. get video count of youtuber into youtubers table

4. start a jupyter notebook to apply play around with NLP on the youtuber dataset
5. start figuring out what the main niche/topic of a youtuber is by applying topic modeling
---
# [youtube-search-python](https://github.com/alexmercerind/youtube-search-python)

##### Search for YouTube videos, channels & playlists. Get video & playlist information using link. Get search suggestions.

#### WITHOUT YouTube Data API v3.

[![PyPI - Version](https://img.shields.io/pypi/v/youtube-search-python?style=for-the-badge)](https://pypi.org/project/youtube-search-python)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/youtube-search-python?label=DOWNLOADS&style=for-the-badge)](https://pypi.org/project/youtube-search-python)

## Installing

```bash
pip3 install youtube-search-python
```

</details>

## License

MIT License

Copyright (c) 2021 [Hitesh Kumar Saini](https://github.com/alexmercerind)

## Information

- All the research, for making this library possible, is entirely done by myself.
- You can use this library & segments of code from it in your projects in any way you want. Just respect the MIT license & credit the original author of the project.
- Current version of this project (`main` branch) simulates the requests made by YouTube's web client during client side rendering. In simple words, it does not fetch any specific webpage's HTML, but the JSONs internally fetched by YouTube when you navigate the website, after loading the webpage completely.
- I do not resist you from using this library in any possible manner, but YouTube T&C stop you from using this library commercially. Respect the law.
- As you might tell by the name of the project, this library initially only used to support searching of videos. Later on, as the project grew, I added a lot of additional features after requests from people. Now, its really powerful.
