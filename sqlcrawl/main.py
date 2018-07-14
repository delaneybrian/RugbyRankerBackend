import datetime


#IMPORT CRAWLERS
from sqlcrawl.xmlcrawlers.top14 import start_crawl as top14_crawl
from sqlcrawl.xmlcrawlers.superrugby import start_crawl as superrugby_crawl
from sqlcrawl.xmlcrawlers.prod2 import start_crawl as prod2_crawl
from sqlcrawl.xmlcrawlers.pro12 import start_crawl as pro12_crawl
from sqlcrawl.xmlcrawlers.championscup import start_crawl as championscup_crawl
from sqlcrawl.xmlcrawlers.challangecup import start_crawl as challangecup_crawl
from sqlcrawl.xmlcrawlers.avivapremiership import start_crawl as avivapremiership_crawl
from sqlcrawl.xmlcrawlers.anglowelsh import start_crawl as anglowelsh_crawl
from sqlcrawl.xmlcrawlers.pro14 import start_crawl as pro14_crawl


def start_all_crawlers():
    start_page = 1
    current_year = 2018
    #CHANGE END YEAR TO CRAWL ENTIRE THING
    endyear = 2017
    #endyear = 2010

    anglowelsh_crawl(current_year, start_page, endyear)
    avivapremiership_crawl(current_year, start_page, endyear)
    championscup_crawl(current_year, start_page, endyear)
    challangecup_crawl(current_year, start_page, endyear)
    #pro12_crawl(current_year, start_page, endyear)
    prod2_crawl(current_year, start_page, endyear)
    superrugby_crawl(current_year, start_page, endyear)
    top14_crawl(current_year, start_page, endyear)
    pro14_crawl(current_year, start_page, endyear)
