from json2html import *
import dominate
from dominate.tags import *
from dominate.util import raw


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
        with div():
            raw(convert_json)
    with open(args_path, "w") as f:
        f.write(doc.render(pretty=True))


def run():
    pass


if __name__ == "__main__":
    run()
    