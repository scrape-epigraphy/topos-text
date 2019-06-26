# author: Kaan Eraslan
# purpose: scrape data from topos texts
# No warranties, see LICENSE

import requests
import json
import os
import glob
from time import sleep
from utils import getProjectHtmlSavePath
from utils import getProjectJsonPath
from utils import getProjectLogPath
from utils import getProjectRawData
from utils import readInHtml
from utils import saveLog


"""
Input: toposText html file

General Approach:
For all the work links in the table:
1. Parse out the work section id from the link: tip it comes after #
    like www.topostext.org/somework/workpage#sectionId

2. Construct the work page link.
3. Go to work page link
4. find the div tag with id equal to section id.
5. Get canonical section id from the paragraph under div tag.
6. Search for all the place ids attested under the div tag.
    tip: place id anchors contain an attribute called 'about'
    which gives a link to the page of the place. 
    Ex: about="https://topostext.org/place/375227ULer"

7. Parse the place id from the given link
8. Search the place id in the toposText.kml document
9. Get pleaides ID of the place as well if it exists.
10. Get the coordinates of the place from point > coordinates tag
11. Get the name of the place
12. Place these informations on geojson file.
13. Repeat it for other text links

The final geojson file should contain:
For each place:
    name: name of the place taken from kml
    coordinate: coordinate of the place taken from kml
    properties: {"toposTextPlaceId": toposText id taken from kml,
                 "pleiadesId": pleiades id taken from kml,
                 "toposTextWorkId": toposTextWork id taken from html table,
                 "workSectionId": urn taken from the paragraph of the section,
                 "workSection": the content of the paragraph,
                 }
In works that are open in those links,
we search for all the place attestations.
Then we save those attestations.
"""


def getWorkIdSectionId(workLink: str):
    "From work link get work id and section id"
    burl = "topostext.org"
    workbase = "/work/"
    sectionPos = workLink.find("#")
    workUrl = burl + workbase
    workUrlPos = workLink.find(workUrl)
    workId = workLink[workUrlPos+len(workUrl):sectionPos]
    sectionId = workLink[sectionPos+1:]
    return {"toposTextWorkId": workId,
            "toposTextWorkSectionId": sectionId,
            "toposTextWorkSectionLink": workLink}


def findWorkLinks(page) -> [str]:
    "find works in page"
    works = page.find_all("a",
                          href=lambda x: "/work/" in x)
    return [work['href'] for work in works]


def saveWorkSectionLink(jsonpath: str,
                        workSectionDicts: [dict]):
    with open(jsonpath, "w", encoding="utf-8", newline="\n") as jf:
        json.dump(workSectionDicts, jf,
                  indent=2, ensure_ascii=False)


def saveWork(workId: int,
             logpath: str,
             savepath: str):
    "save works to savepath"
    name = str(workId) + ".html"
    savename = os.path.join(savepath, name)
    savefileStart = """<html><head><meta charset="utf-8"/></head><body>"""
    savefileEnd = """</body></html>"""
    workPageUrl = "https://topostext.org/ajax/loadParagraphs.php"
    payload = {"work_id": workId}
    resp = requests.get(workPageUrl, params=payload)
    if resp.status_code == 200:
        savefile = savefileStart + resp.text + savefileEnd
        with open(savename, "w", encoding="utf-8", newline="\n") as f:
            f.write(savefile)
        saveLog(logpath, name)
    return


def saveWorks(workDicts: [dict],
              savepath: str,
              logpath: str):
    "Save work section pages"
    workidSet = set()
    for workDict in workDicts:
        workId = int(workDict["toposTextWorkId"])
        if workId not in workidSet:
            workidSet.add(workId)
            saveWork(workId, logpath, savepath)
        sleep(1)


def main():
    projectName = 'toposText'
    rawdataPath = getProjectRawData(projectName)
    htmlp = os.path.join(rawdataPath, 'toposTextData.html')
    page = readInHtml(htmlp)
    wlinks = findWorkLinks(page)
    workSectionIds = [getWorkIdSectionId(wlink) for wlink in wlinks]
    jsonpath = getProjectJsonPath(projectName)
    jsonpath = os.path.join(jsonpath, "toposTextWorkSection.json")
    saveWorkSectionLink(jsonpath, workSectionIds)
    savepath = getProjectHtmlSavePath(projectName)
    logpath = getProjectLogPath(projectName)
    logpath = os.path.join(logpath, 'workLogs.txt')
    workPagePath = os.path.join(savepath, 'works')
    saveWorks(workSectionIds,
              workPagePath,
              logpath)


if __name__ == '__main__':
    main()
