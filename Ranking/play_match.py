#Nessesary Imports
import math
from sqlcrawl.helpers.db_add import connect
from Ranking.rivals import calculate_rivals
from Ranking.date_test import date_checker
from Ranking.streak import streak
from Ranking.updateMatchRatingValues import updateMatchRatingValues
from Ranking.MoveCurrentToPrevious import MoveCurrentToPrevious
from Ranking.AddNewToCurrent import AddNewToCurrent

#Define DB Connection Variables
HOST = 'localhost'
DBNAME = 'rugbyrank'
USER = 'briandelaney'
PASSWORD = 'quqaiwii1!'


#Define Global Variables
Home_Advantage = 50
Denominator = 400

tournament_rating_dict = {
    1: 30, #Guinness PRO12
    2: 35, #Aviva Premiership
    3: 35, #Top 14
    4: 25, #Rugby Pro D2
    5: 50, #European Rugby Champions Cup
    6: 40, #European Rugby Challenge Cup
    7: 30, #Eccellenza
    8: 30, #Anglo-Welsh Cup
    9: 45, #Super Rugby
}
default_tournament_rating = 40


#TAKES AN INSTANCE OF A MATCH RECORD AND RETURNS DICTIONARY OF TEAMIDS AND TEAMSCORES
def get_team_scores_and_ids(record):
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
        except:
            print("Error: Could not get database cursor")
            return False
        if cur:
            try:
                hometeam_score = str(record[1])
                awayteam_score = str(record[2])
                match_date = str(record[3])
                match_id = str(record[0])

                #GET HOMETEAM ID
                home_select_str = "SELECT hometeam_id FROM elo_match WHERE id = '%s';" % (match_id)
                print(home_select_str)
                cur.execute(home_select_str)
                for record in cur:
                    hometeam_id = str(record[0])

                #GET AWAYTEAM ID
                away_select_str = "SELECT awayteam_id FROM elo_match WHERE id = '%s';" % (match_id)
                print(away_select_str)
                cur.execute(away_select_str)
                for record in cur:
                    awayteam_id = str(record[0])
                try:
                    conn.commit()
                    cur.close()
                    conn.close()

                    #CREATE DICTIONARY OF INFORMATION TO RETURN
                    if hometeam_id and hometeam_score and awayteam_id and awayteam_score:
                        info_dict = {
                            "hometeam_id" : hometeam_id,
                            "hometeam_score" : hometeam_score,
                            "awayteam_id" : awayteam_id,
                            "awayteam_score" : awayteam_score,
                            "match_id" : match_id,
                            "match_date" : match_date,
                        }
                        return info_dict
                    else:
                        print("Error: Not all values present to create dictionay")
                        return False
                except:
                    print("Error: Could not Commit Changes")
                    return False
            except:
                print("Error: Could not Execute SQL Statement")
                return False
        else:
            print("Error: No Cursor Object")
            return False
    else:
        print("Error: No Connection")
        return False


#TAKES NO INPUT BUT RETURNS LIST OF ALL MATCHES WHERE CALCULATIONS HAVE NOT YET BEEN PERFORMED
def get_matches_to_calculate():
    list_of_matches = []
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
        except:
            print("Error: Could not get database cursor")
            return False
        if cur:
            try:
                select_str = "SELECT * FROM elo_match WHERE calculated = False ORDER BY match_date;"
                cur.execute(select_str)
                for record in cur:
                    list_of_matches.append(record)
                try:
                    conn.commit()
                    cur.close()
                    conn.close()
                    return(list_of_matches)
                except:
                    print("Error: Could not Commit Changes")
                    return False
            except:
                print("Error: Could not Execute SQL Statement")
                return False
        else:
            print("Error: No Cursor Object")
            return False
    else:
        print("Error: No Connection")
        return False



#FUNCTION WHICH IS GIVEN DICTIONARY OF TEAM_IDS AND TEAM_SCORES AND GETS RATINGS FOR BOTH TEAMS RETURNS DICT OF ALL INFORMATION
def get_team_ratings(dict):
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
        except:
            print("Error: Could not get database cursor")
            return False
        if cur:
            try:
                hometeam_id = dict['hometeam_id']
                awayteam_id = dict['awayteam_id']

                #GET HOMETEAM RATING
                home_select_str = "SELECT rating FROM elo_team WHERE id = '%s';" % (hometeam_id)
                cur.execute(home_select_str)
                for record in cur:
                    hometeam_rating = str(record[0])
                    dict["hometeam_rating"] = hometeam_rating

                #GET AWAYTEAM RATING
                away_select_str = "SELECT rating FROM elo_team WHERE id = '%s';" % (awayteam_id)
                cur.execute(away_select_str)
                for record in cur:
                    awayteam_rating = str(record[0])
                    dict["awayteam_rating"] = awayteam_rating

                #COMMIT AND CLOSE
                try:
                    conn.commit()
                    cur.close()
                    conn.close()
                    if dict:
                        return dict
                    else:
                        print("Error: Ratings Not Returned")
                        return False
                except:
                    print("Error: Could not Commit Changes")
                    return False
            except:
                print("Error: Could not Execute SQL Statement")
                return False
        else:
            print("Error: No Cursor Object")
            return False
    else:
        print("Error: No Connection")
        return False



