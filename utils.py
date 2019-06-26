# author: Kaan Eraslan
# purpose: scrape data from topos texts
# No warranties, see LICENSE

import os
from bs4 import BeautifulSoup


def getProjectRawData(projectName: str):
    curdir = os.path.curdir
    rawdata = os.path.join(curdir, "rawData")
    return os.path.join(rawdata, projectName)


def readInHtml(htmlpath: str):
    "Read topos text html"
    with open(htmlpath, 'r', encoding="utf-8") as f:
        page = BeautifulSoup(f, "lxml")
    return page


def getProjectHtmlSavePath(projectName: str):
    "get html save path"
    curdir = os.path.curdir
    assetdir = os.path.join(curdir, "assets")
    htmlpath = os.path.join(assetdir, 'htmlpages')
    return os.path.join(htmlpath, projectName)


def getProjectLogPath(projectName: str):
    "get log path"
    curdir = os.path.curdir
    assetdir = os.path.join(curdir, "assets")
    logdir = os.path.join(assetdir, 'logs')
    return os.path.join(logdir, projectName)


def getProjectJsonPath(projectName: str):
    ""
    curdir = os.path.curdir
    assetdir = os.path.join(curdir, "assets")
    jsondir = os.path.join(assetdir, 'jsonfiles')
    return os.path.join(jsondir, projectName)


def saveLog(logpath: str, element: str):
    "Save last scraped link to log"
    with open(logpath, "a",
              encoding="utf-8",
              newline="\n") as log:
        log.writelines(["\n", element])


def getLogElements(logpath):
    "obtain work section page links from log"
    with open(logpath, 'r',
              encoding="utf-8",
              newline='\n') as log:
        elements = log.readlines()
    return elements
