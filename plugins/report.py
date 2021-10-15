from json2html import *
import dominate
from dominate.tags import *
from dominate.util import raw
from pathlib import Path
import glob
import os
from main import return_excluded, return_included, return_post
import json
from datetime import datetime
from coloroma_colours import *

ROOT = str(Path(__file__).parent.parent)


def get_datetime():
    """"
    Gets the current computer time and returns it.
    :param: None
    :return: dt_string
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%YT%H:%M:%S.%f")
    return dt_string


def get_files(path, arg_name):
    """"
    Helper function to return all directories in working directory.
    :param: path
            arg_name
    :return: result
    """
    result = []
    for name in glob.iglob(path + arg_name):
        name = os.path.basename(name)
        result.append(name)
    return result


def nav_misc_menu_list():
    """"
    Returns a list of files that is in the misc category.
    :param: None
    :return: misc_menu
    """
    misc_menu = get_files(str(Path(ROOT + "/data/**/")), "/misc*")
    return misc_menu


def nav_usb_menu_list():
    """"
    Returns a list of files that is in the usb category.
    :param: None
    :return: usb_menu
    """
    usb_menu = get_files(str(Path(ROOT + "/data/**/")), "/usb*")
    return usb_menu


def nav_file_menu_list():
    """"
    Returns a list of files that is in the file activity category.
    :param: None
    :return: file_menu
    """
    file_menu = get_files(str(Path(ROOT + "/data/**/")), "/file_activity*")
    return file_menu


def nav_keyword_menu_list():
    """"
    Returns a list of files that is in the keyword search category.
    :param: None
    :return: keyword_menu
    """
    keyword_menu = get_files(str(Path(ROOT + "/data/**/")), "/keyword_search*")
    return keyword_menu


def nav_browser_menu_list():
    """"
    Returns a list of files that is in the browser activity category.
    :param: None
    :return: browser_menu
    """
    browser_menu = get_files(str(Path(ROOT + "/data/**/")), "/browser_activity*")
    return browser_menu


def nav_others_menu_list():
    """"
    Returns a list of files that is in the others category.
    :param: None
    :return: others_menu
    """
    others_menu = get_files(str(Path(ROOT + "/data/**/")), "/*")
    others_menu = [m for m in others_menu if m not in nav_misc_menu_list()]
    others_menu = [m for m in others_menu if m not in nav_usb_menu_list()]
    others_menu = [m for m in others_menu if m not in nav_file_menu_list()]
    others_menu = [m for m in others_menu if m not in nav_keyword_menu_list()]
    others_menu = [m for m in others_menu if m not in nav_browser_menu_list()]
    return others_menu


def homepage():
    """"
    Generates index.html page, it will only execute when ran from main.py.
    :param: None
    :return: None
    """
    try:
        homepage_title = "Blitz-X Summary Page"
        homepage_path = Path(ROOT + "/HTMLReport/index.html")
        homepage_path.parent.mkdir(exist_ok=True, parents=True)
        doc = dominate.document(title=str(homepage_title))
        misc_menu_list = nav_misc_menu_list()
        if misc_menu_list:
            misc_menu_list = [x.replace("json", "html") for x in misc_menu_list]
        usb_menu_list = nav_usb_menu_list()
        if usb_menu_list:
            usb_menu_list = [x.replace("json", "html") for x in usb_menu_list]
        file_menu_list = nav_file_menu_list()
        if file_menu_list:
            file_menu_list = [x.replace("json", "html") for x in file_menu_list]
        keyword_menu_list = nav_keyword_menu_list()
        if keyword_menu_list:
            keyword_menu_list = [x.replace("json", "html") for x in keyword_menu_list]
        browser_menu_list = nav_browser_menu_list()
        if browser_menu_list:
            browser_menu_list = [x.replace("json", "html") for x in browser_menu_list]
        others_menu_list = nav_others_menu_list()
        if others_menu_list:
            others_menu_list = [x.replace("json", "html") for x in others_menu_list]
        excluded_plugins = ", ".join(return_excluded())
        included_plugins = ", ".join(return_included())
        post_plugins = ", ".join(return_post())
        if len(excluded_plugins) == 0:
            excluded_plugins = "No plugins were excluded."
        if len(included_plugins) == 0:
            included_plugins = "No plugins were included."
        if len(post_plugins) == 0:
            post_plugins = "No plugins were used for post-processing."
        with doc.head:
            meta(name="viewport", content="width=device-width, initial-scale=1.0")
            style("""\
                        html {
                            font-family: Verdana;
                            font-size: 12px;
                            max-width: 100%;
                            overflow-x: hidden;
                        }
                        .dropdown {
                            float: left;
                            overflow: hidden;
                        }
                        .navbar {
                            overflow: hidden;
                            background-color: #333;
                        }
                        .dropdown .dropbtn {
                            font-size: 16px;
                            border: none;
                            outline: none;
                            color: white;
                            padding: 14px 16px;
                            background-color: inherit;
                            font-family: inherit;
                            margin: 0;
                        }
                        .dropdown-content {
                            display: none;
                            position: absolute;
                            background-color: #f2f2f2;
                            min-width: 160px;
                            box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                            z-index: 1;
                        }
                        .dropdown-content a {
                            float: none;
                            color: black;
                            padding: 12px 16px;
                            text-decoration: none;
                            display: block;
                            text-align: left;
                        }
                        .dropdown:hover .dropdown-content {
                            display: block;
                        }
                        .navbar a {
                            float: left;
                            font-size: 16px;
                            color: white;
                            text-align: center;
                            padding: 14px 16px;
                            text-decoration: none;
                        }
                        .dropdown-content a:hover {
                            background-color: #ddd;
                        }
                        .dropdown-content a {
                            float: none;
                            color: black;
                            padding: 12px 16px;
                            text-decoration: none;
                            display: block;
                            text-align: left;
                        }
                        .navbar a:hover, .dropdown:hover .dropbtn {
                            background-color: #cbcbcb;
                        }
                        """)
        with doc:
            nav_bar = div(cls="navbar")
            with nav_bar:
                a("Home", href="index.html")
                if misc_menu_list:
                    dropdown = div(cls="dropdown")
                    with dropdown:
                        button("Miscellaneous", cls="dropbtn")
                    with dropdown:
                        dropdown_div = div(cls="dropdown-content")
                        dropdown_div.add(a(misc_menu_list, href=misc_menu_list) for misc_menu_list in misc_menu_list)
                if usb_menu_list:
                    dropdown = div(cls="dropdown")
                    with dropdown:
                        button("External Device / USB", cls="dropbtn")
                    with dropdown:
                        dropdown_div = div(cls="dropdown-content")
                        dropdown_div.add(a(usb_menu_list, href=usb_menu_list) for usb_menu_list in usb_menu_list)
                if file_menu_list:
                    dropdown = div(cls="dropdown")
                    with dropdown:
                        button("File Activity", cls="dropbtn")
                    with dropdown:
                        dropdown_div = div(cls="dropdown-content")
                        dropdown_div.add(a(file_menu_list, href=file_menu_list) for file_menu_list in file_menu_list)
                if keyword_menu_list:
                    dropdown = div(cls="dropdown")
                    with dropdown:
                        button("Keyword Search", cls="dropbtn")
                    with dropdown:
                        dropdown_div = div(cls="dropdown-content")
                        dropdown_div.add(a(keyword_menu_list, href=keyword_menu_list) for keyword_menu_list in keyword_menu_list)
                if browser_menu_list:
                    dropdown = div(cls="dropdown")
                    with dropdown:
                        button("Browser Activity", cls="dropbtn")
                    with dropdown:
                        dropdown_div = div(cls="dropdown-content")
                        dropdown_div.add(
                            a(browser_menu_list, href=browser_menu_list) for browser_menu_list in browser_menu_list)
                if others_menu_list:
                    dropdown = div(cls="dropdown")
                    with dropdown:
                        button("Other Plugins", cls="dropbtn")
                    with dropdown:
                        dropdown_div = div(cls="dropdown-content")
                        dropdown_div.add(a(others_menu_list, href=others_menu_list) for others_menu_list in others_menu_list)
            h1(homepage_title)
            hr()
            h2("About Blitz-X")
            pre("\n ######                              #     # \n"
                " #     # #      # ##### ######        #   # \n"
                " #     # #      #   #       #          # #  \n"
                " ######  #      #   #      #   #####    #   \n"
                " #     # #      #   #     #            # #  \n"
                " #     # #      #   #    #            #   # \n"
                " ######  ###### #   #   ######       #     # \n")
            p("Blitz-X (Blitz-eXtractor) is a modular forensic triage tool written in Python designed to access "
              "various forensic artifacts on Windows relating to user data exfiltration. ")
            p("The tool will parse the artifacts, and present them in a format viable for analysis. ")
            p("The output may provide valuable insights during an incident response in a Windows environment while "
              "waiting for a full disk image to be acquired.")
            p("The tool is meant to run on live systems on the offending User Account with administrative rights.")
            hr()
            h2("Report Information")
            p("This report was generated on: " + str(get_datetime()) + " Local Time.")
            p("Modules that were loaded: " + included_plugins + ".")
            p("Modules that were used for post-processing: " + post_plugins + ".")
            p("Modules that were excluded are: " + excluded_plugins + ".")
        with open(homepage_path, "w") as f:
            f.write(doc.render(pretty=True))
    except:
        print(print_red("INFO: index.html failed to generate"))
        pass


def get_json_files():
    """"
    Returns all files in a list that resides in the data directory with a json extension.
    :param: None
    :return: json_files
    """
    json_files = []
    for root, dirs, files in os.walk(str(Path(ROOT + "/data/"))):
        for file in files:
            json_files.append(os.path.join(root, file))
    return json_files


def get_json_title():
    """"
    Returns all json file titles in the data directory in a list.
    :param: None
    :return: json_title
     """
    json_title = []
    for root, dirs, files in os.walk(str(Path(ROOT + "/data/"))):
        for file in files:
            file = file[:-5]
            json_title.append(file)
    return json_title


def json_to_html(args_dir):
    """"
    Takes in the full pathname of the json file and converts it to html and returns it.
    :param: args_dir
    :return: convert_json
     """
    with open(args_dir, "r") as f:
        json_info = json.loads(f.read())
        convert_json = json2html.convert(json=json_info)
        convert_json = convert_json.replace("<ul>", "")
        convert_json = convert_json.replace("</ui>", "")
    return convert_json


def html_template():
    """"
    Generates a template in HTML.
    :param: None
    :return: None
     """
    try:
        misc_menu_list = nav_misc_menu_list()
        if misc_menu_list:
            misc_menu_list = [x.replace("json", "html") for x in misc_menu_list]
        usb_menu_list = nav_usb_menu_list()
        if usb_menu_list:
            usb_menu_list = [x.replace("json", "html") for x in usb_menu_list]
        file_menu_list = nav_file_menu_list()
        if file_menu_list:
            file_menu_list = [x.replace("json", "html") for x in file_menu_list]
        keyword_menu_list = nav_keyword_menu_list()
        if keyword_menu_list:
            keyword_menu_list = [x.replace("json", "html") for x in keyword_menu_list]
        browser_menu_list = nav_browser_menu_list()
        if browser_menu_list:
            browser_menu_list = [x.replace("json", "html") for x in browser_menu_list]
        others_menu_list = nav_others_menu_list()
        if others_menu_list:
            others_menu_list = [x.replace("json", "html") for x in others_menu_list]
        json_files = get_json_files()
        json_title = get_json_title()
        for json_files, json_title in zip(json_files, json_title):
            json_html = json_to_html(json_files)
            doc = dominate.document(title=str(json_title))
            with doc.head:
                meta(name="viewport", content="width=device-width, initial-scale=1.0")
                style("""\
                    table {
                        table-layout: fixed;
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 8px;
                        margin-bottom: 8px;
                    }
                    td {
                        width: 70%;
                    }
                    th {
                        width:30%;
                    }
                    th, td {
                        padding: 5px;
                        text-align: left;
                        word-wrap: break-word;
                    }
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                    html {
                        font-family: Verdana;
                        font-size: 12px;
                        max-width: 100%;
                        overflow-x: hidden;
                    }
                    ul, li {
                        list-style-type: none;
                    }
                    .dropdown {
                        float: left;
                        overflow: hidden;
                    }
                    .navbar {
                        overflow: hidden;
                        background-color: #333;
                    }
                    .dropdown .dropbtn {
                        font-size: 16px;
                        border: none;
                        outline: none;
                        color: white;
                        padding: 14px 16px;
                        background-color: inherit;
                        font-family: inherit;
                        margin: 0;
                    }
                    .dropdown-content {
                        display: none;
                        position: absolute;
                        background-color: #f2f2f2;
                        min-width: 160px;
                        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                        z-index: 1;
                    }
                    .dropdown-content a {
                        float: none;
                        color: black;
                        padding: 12px 16px;
                        text-decoration: none;
                        display: block;
                        text-align: left;
                    }
                    .dropdown:hover .dropdown-content {
                        display: block;
                    }
                    .navbar a {
                        float: left;
                        font-size: 16px;
                        color: white;
                        text-align: center;
                        padding: 14px 16px;
                        text-decoration: none;
                    }
                    .dropdown-content a:hover {
                        background-color: #ddd;
                    }
                    .dropdown-content a {
                        float: none;
                        color: black;
                        padding: 12px 16px;
                        text-decoration: none;
                        display: block;
                        text-align: left;
                    }
                    .navbar a:hover, .dropdown:hover .dropbtn {
                        background-color: #cbcbcb;
                    }
                    """)
            with doc:
                nav_bar = div(cls="navbar")
                with nav_bar:
                    a("Home", href="index.html")
                    if misc_menu_list:
                        dropdown = div(cls="dropdown")
                        with dropdown:
                            button("Miscellaneous", cls="dropbtn")
                        with dropdown:
                            dropdown_div = div(cls="dropdown-content")
                            dropdown_div.add(a(misc_menu_list, href=misc_menu_list) for misc_menu_list in misc_menu_list)
                    if usb_menu_list:
                        dropdown = div(cls="dropdown")
                        with dropdown:
                            button("External Device / USB", cls="dropbtn")
                        with dropdown:
                            dropdown_div = div(cls="dropdown-content")
                            dropdown_div.add(a(usb_menu_list, href=usb_menu_list) for usb_menu_list in usb_menu_list)
                    if file_menu_list:
                        dropdown = div(cls="dropdown")
                        with dropdown:
                            button("File Activity", cls="dropbtn")
                        with dropdown:
                            dropdown_div = div(cls="dropdown-content")
                            dropdown_div.add(a(file_menu_list, href=file_menu_list) for file_menu_list in file_menu_list)
                    if keyword_menu_list:
                        dropdown = div(cls="dropdown")
                        with dropdown:
                            button("Keyword Search", cls="dropbtn")
                        with dropdown:
                            dropdown_div = div(cls="dropdown-content")
                            dropdown_div.add(a(keyword_menu_list, href=keyword_menu_list) for keyword_menu_list in keyword_menu_list)
                    if browser_menu_list:
                        dropdown = div(cls="dropdown")
                        with dropdown:
                            button("Browser Activity", cls="dropbtn")
                        with dropdown:
                            dropdown_div = div(cls="dropdown-content")
                            dropdown_div.add(
                                a(browser_menu_list, href=browser_menu_list) for browser_menu_list in browser_menu_list)
                    if others_menu_list:
                        dropdown = div(cls="dropdown")
                        with dropdown:
                            button("Other Plugins", cls="dropbtn")
                        with dropdown:
                            dropdown_div = div(cls="dropdown-content")
                            dropdown_div.add(
                                a(others_menu_list, href=others_menu_list) for others_menu_list in others_menu_list)
                h1(json_title)
                hr()
                with div():
                    raw(json_html)
            filename = Path(ROOT + "/HTMLReport/" + json_title + ".html")
            filename.parent.mkdir(exist_ok=True, parents=True)
            with open(filename, "w") as f:
                f.write(doc.render(pretty=True))
    except:
        pass


def run():
    """
    Runs the report module.
    :param: None
    :return: None
    """
    html_template()
    homepage()


if __name__ == "__main__":
    run()
