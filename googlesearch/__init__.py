"""googlesearch is a Python library for searching Google, easily."""
import asyncio
from bs4 import BeautifulSoup
import aiohttp
from .user_agents import get_useragent
import urllib


async def _req(term, results, lang, start, proxy, timeout):
    url="https://www.google.com/search"
    headers={
        "User-Agent": get_useragent()
    }
    params={
        "q": term,
        "num": results + 2,  # Prevents multiple requests
        "hl": lang,
        "start": start,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers = headers, params = params, proxy = proxy, timeout = timeout) as resp:
            resp.raise_for_status()
            return await resp.text()


class SearchResult:
    def __init__(self, url, title, description):
        self.url = url
        self.title = title
        self.description = description

    def __repr__(self):
        return f"SearchResult(url={self.url}, title={self.title}, description={self.description})"


async def search(term, num_results=10, lang="en", proxy=None, advanced=False, sleep_interval=0, timeout=5):
    """Search the Google search engine"""

    escaped_term = urllib.parse.quote_plus(term) # make 'site:xxx.xxx.xxx ' works.


    # Fetch
    start = 0
    while start < num_results:
        # Send request
        resp = await  _req(escaped_term, num_results - start,
                    lang, start, proxy, timeout)
        # Parse
        soup = BeautifulSoup(resp, "html.parser")
        result_block = soup.find_all("div", attrs={"class": "g"})
        print("len(result_block):{}".format(len(result_block)) )
        if len(result_block) ==0:
            start += 1
        for result in result_block:
            # Find link, title, description
            link = result.find("a", href=True)
            title = result.find("h3")
            description_box = result.find(
                "div", {"style": "-webkit-line-clamp:2"})
            if description_box:
                description = description_box.text
                if link and title and description:
                    start += 1
                    if advanced:
                        yield SearchResult(link["href"], title.text, description)
                    else:
                        yield link["href"]
        asyncio.sleep(sleep_interval)

        if start == 0:
            return
