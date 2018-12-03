import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from sqlcrawl.helpers.db_add import add_match
from sqlcrawl.helpers.get_ids import check_awayteam_name, check_hometeam_name, check_tournament_id

#PARAMATERS TO SET
tournament_name = "anglowelsh"

def create_url(start_year, end_year, page):

    url = "http://www.scorespro.com/rugby-union/ajaxdata.php?country=europe&comp=anglo-welsh-cup&league=&season=" + str(
        start_year) + '-' + str(end_year) + "&status=results&page=" + str(page)

    return url

def get_page_source(url):
        driver = webdriver.PhantomJS()
        driver.get(url)
        time.sleep(1)
        page_source = driver.page_source
        driver.close()
        return page_source

def format_month(date_str):
    try:
        date_str = str(date_str).strip().lower()
        date_dict = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
        if date_str in date_dict:
            return(date_dict[date_str])
        else:
            return None
    except:
        return None

def convert_to_datetime(date):
    date = str(date.text)
    date = date.split(' ')
    day = date[1].strip()
    month = date[2].strip()
    month = format_month(month)
    year = date[3].strip()
    date = datetime.datetime(int(year), int(month), int(day))
    return(date)

def extract_data(soup):
    match_sections = soup.findAll('div', {'class': 'compgrp'})

    count = 0
    match_soup = BeautifulSoup(str(match_sections[count]), 'html.parser')
    match_list = match_soup.findAll('tbody')
    for match in match_list:
        game_soup = BeautifulSoup(str(match), 'html.parser')
        date = game_soup.find('span', {'class': 'kick_t_dt'}).text.strip()

        game = game_soup.findAll('tr')
        if len(game) == 2:
            # HOMETEAM
            hometeam = BeautifulSoup(str(game[0]), "html.parser")
            # FIND HOMETEAM NAME
            hometeam_name = (hometeam.find('td', {'class': 'hometeam_rg'})).text.strip()
            # FIND HOMETEAM SCORE
            hometeam_score = (hometeam.find('td', {'class': 'ts_setB'})).text.strip()

            # AWAYTEAM
            awayteam = BeautifulSoup(str(game[1]), "html.parser")
            # FIND AWAYTEAM NAME
            awayteam_name = (awayteam.find('td', {'class': 'awayteam_rg'})).text.strip()
            # FIND AWAYTEAM SCORE
            awayteam_score = (awayteam.find('td', {'class': 'ts_setB'})).text.strip()

            # Find Tournament
            tournament = tournament_name

            date = str(date).replace(".", "-")
            numbers = date.split('-')
            year = int('20' + str(numbers[2]))
            dateforid = str(year) + numbers[1] + numbers[0]

            # MatchID
            match_id = dateforid + hometeam_name.lower().replace(" ", "") + awayteam_name.replace(" ","").lower()
            match_id = match_id.replace("'", "")
            match_id = match_id.replace('"', "")


            format_to_dict(date, hometeam_name, hometeam_score, awayteam_name, awayteam_score, tournament_name, match_id)

    count += 1


def format_to_dict(date, hometeam, hometeam_score, awayteam, awayteam_score, torunament, match_id):
    post = {
        "hometeam": hometeam,
        "hometeam_score": str(hometeam_score),
        "awayteam": awayteam,
        "awayteam_score": str(awayteam_score),
        "match_date": date,
        "_id": match_id,
        "tournament": torunament,
        "added_on": datetime.datetime.utcnow()
    }
    #print(post)
    save_to_database(post)

def save_to_database(post):
    print("Saving Match To Database...")
    hometeam_id = check_hometeam_name(post)
    awayteam_id = check_awayteam_name(post)
    tournament_id = check_tournament_id(post)
    if hometeam_id and awayteam_id and tournament_id:
        post["hometeam_id"] = hometeam_id
        post["awayteam_id"] = awayteam_id
        post["tournament_id"] = tournament_id
        add_match(post)
    elif not hometeam_id:
        print("Error: Could Not Match Hometeam")
        return False
    elif not awayteam_id:
        print("Error: Could Not Match Awayteam")
        return False
    else:
        print("Error: Cannot Match Tourmanemt")
        return False

# CUSTOM FOR ANGLO WELSH CUP
def start_crawl(current_year, start_page, endyear):
    print("Now Crawling: " + tournament_name)
    skip = 1
    while current_year > endyear and skip < 3:
        previous_year = current_year - 1
        while start_page < 10:
            url = create_url(previous_year, current_year, start_page)
            page_source = get_page_source(url)
            soup = BeautifulSoup(page_source, 'html.parser')
            body = soup.find('div', {'class': 'no_data'})
            if body:
                break
            extract_data(soup)
            start_page += 1
        start_page = 1

        url = create_url(previous_year, current_year, start_page)
        page_source = get_page_source(url)
        soup = BeautifulSoup(page_source, 'html.parser')
        body = soup.find('body')
        if len(body.text) < 100:
            skip += 1
            current_year -= 1
        else:
            current_year -= 1
