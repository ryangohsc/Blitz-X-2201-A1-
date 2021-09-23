from json2html import *
import dominate
from dominate.tags import *
from dominate.util import raw
from pathlib import Path
import glob
import os


def get_project_root():
    """
    Returns project root directory
    """
    return Path(__file__).parent.parent


ROOT = str(get_project_root())


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
    others_menu.remove("index.html")
    return others_menu


def homepage():
    """
    Generates a index.html page
    """
    homepage_title = "Blitz-X Home Page"
    homepage_path = Path(ROOT + "/htmlreport/index.html")
    doc = dominate.document(title=str(homepage_title))
    misc_menu_list = get_misc_menu_list()
    usb_menu_list = get_usb_menu_list()
    file_menu_list = get_file_menu_list()
    others_menu_list = get_others_menu_list()
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
                        font-family: inherit; /* Important for vertical align on mobile phones */
                        margin: 0; /* Important for vertical align on mobile phones */
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
    with open(homepage_path, "w") as f:
        f.write(doc.render(pretty=True))


def html_template(args_title, args_path, args_json_obj):
    convert_json = json2html.convert(json=args_json_obj)
    convert_json = convert_json.replace("<ul>", "")
    convert_json = convert_json.replace("</ui>", "")
    doc = dominate.document(title=str(args_title))
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
                font-family: inherit; /* Important for vertical align on mobile phones */
                margin: 0; /* Important for vertical align on mobile phones */
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
        h1(args_title)
        with div():
            raw(convert_json)
    with open(args_path, "w") as f:
        f.write(doc.render(pretty=True))


def run():
    homepage()


if __name__ == "__main__":
    run()
    