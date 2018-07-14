import psycopg2
from sqlcrawl.helpers.db_add import connect


def updateMatchRatingValues(hometeam_rating_before, awayteam_rating_before, hometeam_rating_after, awayteam_rating_after, match_id):
    if hometeam_rating_before and awayteam_rating_before and hometeam_rating_after and awayteam_rating_after and match_id:
        conn = connect()
        if conn:
            try:
                cur = conn.cursor()
            except:
                print("Error: Could Not Create A Database Cursor")
                return False
            if cur:
                insert_str = ("UPDATE elo_match SET hometeam_rating_before=%s, awayteam_rating_before=%s, hometeam_rating_after=%s, awayteam_rating_after=%s WHERE id=('%s');") % (hometeam_rating_before, awayteam_rating_before, hometeam_rating_after, awayteam_rating_after, match_id)
                try:
                    cur.execute(insert_str)
                    conn.commit()
                except:
                    print("Error: Could Not Execute SQL Statement For Match Team Rating Update")
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
    else:
        print("Error: Not All Values Present To Update Match Team Ratings")
        return False