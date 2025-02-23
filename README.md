# async_googlesearch
async_googlesearch is a Python library for searching Google, easily. googlesearch uses requests and BeautifulSoup4 to scrape Google. 

## Installation
To install, run the following command:
```bash
python3 -m pip install git+https://github.com/alexmerm/async-googlesearch.git
```
## Usage
To get results for a search term, simply use the search function in googlesearch. For example, to get results for "Google" in Google, just run the following program:
```python
from async_googlesearch import search
async for link in search("Google"):
    print(link)
```

## Additional options
async_googlesearch supports a few additional options. By default, async_googlesearch returns 10 results. This can be changed. To get a 100 results on Google for example, run the following program.
```python
from async_googlesearch import search
await search("Google", num_results=100)
```
In addition, you can change the language google searches in. For example, to get results in French run the following program:
```python
from async_googlesearch import search
await search("Google", lang="fr")
```
To extract more information, such as the description or the result URL, use an advanced search:
```python
from async_googlesearch import search
await search("Google", advanced=True)
# Returns a list of SearchResult
# Properties:
# - title
# - url
# - description
```
If requesting more than 100 results, googlesearch will send multiple requests to go through the pages. To increase the time between these requests, use `sleep_interval`:
```python
from async_googlesearch import search
await search("Google", sleep_interval=5, num_results=200)
```