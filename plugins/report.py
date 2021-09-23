from json2html import *
import dominate
from dominate.tags import *
from dominate.util import raw
from pathlib import Path
import glob
import os
from main import return_excluded
import json
from datetime import datetime


def get_project_root():
    """
    Returns project root directory
    """
    return Path(__file__).parent.parent


ROOT = str(get_project_root())


def get_datetime():
    """
    Gets the current computer time and returns it
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%YT%H:%M:%S")
    return dt_string


def get_files(path, arg_name):
    """
    Helper function to return all directories in working directory
    """
    result = []
    for name in glob.iglob(path + arg_name):
        name = os.path.basename(name)
        result.append(name)
    return result


def get_misc_menu_list():
    """
    Returns a list of files that is in the misc category
    """
    misc_menu = get_files(str(Path(ROOT + "/htmlreport/")), "/misc*")
    return misc_menu


def get_usb_menu_list():
    """
    Returns a list of files that is in the usb category
    """
    usb_menu = get_files(str(Path(ROOT + "/htmlreport/")), "/usb*")
    return usb_menu


def get_file_menu_list():
    """
    Returns a list of files that is in the file activity category
    """
    file_menu = get_files(str(Path(ROOT + "/htmlreport/")), "/file_activity*")
    return file_menu


def get_others_menu_list():
    """
    Returns a list of files that is in the others category
    """
    others_menu = get_files(str(Path(ROOT + "/htmlreport/")), "/*")
    others_menu = [m for m in others_menu if m not in get_misc_menu_list()]
    others_menu = [m for m in others_menu if m not in get_usb_menu_list()]
    others_menu = [m for m in others_menu if m not in get_file_menu_list()]
    try:
        others_menu.remove("index.html")
    except ValueError:
        pass
    return others_menu


def homepage():
    """
    Generates index.html page
    """
    homepage_title = "Blitz-X Home Page"
    homepage_path = Path(ROOT + "/htmlreport/index.html")
    doc = dominate.document(title=str(homepage_title))
    misc_menu_list = get_misc_menu_list()
    usb_menu_list = get_usb_menu_list()
    file_menu_list = get_file_menu_list()
    others_menu_list = get_others_menu_list()
    excluded_plugins = "".join(return_excluded())
    if len(excluded_plugins) == 0:
        excluded_plugins = "No plugins were excluded."
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
                        background-color: #f9f9f9;
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
                        background-color: red;
                    }
                    """)
    with doc:
        nav_bar = div(cls="navbar")
        with nav_bar:
            a("Home", href="index.html")
            dropdown = div(cls="dropdown")
            with dropdown:
                button("Miscellaneous", cls="dropbtn")
            with dropdown:
                dropdown_div = div(cls="dropdown-content")
                dropdown_div.add(a(misc_menu_list, href=misc_menu_list) for misc_menu_list in misc_menu_list)
            dropdown = div(cls="dropdown")
            with dropdown:
                button("External Device / USB", cls="dropbtn")
            with dropdown:
                dropdown_div = div(cls="dropdown-content")
                dropdown_div.add(a(usb_menu_list, href=usb_menu_list) for usb_menu_list in usb_menu_list)
            dropdown = div(cls="dropdown")
            with dropdown:
                button("File Activity", cls="dropbtn")
            with dropdown:
                dropdown_div = div(cls="dropdown-content")
                dropdown_div.add(a(file_menu_list, href=file_menu_list) for file_menu_list in file_menu_list)
            dropdown = div(cls="dropdown")
            with dropdown:
                button("Other Plugins", cls="dropbtn")
            with dropdown:
                dropdown_div = div(cls="dropdown-content")
                dropdown_div.add(a(others_menu_list, href=others_menu_list) for others_menu_list in others_menu_list)
        h1(homepage_title)
        p("This report was generated on: " + str(get_datetime()) + " local time.")
        p("Modules that are loaded:")
        p("Modules that are excluded are: " + excluded_plugins)
    with open(homepage_path, "w") as f:
        f.write(doc.render(pretty=True))


def get_json_files():
    json_files = []
    for root, dirs, files in os.walk(str(Path(ROOT + "/data/"))):
        for file in files:
            json_files.append(os.path.join(root, file))
    return json_files


def get_json_title():
    json_title = []
    for root, dirs, files in os.walk(str(Path(ROOT + "/data/"))):
        for file in files:
            file = file[:-5]
            json_title.append(file)
    return json_title


def json_to_html(args_dir):
    with open(args_dir, "r") as f:
        json_info = json.loads(f.read())
        convert_json = json2html.convert(json=json_info)
        convert_json = convert_json.replace("<ul>", "")
        convert_json = convert_json.replace("</ui>", "")
    return convert_json


def html_template():
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
                    word-wrap: break-word;
                }
                th {
                    width:30%;
                }
                th, td {
                    padding: 5px;
                    text-align: left;
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
                    background-color: #f9f9f9;
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
                    background-color: red;
                }
                """)
        with doc:
            misc_menu_list = get_misc_menu_list()
            usb_menu_list = get_usb_menu_list()
            file_menu_list = get_file_menu_list()
            others_menu_list = get_others_menu_list()
            nav_bar = div(cls="navbar")
            with nav_bar:
                a("Home", href="index.html")
                dropdown = div(cls="dropdown")
                with dropdown:
                    button("Miscellaneous", cls="dropbtn")
                with dropdown:
                    dropdown_div = div(cls="dropdown-content")
                    dropdown_div.add(a(misc_menu_list, href=misc_menu_list) for misc_menu_list in misc_menu_list)
                dropdown = div(cls="dropdown")
                with dropdown:
                    button("External Device / USB", cls="dropbtn")
                with dropdown:
                    dropdown_div = div(cls="dropdown-content")
                    dropdown_div.add(a(usb_menu_list, href=usb_menu_list) for usb_menu_list in usb_menu_list)
                dropdown = div(cls="dropdown")
                with dropdown:
                    button("File Activity", cls="dropbtn")
                with dropdown:
                    dropdown_div = div(cls="dropdown-content")
                    dropdown_div.add(a(file_menu_list, href=file_menu_list) for file_menu_list in file_menu_list)
                dropdown = div(cls="dropdown")
                with dropdown:
                    button("Other Plugins", cls="dropbtn")
                with dropdown:
                    dropdown_div = div(cls="dropdown-content")
                    dropdown_div.add(a(others_menu_list, href=others_menu_list) for others_menu_list in others_menu_list)
            h1(json_title)
            with div():
                raw(json_html)
        filename = Path(ROOT + "/htmlreport/" + json_title + ".html")
        filename.parent.mkdir(exist_ok=True, parents=True)
        with open(filename, "w") as f:
            f.write(doc.render(pretty=True))


def run():
    html_template()
    homepage()


if __name__ == "__main__":
    run()