def upload_newratings(dict):
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
        except:
            print("Error 3: Could not get database cursor")
            return False
        if cur:
            try:
                insert_home_rating_str = "UPDATE elo_team SET rating = %s WHERE id = '%s';" % (dict["hometeam_rating"], dict["hometeam_id"])
                cur.execute(insert_home_rating_str)
                insert_away_rating_str = "UPDATE elo_team SET rating = %s WHERE id = '%s';" % (dict["awayteam_rating"], dict["awayteam_id"])
                cur.execute(insert_away_rating_str)

                #COMMIT AND CLOSE
                try:
                    conn.commit()
                    print("Hometeam Team ID: " + dict["hometeam_id"] + " Rating Updated To: " + str(dict["hometeam_rating"]))
                    print("Hometeam Team ID: " + dict["awayteam_id"] + " Rating Updated To: " + str(dict["awayteam_rating"]))
                    cur.close()
                    conn.close()
                    return True
                except:
                    print("Error 3: Could not Commit Changes")
                    return False
            except:
                print("Error 3: Could not Execute SQL Statement")
                return False
        else:
            print("Error 3: No Cursor Object")
            return False
    else:
        print("Error 3: No Connection")
        return False


def calculate_ratings(dict, Match_Weight):
    #convert strings to ints if necessary
    try:
        dict["hometeam_rating"] = int(dict["hometeam_rating"])
        dict["hometeam_score"] = int(dict["hometeam_score"])
        dict["awayteam_rating"] = int(dict["awayteam_rating"])
        dict["awayteam_score"] = int(dict["awayteam_score"])
    except:
        print("Error: Incorrect Input to Rating System")
        return False

    #Home Team Wins
    if dict["hometeam_score"] > dict["awayteam_score"]:

        #Margin of Victory - NEED TO PROTECT AGAINST 0 DIVISION
        if dict["hometeam_score"] == 0:
            MoV = 2
        elif dict["awayteam_score"] == 0:
            MoV = 2
        else:
            MoV = dict["hometeam_score"] / dict["awayteam_score"]
            if MoV > 2:
                MoV = 2


        #Outcome
        home_outcome = 1
        away_outcome = 0

        # Expectation of Victory
        dr_home = (dict["hometeam_rating"] + Home_Advantage) - dict["awayteam_rating"]
        dr_away = dict["awayteam_rating"] - (dict["hometeam_rating"] + Home_Advantage)
        e_home = 1 / (1 + math.pow(10, ((-1 * dr_home) / Denominator)))
        e_away = 1 / (1 + math.pow(10, ((-1 * dr_away) / Denominator)))

        #Calculate Points Change
        new_rating_home = dict["hometeam_rating"] + (Match_Weight * MoV * (home_outcome - e_home))
        new_rating_away = dict["awayteam_rating"] + (Match_Weight * MoV * (away_outcome - e_away))


        #update ratings
        dict["hometeam_rating"] = new_rating_home
        dict["awayteam_rating"] = new_rating_away

        return dict

    #Away Team Wins
    elif dict["hometeam_score"] < dict["awayteam_score"]:

        # Margin of Victory - NEED TO PROTECT AGAINST 0 DIVISION
        if dict["hometeam_score"] == 0:
            MoV = 2
        elif dict["awayteam_score"] == 0:
            MoV = 2
        else:
            MoV = dict["awayteam_score"] / dict["hometeam_score"]
            if MoV > 2:
                MoV = 2


        #Outcome
        home_outcome = 0
        away_outcome = 1

        # Expectation of Victory
        dr_home = (dict["hometeam_rating"] + Home_Advantage) - dict["awayteam_rating"]
        dr_away = dict["awayteam_rating"] - (dict["hometeam_rating"] + Home_Advantage)
        e_home = 1 / (1 + math.pow(10, ((-1 * dr_home) / Denominator)))
        e_away = 1 / (1 + math.pow(10, ((-1 * dr_away) / Denominator)))

        # Calculate Points Change
        new_rating_home = dict["hometeam_rating"] + (Match_Weight * MoV * (home_outcome - e_home))
        new_rating_away = dict["awayteam_rating"] + (Match_Weight * MoV * (away_outcome - e_away))

        # update ratings
        dict["hometeam_rating"] = new_rating_home
        dict["awayteam_rating"] = new_rating_away

        return dict

    #Match is Drawn
    else:

        #Margin of Victory
        MoV = 1

        #Outcome
        home_outcome = 0.5
        away_outcome = 0.5

        #Expectation of Victory
        dr_home = (dict["hometeam_rating"] + Home_Advantage) - dict["awayteam_rating"]
        dr_away = dict["awayteam_rating"] - (dict["hometeam_rating"] + Home_Advantage)
        e_home = 1/(1 + math.pow(10, ((-1 * dr_home)/Denominator)))
        e_away = 1/(1 + math.pow(10, ((-1 * dr_away)/Denominator)))

        # Calculate Points Change
        new_rating_home = dict["hometeam_rating"] + (Match_Weight * MoV * (home_outcome - e_home))
        new_rating_away = dict["awayteam_rating"] + (Match_Weight * MoV * (away_outcome - e_away))



        # update ratings
        dict["hometeam_rating"] = new_rating_home
        dict["awayteam_rating"] = new_rating_away

        return dict


