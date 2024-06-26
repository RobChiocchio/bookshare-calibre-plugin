#import mimetypes
from contextlib import closing

try:
    from urllib.parse import quote_plus, urljoin
except ImportError:
    from urllib2 import quote_plus, urljoin

from http.cookiejar import LoadError, LWPCookieJar  #, MozillaCookieJar

from bs4 import BeautifulSoup
from PyQt5.Qt import QUrl

#from calibre.utils.opensearch.query import Query
from calibre import browser
from calibre.gui2 import open_url
from calibre.gui2.store import StorePlugin
from calibre.gui2.store.search_result import SearchResult
from calibre.gui2.store.web_store_dialog import WebStoreDialog

from .config import CONFIG, COOKIEJAR_PATH, BookshareStorePluginConfig

BASE_URL = "https://www.bookshare.org"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

ENABLE_DOWNLOADS = False # DEBUG: need to fix download links

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
    s.drm = SearchResult.DRM_UNLOCKED
    #s.formats = ["EPUB"]

    dl_cell = tr.select_one("td[class='downloadLinks']")

    #title_id = dl_cell.select_one("span[class=' readingListAdd'] > a[class='addToReadingListAnchor']")
    title_id = tr.select("td")[2].text.split("-")[-1].strip()
    raw_formats = dl_cell.select("form > select[class='downloadFormatSelector'] > option")
    raw_formats += dl_cell.select("form > select[class='downloadFormatSelector'] > optgroup > option")

    if len(raw_formats) > 0: # and title_id:
        print(title_id)
        for rf in raw_formats:
            #print(rf)
            if rf.get("disabled", False):
                continue

            download_url = urljoin(BASE_URL, f"download/book?titleInstanceId={title_id}&downloadFormat={rf['value']}")
            #ext = mimetypes.guess_extension(rf['value']) if rf["value"] != "DAISY" else "ZIP"
            ext = rf['value'] if rf["value"] != "DAISY" else "ZIP"
            ext = "EPUB" if ext == "EPUB3" else ext # DEBUG: make a real mapping
            if ext and download_url:
                #ext = ext[1:].upper().strip()
                s.formats = ", ".join([ext, s.formats])
                if ENABLE_DOWNLOADS: # DEBUG: does not download file, needs unique id
                    s.downloads[ext] = download_url
        
    return s

def search_bookshare(query, max_results=25, timeout=60, br=None):
    """Search for books
    :param query: A string containing the search query
    :param max_results: Maximum number of results to return
    :param timeout: Timeout in seconds
    :return: A list of dictionaries containing the search results
    """
    max_results = min(max_results, 100)
    url = f"{BASE_URL}/search?limit={max_results}&keyword={quote_plus(query)}"

    counter = max_results
    br = br or browser(user_agent=USER_AGENT)
    
    with closing(br.open(url, timeout=timeout)) as f:
        soup = BeautifulSoup(f.read(), "html5lib")
        results = soup.select("table[class='resultsTable table'] > tbody > tr")
    
        for result in results:
            if counter <= 0:
                break
            counter -= 1

            yield build_search_result(result)

def login(br, username, password):
    """Login to Bookshare
    :param br: A browser session object
    :param username: Bookshare username
    :param password: Bookshare password
    :return: A requests.Session object
    """
    url = urljoin(BASE_URL, "/login")
    br.open(url)
    
    try:
        br.select_form(action=url)
    except Exception as e:
        print(e)
        return br
    
    br["j_userName"] = username
    br["j_password"] = password
    #br["_spring_security_remember_me"] = "true"
    response = br.submit()
    #if "Log out" not in response.read().decode("utf-8"):
    if not is_logged_in(br):
        print("Login failed: ", response.getcode())
    return br

def is_logged_in(br):
    """Check if the user is logged in
    :param br: A browser session object
    :return: True if the user is logged in, False otherwise
    """
    br.open(BASE_URL)
    return "Log out" in br.response().read().decode("utf-8")

class BookshareStore(BookshareStorePluginConfig, StorePlugin):
    def search(self, query, max_results=25, timeout=60):
        for result in search_bookshare(query, max_results, timeout, self.br):
            yield result

    def login(self):
        if (is_logged_in(self.br)):
            self.logged_in = True
            return True
        
        try:
            self.br.cookiejar.load(COOKIEJAR_PATH)
            self.logged_in = is_logged_in(self.br)
        except LoadError:
            pass
        except Exception as e:
            print(e)

        if not self.logged_in and self.config.get("username", None) and self.config.get("password", None):
            self.br = login(self.br, self.config.get("username"), self.config.get("password"))
            self.logged_in = is_logged_in(self.br) # TODO: clean this up
            
            if self.logged_in:
                self.br.add_password(BASE_URL, self.config.get("username"), self.config.get("password"))
                self.br.cookiejar.save()

        print("Logged in: ", self.logged_in)
        return self.logged_in
    
    def create_browser(self):
        br = browser(user_agent=USER_AGENT)
        br.set_cookiejar(LWPCookieJar(COOKIEJAR_PATH, delayload=True))
        return br
    
    def open(self, parent=None, detail_item=None, external=False):
        detail_url = detail_item if detail_item else BASE_URL

        if external or self.config.get("open_external", False):
            open_url(QUrl(detail_url))
        else:
            d = WebStoreDialog(self.gui, detail_url, parent, detail_item)
            d.setWindowTitle(self.name)
            d.set_tags(self.config.get("tags", ""))
            d.exec_()

    def genesis(self):
        """This method is called once per plugin, do initial setup here
        """
        self.name = "Bookshare"
        self.logged_in = False
        #self.config = BookshareConfig()
        self.config = CONFIG
        self.br = self.create_browser()

        self.login()

if __name__ == "__main__":
    for book in search_bookshare("Harry Potter"):
        print(book)