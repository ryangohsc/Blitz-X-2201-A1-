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


def homepage():
    homepage_title = "Blitz-X Home Page"
    homepage_path = Path(ROOT + "/htmlreport/index.html")
    doc = dominate.document(title=str(homepage_title))
    misc_menu_list = get_files(str(Path(ROOT + "/htmlreport/")), "/misc*")
    usb_menu_list = get_files(str(Path(ROOT + "/htmlreport/")), "/usb*")
    file_menu_list = get_files(str(Path(ROOT + "/htmlreport/")), "/file_activity*")
    others_menu_list = get_files(str(Path(ROOT + "/htmlreport/")), "/*")
    others_menu_list = [m for m in others_menu_list if m not in misc_menu_list]
    others_menu_list = [m for m in others_menu_list if m not in usb_menu_list]
    others_menu_list = [m for m in others_menu_list if m not in file_menu_list]
    others_menu_list.remove("index.html")
    with doc.head:
        meta(name="viewport", content="width=device-width, initial-scale=1.0")
        style("""\
                    html {
                        font-family: Verdana;
                        font-size: 12px;
                        max-width: 100%;
                        overflow-x: hidden;
                    }
                    """)
    with doc:
        h1(homepage_title)
        nav_bar = nav()
        with nav_bar:
            ul("Home Page:")
            ul(ul(a("Home", href="index.html")))
            ul("Miscellaneous:")
            ul(ul(a(misc_menu_list, href=misc_menu_list)) for misc_menu_list in misc_menu_list)
            ul("External Device / USB:")
            ul(ul(a(usb_menu_list, href=usb_menu_list)) for usb_menu_list in usb_menu_list)
            ul("File Activity:")
            ul(ul(a(file_menu_list, href=file_menu_list)) for file_menu_list in file_menu_list)
            ul("Other Plugins:")
            ul(ul(a(others_menu_list, href=others_menu_list)) for others_menu_list in others_menu_list)
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
            """)
    with doc:
        h1(args_title)
        nav_bar = nav()
        with nav_bar:
            ul("Home Page:")
            ul(ul(a("Home", href="index.html")))
        with div():
            raw(convert_json)
    with open(args_path, "w") as f:
        f.write(doc.render(pretty=True))


def run():
    homepage()


if __name__ == "__main__":
    run()
    