from sqlcrawl.helpers.db_add import connect

#CONSTANT
MIN_MATCHES = 5

def AddNewToCurrent(match_dict):
    if "match_date" in match_dict:
        matchDate = match_dict["match_date"]
        conn = connect()
        if conn:
            try:
                cur = conn.cursor()
            except:
                print("Error: Could Not Create A Database Cursor for MoveCurrentToPrevious")
                return False
            if cur:
                select_str = "SELECT id, rating, min_position, max_position, played_matches FROM elo_team ORDER BY rating DESC;"
                cur.execute(select_str)
                for index, record in enumerate(cur):
                    teamDict = {
                        "teamId": record[0],
                        "teamCurrentRanking": record[1],
                        "teamCurrentPosition": index + 1,
                        "teamMinPosition": record[2],
                        "teamMaxPosition": record[3],
                        "teamPlayedMatches": record[4],
                        "matchDate": matchDate
                    }
                    UpdateCurrent(teamDict)
                    CheckMaxMin(teamDict)
                try:
                    cur.close()
                    conn.close()
                except:
                    print("Error: Could Not Close Connection to DB for MoveCurrentToPrevious")
                    return False
            else:
                print("Error: No Cursor Object for MoveCurrentToPrevious")
                return False
        else:
            print("Error: No Connection to DB for MoveCurrentToPrevious")
            return False
    else:
        print("Error: No Match Date Provided To MoveCurrentToPrevious")
        return False


def CheckMaxMin(teamDict):
    if "teamId" in teamDict and "teamCurrentPosition" in teamDict and "teamCurrentRanking" in teamDict and "teamMinPosition" in teamDict and "teamMaxPosition" in teamDict and "teamPlayedMatches" in teamDict and "matchDate" in teamDict:
        currentRating = teamDict["teamCurrentRanking"]
        currentPosition = teamDict["teamCurrentPosition"]
        teamId = teamDict["teamId"]
        teamMaxPosition = teamDict["teamMaxPosition"]
        teamMinPosition = teamDict["teamMinPosition"]
        teamPlayedMatches = teamDict["teamPlayedMatches"]
        matchDate = teamDict["matchDate"]

        if currentPosition <= teamMaxPosition and teamPlayedMatches > MIN_MATCHES:
            print("Current Position: " + str(currentPosition) + " Team Max Position: " + str(teamMaxPosition))
            print("Played Matches: " + str(teamPlayedMatches))
            updatePosition = currentPosition
            updateRating = currentRating
            UpdateDate = matchDate
            update_string = "UPDATE elo_team SET max_rating=%s, max_position=%s, max_date='%s' WHERE id=%s;" % ( updateRating, updatePosition, UpdateDate, teamId)
            print(update_string)
        elif currentPosition >= teamMinPosition and teamPlayedMatches > MIN_MATCHES:
            print("Current Position: " + str(currentPosition) + " Team Min Position: " + str(teamMinPosition))
            updatePosition = currentPosition
            updateRating = currentRating
            UpdateDate = matchDate
            update_string = "UPDATE elo_team SET min_rating=%s, min_position=%s, min_date='%s' WHERE id=%s;" % ( updateRating, updatePosition, UpdateDate, teamId)
            print(update_string)
        else:
            return False

        conn = connect()
        if conn:
            try:
                cur = conn.cursor()
            except:
                print("Error: Could Not Create A Database Cursor for MoveCurrentToPrevious - CheckMaxMin")
                return False
            if cur:
                try:
                    cur.execute(update_string)
                    try:
                        conn.commit()
                        cur.close()
                        conn.close()
                    except:
                        print("Error: Could Not Close Connection to DB for MoveCurrentToPrevious - CheckMaxMin")
                        return False
                except:
                    print("Error: Could Not Excecute Update SQL for MoveCurrentToPrevious - CheckMaxMin")
        else:
            print("Error: No Connection to DB for MoveCurrentToPrevious - CheckMaxMin")
    else:
        print("Error: Not all Update Paramaters Present for MoveCurrentToPrevious - CheckMaxMin")
        return False


def UpdateCurrent(teamDict):
    if "teamId" in teamDict and "teamCurrentPosition" in teamDict and "teamCurrentRanking" in teamDict:
        currentRating = teamDict["teamCurrentRanking"]
        currentPosition = teamDict["teamCurrentPosition"]
        teamId = teamDict["teamId"]
        update_str = "UPDATE elo_team SET thisweek_rating=%s WHERE id=%s;" % (currentRating, teamId)
        update_str2 = "UPDATE elo_team SET thisweek_position=%s WHERE id=%s AND active=TRUE;" % (currentPosition, teamId)
        try:
            conn = connect()
            try:
                cur = conn.cursor()
                try:
                    cur.execute(update_str)
                    cur.execute(update_str)
                    conn.commit()
                    cur.close()
                    conn.close()
                except:
                    print("Error: Error Executing or Closing DB Connection for MoveCurrentToPrevious  - UpdateCurrent")
            except:
                print("Error: Could Not Create A Database Cursor for MoveCurrentToPrevious  - UpdateCurrent")
                return False
        except:
            print("Error: No Connection to DB for MoveCurrentToPrevious - UpdateCurrent")
    else:
        print("Error: Not all Update Paramaters Present for MoveCurrentToPrevious - UpdateCurrent")
        return False