def update_calculated(dict):
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
        except:
            print("Error: Could not get database cursor")
            return False
        if cur:
            try:
                 insert__cal_str = "UPDATE elo_match SET calculated = True WHERE id = '%s';" % (dict["match_id"])
                 cur.execute(insert__cal_str)
                 try:
                     conn.commit()
                     cur.close()
                     conn.close()
                     return True
                 except:
                     print("Error: Could not Commit Changes")
                     return False
            except:
                print("Error: Could not Execute SQL Statement")
                return False
        else:
            print("Error: No Cursor Object")
            return False
    else:
        print("Error: No Connection")
        return False


#CALCULATE TOURNAMENT RATING GIVEN ID

#if tournament has a rating return rating for tournament else return default rating
def get_tournament_rating(tournament_id):
    if tournament_id in tournament_rating_dict:
        return (tournament_rating_dict[tournament_id])
    else:
        print("Used Default Rating")
        return default_tournament_rating



#GET TOURNAMENT RATING - gets a dict for a match and returns the tournament rating
def get_tornament_id(dict):
    if dict["match_id"]:
        conn = connect()
        if conn:
            try:
                cur = conn.cursor()
            except:
                print("Error: Could Not Create A Database Cursor")
                return False
            if cur:
                select_str = ("SELECT tournament_id FROM elo_match WHERE id=('%s');") % dict["match_id"]
                cur.execute(select_str)
                for record in cur:
                    tournament_id = int(record[0])
                    tournament_rating_value = get_tournament_rating(tournament_id)
                    return tournament_rating_value
                try:
                    cur.close()
                    conn.close()
                except:
                    print("Error: Could Not Close Connection to DB")
                    return False
            else:
                print("Error: No Cursor Object")
                return False
    else:
        print("Error: No Connection")
        return False




#INITIATE ANALYSIS
def initate_analysis():
    matches = get_matches_to_calculate()
    print("Number of matches to calculate: " + str(len(matches)))

    if matches:

        #For initial run - INITIAL DATE and turn off time zone information
        compare_date = matches[0][3]
        compare_date = compare_date.replace(tzinfo=None)

        for match in matches:
            #Gets relevant team ids
            dict = (get_team_scores_and_ids(match))
            # GET TOURNAMENT RATING VALUE
            Match_Weight = get_tornament_id(dict)
            #Gets current team ratings
            dict = get_team_ratings(dict)

            try:
                hometeam_rating_before = dict["hometeam_rating"]
                awayteam_rating_before = dict["awayteam_rating"]
                match_id = dict["match_id"]
            except:
                print("Error: Not All Info Present Before Match To Store Rating Changes")

            #Calculates New Rating
            dict = calculate_ratings(dict, Match_Weight)

            try:
                hometeam_rating_after = dict["hometeam_rating"]
                awayteam_rating_after = dict["awayteam_rating"]
                updateMatchRatingValues(hometeam_rating_before, awayteam_rating_before, hometeam_rating_after, awayteam_rating_after, match_id)
            except:
                print("Error: Not All Info Present Before Match To Store Rating Changes")

            #uploads new ratings to the db
            upload_newratings(dict)
            # Calculates Winning Streaks
            streak(dict)
            #add match to rivals table
            calculate_rivals(dict)
            #updates calcaulted field in match database to ensure it is not double counted
            update_calculated(dict)

            #FOR INITIAL RUNS - UPDATE TIME STAMP ON A WEEKLY BASIS
            compare_date = date_checker(dict, compare_date)

        #for last run do this
        if dict:
            #last match
            print("Last Match Calculations")
            MoveCurrentToPrevious()
            AddNewToCurrent(dict)

#START ANALYSIS
initate_analysis()

