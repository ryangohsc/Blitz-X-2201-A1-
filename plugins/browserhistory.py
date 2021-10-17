import json
import browser_cookie3
from browser_history.browsers import Edge
from browser_history.browsers import Chrome
from browser_history.browsers import Firefox
from main import *

# Global Variables
ROOT = str(get_project_root())

# History
CHROME_HISTORY_TITLE = "Chrome History"
CHROME_HISTORY_DESC = "Chrome history. The history of a web browser can assist in activity reporting."
CHROME_HISTORY_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_chrome_history.json")
CHROME_HISTORY_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

FIREFOX_HISTORY_TITLE = "Firefox History"
FIREFOX_HISTORY_DESC = "Firefox history. The history of a web browser can assist in activity reporting."
FIREFOX_HISTORY_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_firefox_history.json")
FIREFOX_HISTORY_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

EDGE_HISTORY_TITLE =  "Edge History"
EDGE_HISTORY_DESC =  "Edge history. The history of a web browser can assist in activity reporting."
EDGE_HISTORY_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_edge_history.json")
EDGE_HISTORY_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

# Cookies
CHROME_COOKIE_TITLE = "Chrome Cookies"
CHROME_COOKIE_DESC = "Chrome cookies. The cookies of a web browser can indicate that the user has a particular page."
CHROME_COOKIE_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_chrome_cookie.json")
CHROME_COOKIE_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

FIREFOX_COOKIE_TITLE = "Firefox Cookies"
FIREFOX_COOKIE_DESC = "Firefox cookies. The cookies of a web browser can indicate that the user has a particular page."
FIREFOX_COOKIE_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_firefox_cookie.json")
FIREFOX_COOKIE_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

EDGE_COOKIE_TITLE = "Edge Cookies"
EDGE_COOKIE_DESC = "Edge cookies. The cookies of a web browser can indicate that the user has a particular page."
EDGE_COOKIE_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_edge_cookie.json")
EDGE_COOKIE_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

# Bookmarks
CHROME_BOOKMARKS_TITLE = "Chrome Bookmarks"
CHROME_BOOKMARKS_DESC = "Chrome bookmarks. The bookmarks of a web browser can indicate pages the user favours."
CHROME_BOOKMARKS_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_chrome_bookmarks.json")
CHROME_BOOKMARKS_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

FIREFOX_BOOKMARKS_TITLE = "Firefox Bookmarks"
FIREFOX_BOOKMARKS_DESC = "Firefox bookmarks. The bookmarks of a web browser can indicate pages the user favours."
FIREFOX_BOOKMARKS_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_firefox_bookmarks.json")
FIREFOX_BOOKMARKS_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

EDGE_BOOKMARKS_TITLE = "Edge Bookmarks"
EDGE_BOOKMARKS_DESC = "Edge bookmarks. The bookmarks of a web browser can indicate pages the user favours."
EDGE_BOOKMARKS_OUTFILE = Path(ROOT + "/data/browser_history/browser_activity_edge_bookmarks.json")
EDGE_BOOKMARKS_OUTFILE.parent.mkdir(exist_ok=True, parents=True)


def dump_to_json(file_path, data):
    """"
    Desc   :    Dumps the data extracted to json format.

    Params :    file_path - The path of the file to dump the json data to.
                data - The extracted data.
    """
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, default=str, indent=4)


def parse_history(title, description, outfile, browser_type):
    """"
    Desc   :    Parses the history of a web browser and extracts it.

    Params :    title - The title of the module.
                description - The description of the module.
                outfile - The file the history gets output to.
                browser_type - The type of browser the function will operate on (e.g. chrome, firefox, edge).
    """
    data = []
    if browser_type == "chrome":
        f = Chrome()
    elif browser_type == "firefox":
        f = Firefox()
    elif browser_type == "edge":
        f = Edge()
    else:
        return
    outputs = f.fetch_history()
    histories = outputs.histories
    for history in histories:
        data.append({
            'time': history[0],
            'url': history[1],
        })
    if len(data) == 0:
        data.insert(0, {"not found": "No history found!"})
    else:
        data = sorted(data, key=lambda k: k['time'], reverse=True)
    data.insert(0, description)
    data.insert(0, title)
    dump_to_json(outfile, data)


