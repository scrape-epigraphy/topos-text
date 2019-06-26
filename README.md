# topos-text
scrape works from topostext.org

## Usage Guide

### Installation

Required packages are:

- `beautifulsoup4`
  
  - `pip install beautifulsoup4`

- `requests`

  - `pip install requests`


### Scraping

Scraper assumes the following: 

- You are trying to get the content of a list of works related to some query you
did. Resulting in an html page more or less like that in
`rawData/toposText/toposTextData.html`

If these are true:

- simply copy paste your html page to `rawData/toposText/`
- rename the new page to `toposTextData.html`
- run `python toposTextWorkScraper.py` in main directory from command line


