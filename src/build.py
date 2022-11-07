import argparse
from jinja2 import Environment, FileSystemLoader
import json
import os


HEADERS = [
  "home",
  "publications",
  "team",
  "news",
  "jobs",
]

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_PATH, "data")
TEMPLATE_DIR = os.path.join(BASE_PATH, "templates")


def process_publications(data):
    pubs = {
        "book": {
        },
        "journal": {
        },
    }
    for typ in pubs.keys():
        npubs = len(data["publications"][typ])
        for p, pub in enumerate(data["publications"][typ]):
            pub["number"] = npubs - p

            if len(pub["authors"]) == 1:
                authors = pub["author"][0]
            elif len(pub["authors"]) == 2:
                authors = " and ".join(pub["authors"])
            else:
                authors = ", ".join(pub["authors"][:-1]) + ", and " + pub["authors"][-1]
            pub["authors"] = authors

            if "journal" not in pub and "titleBook" not in pub:
                pub["status"] = "submitted"
            elif "doi" not in pub and "url" not in pub:
                pub["status"] = "in press"

            if "doi" in pub:
                url = f'<a href="https://doi.org/{pub["doi"]} target="_blank">DOI:{pub["doi"]}</a>'
            elif "arxiv" in pub:
                url = f'<a href="https://arxiv.org/{pub["arxiv"]} target="_blank">ArXiV</a>'

            year = pub["year"]
            if year not in pubs[typ].keys():
                pubs[typ][year] = [pub]
            else:
                pubs[typ][year].append(pub)
    data["publications"] = pubs


PROCESS_DATA = {
    "publications": process_publications,
}


def arg_parser() -> argparse.ArgumentParser:
    """Parse command line arguments.

    Returns:
    --------
    parser: argparse.ArgumentParser
        The argument parser object
    """
    parser = argparse.ArgumentParser(
        prog="build",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "section",
        type=str.lower,
        help="The section to build.",
    )
    parser.add_argument(
        "-e",
        "--extra_data",
        nargs="*",
        default=[],
    )
    return parser


def build_html(section: str = "", extra_data: list = []) -> str:
    """Create a rendered HTML file.

    Parameters:
    -----------
    section: str
        The section/HTML name.
    extra_data: list
        Extra json files to be read in.

    Returns:
    --------
    str
        The rendered HTML file string.
    """
    if section.endswith(".html"):
        section = section[:-5]

    data = {
        "headers": HEADERS,
        "section": section,
    }
    with open(os.path.join(DATA_DIR, "news.json")) as f:
        data["news"] = json.loads(f.read())
    if section != "news":
        with open(os.path.join(DATA_DIR, f"{section}.json")) as f:
            data[section] = json.loads(f.read())
    for extra in extra_data:
        extra_file = extra
        extra_section = extra
        if extra.endswith(".json"):
            extra_section = extra[:-5]
        else:
            extra_file = f"{extra}.json"
        with open(os.path.join(DATA_DIR, extra_file)) as f:
            data[extra_section] = json.loads(f.read())
    if section in PROCESS_DATA:
        PROCESS_DATA[section](data)

    loader = FileSystemLoader(TEMPLATE_DIR)
    env = Environment(loader=loader)
    template = env.get_template(f"{section}.html")
    return template.render(data=data)


if __name__ == "__main__":
    parser = arg_parser()
    args, _ = parser.parse_known_args()
    print(build_html(args.section, extra_data=args.extra_data))
