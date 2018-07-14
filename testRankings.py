import math
Home_Advantage = 50
Denominator = 400
Match_Weight = 50

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



dict = {
    "hometeam_rating" : 1874,
    "hometeam_score" : 23,
    "awayteam_rating" : 2,
    "awayteam_score" : 247
}

ratings = calculate_ratings(dict ,Match_Weight)
print(ratings)
