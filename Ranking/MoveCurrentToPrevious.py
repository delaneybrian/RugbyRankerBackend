from sqlcrawl.helpers.db_add import connect

def MoveCurrentToPrevious():
        conn = connect()
        if conn:
            try:
                cur = conn.cursor()
            except:
                print("Error: Could Not Create A Database Cursor for MoveCurrentToPrevious")
                return False
            if cur:
                select_str = "SELECT id, thisweek_rating, thisweek_position FROM elo_team;"
                cur.execute(select_str)
                for record in cur:
                    UpdatePrevious(record)
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

def UpdatePrevious(record):
    teamId = record[0]
    previousRating = record[1]
    previousPosition = record[2]
    update_str = "UPDATE elo_team SET lastweek_rating=%s WHERE id=%s;" % (previousRating, teamId)
    update_str2 = "UPDATE elo_team SET lastweek_position=%s WHERE id=%s AND active=TRUE;" % (previousPosition, teamId)
    try:
        conn = connect()
        try:
            cur = conn.cursor()
            try:
                cur.execute(update_str)
                cur.execute(update_str2)
                conn.commit()
                cur.close()
                conn.close()
            except:
                print("Error: Error Executing or Closing DB Connection for MoveCurrentToPrevious  - UpdatePrevious")
        except:
            print("Error: Could Not Create A Database Cursor for MoveCurrentToPrevious  - UpdatePrevious")
            return False
    except:
        print("Error: No Connection to DB for MoveCurrentToPrevious - UpdatePrevious")
