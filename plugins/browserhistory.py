#important module to install
#pip install browser-history
#pip3 install browser-cookie3

#importing module
import json
import browser_cookie3

def write_Edgehistory_json():
    from browser_history.browsers import Edge
    f = Edge()
    outputs = f.fetch_history()
    his = outputs.histories
    outputs.save("Edge.json")

def write_Chromehistory_json():
    from browser_history.browsers import Chrome
    f = Chrome()
    outputs = f.fetch_history()
    his = outputs.histories
    outputs.save("Chrome.json")


def write_Foxhistory_json():
    from browser_history.browsers import Firefox
    f = Firefox()
    outputs = f.fetch_history()
    his = outputs.histories
    outputs.save("Firefox.json")

def Foxhistory_bookmark_json():
    from browser_history.browsers import Firefox
    f = Firefox()
    outputs = f.fetch_bookmarks()
    bms = outputs.bookmarks
    outputs.save("FirefoxBM.json")

def Chromehistory_bookmark_json():
    from browser_history.browsers import Firefox
    f = Firefox()
    outputs = f.fetch_bookmarks()
    bms = outputs.bookmarks
    outputs.save("ChromeBM.json")

def Edgehistory_bookmark_json():
    from browser_history.browsers import Firefox
    f = Firefox()
    outputs = f.fetch_bookmarks()
    bms = outputs.bookmarks
    outputs.save("EdgeBM.json")

def Chrome_Cookie_json():
    with open('Chrome_cookie.json', mode='w', encoding='utf-8', newline='') as file:
        for list in browser_cookie3.chrome():
            json.dump(list.__dict__, file, ensure_ascii=False)
            file.write('\n')

def firefox_Cookie_json():
    with open('firefox_cookie.json', mode='w', encoding='utf-8', newline='') as file:
        for list in browser_cookie3.firefox():
            json.dump(list.__dict__, file, ensure_ascii=False)
            file.write('\n')

def edge_Cookie_json():
    import browser_cookie3
    with open('edge_cookie.json', mode='w', encoding='utf-8', newline='') as file:
        for list in browser_cookie3.edge():
            json.dump(list.__dict__, file, ensure_ascii=False)
            file.write('\n')

def run():
    Chrome_Cookie_json()
    edge_Cookie_json()
    firefox_Cookie_json()
    write_Edgehistory_json()
    write_Chromehistory_json()
    write_Foxhistory_json()
    Edgehistory_bookmark_json()
    Chromehistory_bookmark_json()
    Foxhistory_bookmark_json()


if __name__ == "__main__":
    run()
