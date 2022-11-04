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

    loader = FileSystemLoader(TEMPLATE_DIR)
    env = Environment(loader=loader)
    template = env.get_template(f"{section}.html")
    return template.render(data=data)


if __name__ == "__main__":
    parser = arg_parser()
    args, _ = parser.parse_known_args()
    print(build_html(args.section, extra_data=args.extra_data))
