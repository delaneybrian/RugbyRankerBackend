import datetime
from Ranking.AddNewToCurrent import AddNewToCurrent
from Ranking.MoveCurrentToPrevious import MoveCurrentToPrevious

def convert_date(match_dict):
    match_date = match_dict["match_date"].split(' ')
    match_date = match_date[0].split('-')
    match_date = datetime.datetime(int(match_date[0]), int(match_date[1]), int(match_date[2]))
    return match_date

def date_checker(match_dict, compare_date):

    match_date = convert_date(match_dict)

    print("Match Date: " + str(match_date))
    print("Compare Date " + str(compare_date))

    if ((match_date - compare_date) < datetime.timedelta(days=7)):
        print("Inside Range")
        #DO NOTHING?
        return compare_date
    else:
        print("Outside Range")
        compare_date = match_date
        #DO SOMETHING WITH TABLES
        MoveCurrentToPrevious()
        AddNewToCurrent(match_dict)
        return compare_date





