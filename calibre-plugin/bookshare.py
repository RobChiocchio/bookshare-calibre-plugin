import mimetypes
import urllib.parse
from contextlib import closing

from bs4 import BeautifulSoup

#from calibre.utils.opensearch.query import Query
from calibre import browser
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.basic_config import BasicStoreConfig
from calibre.gui2.store.search_result import SearchResult

BASE_URL = "https://www.bookshare.org"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

def build_search_result(tr):
    """Build a search result from a BeautifulSoup tag
    :param tr: A BeautifulSoup tag
    :return: A SearchResult object
    """
    s = SearchResult()

    s.title = tr.select_one("td[class='title']").select("a")[-1].text
    s.author = tr.select_one("td[class='author']").select("a")[-1].text
    s.isbn = tr.select("td")[2].text
    s.cover_url = tr.select_one("td[class='title']").select_one("img[class='cover-image-search']")["src"]
    s.detail_item = tr.select_one("td[class='title']").select("a")[-1]["href"]
    s.drm = SearchResult.DRM_UNKNOWN
    #s.formats = ["EPUB"]

    title_id = tr.select_one("a[class='addToReadingListAnchor']")["id"]
    raw_formats = tr.select_one("select[class='downloadFormatSelector']").select("option")["value"]

    for rf in raw_formats:
        download_url = urllib.parse.urljoin(BASE_URL, f"download/book?titleInstanceId={title_id}&downloadFormat={rf}")
        ext = mimetypes.guess_extension(download_url) if rf != "DAISY" else "ZIP"
        if ext and download_url:
            ext = ext[1:].upper().strip()
            s.formats.append(ext)
            s.downloads[ext] = download_url
            break
        
    return s

def search_bookshare(query, max_results=25, timeout=60):
    """Search for books
    :param query: A string containing the search query
    :param max_results: Maximum number of results to return
    :param timeout: Timeout in seconds
    :return: A list of dictionaries containing the search results
    """
    max_results = min(max_results, 100)
    url = f"{BASE_URL}/search?limit={max_results}&keyword={urllib.parse.quote_plus(query)}"

    counter = max_results
    br = browser(user_agent=USER_AGENT)

    with closing(br.open(url, timeout=timeout)) as f:
        soup = BeautifulSoup(f.read(), "html5lib")
        results = soup.find("table[class='resultsTable'] > tbody").select("tr")
    
        for result in results:
            if counter <= 0:
                break
            counter -= 1

            yield build_search_result(result)

class BookshareStore(BasicStoreConfig, StorePlugin):
    def genesis(self):
        """This method is called once per plugin, do initial setup here
        """
        self.name = "Bookshare"
        self.logged_in = False

    def search(self, query, max_results=25, timeout=60):
        for result in search_bookshare(query, max_results, timeout):
            yield result


if __name__ == "__main__":
    for book in search_bookshare("Harry Potter"):
        print(book)