def parse_cookies(title, description, outfile, browser_type):
    """"
    Desc   :    Parses the cookies of a web browser and extracts it.

    Params :    title - The title of the module.
                description - The description of the module.
                outfile - The file the cookies gets output to.
                browser_type - The type of browser the function will operate on (e.g. chrome, firefox, edge).
    """
    data = []
    try:
        if browser_type == "chrome":
            cookies = browser_cookie3.chrome()
        elif browser_type == "firefox":
            cookies = browser_cookie3.firefox()
        elif browser_type == "edge":
            cookies = browser_cookie3.edge()
        else:
            return
    except:
        data.insert(0, {"not found": "No cookies found!"})
        data.insert(0, description)
        data.insert(0, title)
        dump_to_json(outfile, data)
        return

    for cookie in cookies:
        data.append({
            'cookie': cookie,
        })
    data.insert(0, description)
    data.insert(0, title)
    dump_to_json(outfile, data)


def parse_bookmarks(title, description, outfile, browser_type):
    """"
    Desc   :    Parses the bookmarks of a web browser and extracts it.

    Params :    title - The title of the module.
                description - The description of the module.
                outfile - The file the bookmarks gets output to.
                browser_type - The type of browser the function will operate on (e.g. chrome, firefox, edge).
    """
    data = []
    if browser_type == "chrome":
        browser = Chrome()
    elif browser_type == "firefox":
        browser = Firefox()
    elif browser_type == "edge":
        browser = Edge()
    else:
        return

    bookmarks = browser.fetch_bookmarks()
    bookmarks = bookmarks.bookmarks
    for bookmark in bookmarks:
        data.append({
            'time': bookmark[0],
            'bookmark': bookmark[1]
        })
    if len(data) == 0:
        data.insert(0, {"not found": "No bookmarks found!"})
    else:
        data = sorted(data, key=lambda k: k['time'], reverse=True)
    data.insert(0, description)
    data.insert(0, title)
    dump_to_json(outfile, data)


def run():
    """"
    Desc   :    Runs the browser_history module.

    Params :    None.
    """
    CHROME_HISTORY_OUTFILE.parent.mkdir(exist_ok=True, parents=True)

    parse_history(CHROME_HISTORY_TITLE, CHROME_HISTORY_DESC, CHROME_HISTORY_OUTFILE, "chrome")
    parse_history(FIREFOX_HISTORY_TITLE, FIREFOX_HISTORY_DESC, FIREFOX_HISTORY_OUTFILE, "firefox")
    parse_history(EDGE_HISTORY_TITLE, EDGE_HISTORY_DESC, EDGE_HISTORY_OUTFILE, "edge")

    parse_cookies(CHROME_COOKIE_TITLE, CHROME_COOKIE_DESC, CHROME_COOKIE_OUTFILE, "chrome")
    parse_cookies(FIREFOX_COOKIE_TITLE, FIREFOX_COOKIE_DESC, FIREFOX_COOKIE_OUTFILE, "firefox")
    parse_cookies(EDGE_COOKIE_TITLE, EDGE_COOKIE_TITLE, EDGE_COOKIE_OUTFILE, "edge")

    parse_bookmarks(CHROME_BOOKMARKS_TITLE, CHROME_BOOKMARKS_DESC, CHROME_BOOKMARKS_OUTFILE, "chrome")
    parse_bookmarks(FIREFOX_BOOKMARKS_TITLE, FIREFOX_BOOKMARKS_DESC, FIREFOX_BOOKMARKS_OUTFILE, "firefox")
    parse_bookmarks(EDGE_BOOKMARKS_TITLE, EDGE_BOOKMARKS_DESC, EDGE_BOOKMARKS_OUTFILE, "edge")


if __name__ == "__main__":
    run()
