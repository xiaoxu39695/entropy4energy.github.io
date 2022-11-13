import argparse
import functools
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


def process_home(data):
    nslides_max = 10
    img_base = os.path.join(BASE_PATH, "media/publications/")
    slides = []
    for pub in data["publications"]["journal"]:
        if "doi" in pub:
            pub["url"] = f"https://doi.org/{pub['doi']}"
        elif "arxiv" in pub:
            pub["url"] = f"https://arxiv.org/{pub['arxiv']}"
        elif "url" not in pub:
            continue

        if "filename" not in pub:
            continue
        img_file = os.path.join(img_base, f"{pub['filename']}.png")
        if not os.path.exists(os.path.join(img_base, img_file)):
            continue

        slide = {
            "img": f"media/publications/{pub['filename']}.png",
            "text": pub["title"],
            "url": pub["url"],
        }
        slides.append(slide)
        if len(slides) == nslides_max:
            break
    data["slideshow"] = slides


def process_jobs(data):
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"]
    for job in data["jobs"]:
        for month in months:
            job["open"] = job["open"].replace(month, month[:3])
            if "close" in job:
                job["close"] = job["close"].replace(month, month[:3])


def process_publications(data):
    pubs = {
        "book": {
        },
        "journal": {
        },
    }
    file_base = os.path.join(BASE_PATH, "media/publications")
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
                pub["url"] = f'<a href="https://doi.org/{pub["doi"]}" target="_blank">DOI:{pub["doi"]}</a>'
            elif "arxiv" in pub:
                pub["url"] = f'<a href="https://arxiv.org/{pub["arxiv"]}" target="_blank">ArXiV</a>'
            elif "url" in pub:
                pub["url"] = f'<a href="{pub["url"]}" target="_blank">publication</a>'

            if "filename" in pub:
                pdf_file = os.path.join(file_base, f"{pub['filename']}.pdf")
                if not os.path.exists(pdf_file):
                    del pub["filename"]
            if "filename" in pub:
                img_file = os.path.join(file_base, f"{pub['filename']}.png")
                if os.path.exists(img_file):
                    pub["imgfile"] = pub["filename"]

            year = pub["year"]
            if year not in pubs[typ].keys():
                pubs[typ][year] = [pub]
            else:
                pubs[typ][year].append(pub)
    data["publications"] = pubs


def process_team(data):
    def sort_members(a, b):
        if a["id"] == "corey_oses":
            return 1
        if b["id"] == "corey_oses":
            return -1
        if a["rank"] != b["rank"]:
            return 1 if a["rank"] < b["rank"] else -1
        if a["name"] != b["name"]:
            return 1 if a["name"] < b["name"] else -1
        return 0

    groups = [
        {
            "positions": ["Professor", "Assistant Professor"],
            "title": "",
        },
        {
            "positions": ["Postdoctoral Associate"],
            "title": "Postdocs",
        },
        {
            "positions": ["Graduate Student"],
            "title": "Graduate Students",
        },
        {
            "positions": ["Undergraduate Student"],
            "title": "Undergraduate Students",
        },
    ]

    socials = [
        {
            "base": "https://scholar.google.com/citations?user=",
            "icon": '<i class="ai ai-google-scholar-square ai-2x ai-inverse"></i>',
            "key": "gscholar",
        },
        {
            "base": "https://orcid.org/",
            "icon": '<i class="ai ai-orcid-square ai-2x ai-inverse"></i>',
            "key": "orcid",
        },
    ]

    # Assign team members to their groups
    team = {
        "alumni": [],
        "current": [],
    }
    for key in team.keys():
        team[key] = [{"title": grp["title"], "members": []} for grp in groups]
        # Catch-all group if no title fits
        team[key].append({"title": "Affiliates", "members": []})

    for member_id, member in data["team"].items():
        member["id"] = member_id
        member_socials = []
        if "socials" in member:
            for social in socials:
                key = social["key"]
                if key in member["socials"]:
                    member_socials.append({
                        "href": f"{social['base']}{member['socials'][key]}",
                        "icon": social["icon"],
                    })
        member["socials"] = member_socials

        key = "alumni" if "alumnus" in member else "current"
        g = 0
        for group in groups:
            p = 0
            for position in group["positions"]:
                if position in member["titles"]:
                    member["rank"] = p  # for sorting
                    team[key][g]["members"].append(member)
                    break
                p += 1
            if p < len(group["positions"]):
                break
            g += 1
        if g == len(groups):
            team[key][-1]["members"].append(member)

    for groups in team.values():
        for group in groups:
            group["members"] = sorted(group["members"],
                                      key=functools.cmp_to_key(sort_members),
                                      reverse=True)

    # Discard empty groups
    data["team"] = {key: [grp for grp in item if len(grp["members"]) > 0]
                    for key, item in team.items()}


PROCESS_DATA = {
    "home": process_home,
    "jobs": process_jobs,
    "publications": process_publications,
    "team": process_team,
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
    section_data_file = os.path.join(DATA_DIR, f"{section}.json")
    if section != "news" and os.path.exists(section_data_file):
        with open(section_data_file) as f:
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
