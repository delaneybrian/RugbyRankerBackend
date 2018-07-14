from sqlcrawl.helpers.db_add import connect

def SetInActiveTeams():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
        except:
            print("Error: Could Not Create A Database Cursor for UpdateLSetInActiveTeamsastWeek")
            return False
        if cur:
            select_str = "SELECT id, name FROM elo_team WHERE active=false;"
            cur.execute(select_str)
            cur2 = conn.cursor()
            for record in cur:
                id = record[0]
                insert_str = "UPDATE elo_team SET lastweek_rating = %s, thisweek_rating = %s, thisweek_position = %s, lastweek_position = %s WHERE id = %s;" % (5000, 5000, 500, 500, id)
                cur2.execute(insert_str)
            conn.commit()
            cur2.close()
            conn.close()

def UpdateLastWeek():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
        except:
            print("Error: Could Not Create A Database Cursor for UpdateLastWeek")
            return False
        if cur:
            select_str = "SELECT id, lastweek_rating FROM elo_team WHERE active=true ORDER BY lastweek_rating Desc;"
            cur.execute(select_str)
            cur2 = conn.cursor()
            i = 1
            for record in cur:
                id = record[0]
                insert_str = "UPDATE elo_team SET lastweek_position = %s WHERE id = %s;" % (i, id)
                cur2.execute(insert_str)
                i = i + 1
            conn.commit()
            cur2.close()
            conn.close()


def UpdateThisWeek():
    conn = connect()
    if conn:
        try:
            cur = conn.cursor()
        except:
            print("Error: Could Not Create A Database Cursor for UpdateThisWeek")
            return False
        if cur:
            select_str = "SELECT id, thisweek_rating FROM elo_team WHERE active=true ORDER BY thisweek_rating Desc;"
            cur.execute(select_str)
            cur2 = conn.cursor()
            i = 1
            for record in cur:
                id = record[0]
                insert_str = "UPDATE elo_team SET thisweek_position = %s WHERE id = %s;" % (i, id)
                cur2.execute(insert_str)
                i = i + 1
            conn.commit()
            cur2.close()
            conn.close()

def CalculatePositions():
    SetInActiveTeams()
    UpdateThisWeek()
    UpdateLastWeek()

CalculatePositions()
