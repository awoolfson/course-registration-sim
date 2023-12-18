# credit to Bill Tran for the original code for this file

import json
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup


def update_classes() -> None:
    print("fetching data")
    raw_data = fetch_data()
    print("parsing data")
    classes = parse_data(raw_data)
    print("cleaning data")
    classes = clean_data(classes)
    save_data(classes)


def fetch_data() -> bytes:
    url = "https://ssbprod.conncoll.edu/CONN/bwckschd.p_get_crse_unsec"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "term_in": 202410,
        "begin_ap": "a",
        "begin_hh": "0",
        "begin_mi": "0",
        "end_ap": "a",
        "end_hh": "0",
        "end_mi": "0",
        "sel_attr": ["dummy", "%"],
        "sel_camp": "dummy",
        "sel_crse": "",
        "sel_day": "dummy",
        "sel_from_cred": "",
        "sel_insm": "dummy",
        "sel_instr": ["dummy", "%"],
        "sel_levl": "dummy",
        "sel_ptrm": "dummy",
        "sel_schd": "dummy",
        "sel_sess": "dummy",
        "sel_subj": [
            "dummy",
            "ACC",
            "AFR",
            "ASL",
            "AMS",
            "ANT",
            "ARA",
            "ARC",
            "ART",
            "AHI",
            "AT",
            "AST",
            "BIO",
            "BOT",
            "CHM",
            "CHI",
            "CLA",
            "COM",
            "CRE",
            "DAN",
            "EAS",
            "ECO",
            "EDU",
            "ENG",
            "ES",
            "FLM",
            "FYS",
            "FRH",
            "GWS",
            "GEO",
            "GER",
            "GIS",
            "GOV",
            "GRK",
            "HBR",
            "SPA",
            "HIS",
            "HMD",
            "IS",
            "CRT",
            "DAT",
            "ENT",
            "FDP",
            "GC",
            "MRC",
            "PAX",
            "PKP",
            "PBH",
            "SJS",
            "ITL",
            "JPN",
            "JS",
            "LAT",
            "LA",
            "LIN",
            "MAT",
            "MSM",
            "MUS",
            "NEU",
            "PHI",
            "PHE",
            "PHY",
            "PSY",
            "RUS",
            "SLA",
            "SOC",
            "STA",
            "THE",
        ],
        "sel_title": "",
        "sel_to_cred": "",
    }
    r = requests.post(url, headers=headers, data=data)
    return r.content


def parse_data(fetched_content: bytes) -> Dict[str, Dict]:
    soup = BeautifulSoup(fetched_content, "html.parser")
    with open("soup.txt", "w") as f:
        f.write(soup.text)

    raw_classes = soup.find("table", {"class": "bwckschd"}).findAll(
        "td", {"class": "bwckschd_det"}
    )
    parsed_classes = [raw_classes[i : i + 19] for i in range(0, len(raw_classes), 19)]

    classes = {}
    date_time_separator = "%"
    for cls in parsed_classes:
        cls_data = {
            "dept": cls[1].string.strip(),
            "code": cls[2].string.strip(),
            "section": cls[3].string.strip(),
            "name": " ".join(cls[6].string.strip().split()),
            "days": cls[8]
            .get_text(separator=date_time_separator)
            .strip()
            .split(date_time_separator),
            "time": cls[9]
            .get_text(separator=date_time_separator)
            .strip()
            .split(date_time_separator),
            "instructor": cls[-1].string.strip() if cls[-1].string else None,
            "credits": cls[4].string.strip(),
            "attrs": cls[7].string.strip(),
            "cap": cls[11].string.strip(),
        }
        crn = cls[0].string.strip()
        classes[crn] = cls_data
    return classes


def clean_data(classes: Dict[str, Dict]) -> Dict[str, Dict]:
    to_pop = []
    for crn in classes:
        if "TBA" in classes[crn]["days"] or "TBA" in classes[crn]["time"]:
            to_pop.append(crn)
            continue
        elif classes[crn]["cap"] == "0":
            to_pop.append(crn)
    for crn in to_pop:
        classes.pop(crn)
    return classes


def save_data(classes: Dict[str, Dict]) -> None:
    with open("classes.json", "w") as f:
        json.dump(classes, f)


if __name__ == "__main__":
    update_classes()
