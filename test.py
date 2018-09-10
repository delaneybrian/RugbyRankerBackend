from sqlcrawl.xmlcrawlers.avivapremiership import start_crawl as top14_crawl

start_page = 1
current_year = 2019
endyear = 2018

top14_crawl(current_year, start_page, endyear)