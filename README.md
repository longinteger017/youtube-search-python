# How to run:
1. Fill the keyword lists in keywords.txt by adding them line by line
2. Run ```python3 main.py```
3. Check database in sqlite database 'youtube_videos.db' by executing
```sqlite3 youtube_videos.db```


# TODOs
1. get youtuber's from scraping process into a dedicated youtuber table with their subscriber count
2. research NLP and see how to apply it on the database
2a. create a jupyter notebook to play around

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
