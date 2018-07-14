from sqlcrawl.helpers.db_add import connect

#SUPPORT FUNCTION
def update_rivals(sample):
    print("Updating Rivals Table")
    if sample['hometeam_score'] == sample['awayteam_score']:
        #print("Draw")
        update_string1 = "UPDATE elo_rivals SET draws = draws + 1 WHERE team_a_id = '%s' AND team_b_id = '%s';" % ((sample['hometeam_id']), (sample['awayteam_id']))
        sql_statements = [update_string1]
        return (sql_statements)
    elif sample['hometeam_score'] > sample['awayteam_score']:
        #print("Home win for: " + sample["hometeam_id"])
        update_string1 = "UPDATE elo_rivals SET wins = wins + 1 WHERE team_a_id = '%s' AND team_b_id = '%s';" % ((sample['hometeam_id']), (sample['awayteam_id']))
        update_string2 = "UPDATE elo_rivals SET losses = losses + 1 WHERE team_a_id = '%s' AND team_b_id = '%s';" % ((sample['awayteam_id']), (sample['hometeam_id']))
        sql_statements = [update_string1, update_string2]
        return (sql_statements)
    else:
        #print("Away win for: " + sample["awayteam_id"])
        update_string1 = "UPDATE elo_rivals SET wins = wins + 1 WHERE team_a_id = '%s' AND team_b_id = '%s';" % ((sample['awayteam_id']), (sample['hometeam_id']))
        update_string2 = "UPDATE elo_rivals SET losses = losses + 1 WHERE team_a_id = '%s' AND team_b_id = '%s';" % ((sample['hometeam_id']), (sample['awayteam_id']))
        sql_statements = [update_string1, update_string2]
        return(sql_statements)

#SUPPORT FUNCTION
def create_rivals(sample):
    print("Creating Rivals...")
    insert_string_first_team = "INSERT INTO elo_rivals (team_a_id, team_b_id, wins, draws, losses) VALUES ('%s', '%s', '%s', '%s', '%s');" % ((sample['hometeam_id']), (sample['awayteam_id']), 0, 0, 0)
    insert_string_second_team = "INSERT INTO elo_rivals (team_a_id, team_b_id, wins, draws, losses) VALUES ('%s', '%s', '%s', '%s', '%s');" % ((sample['awayteam_id']), (sample['hometeam_id']), 0, 0, 0)
    sql_statements = [insert_string_first_team, insert_string_second_team]
    return(sql_statements)

#MAIN FUNCTION
def calculate_rivals(sample):
    if ('hometeam_id' in sample.keys() and 'awayteam_id' in sample.keys() and 'awayteam_score' in sample.keys() and 'hometeam_score' in sample.keys()):
        print("Calculating Rivals...")
        conn = connect()
        if conn:
            cur = conn.cursor()
            select_string = "SELECT * FROM elo_rivals WHERE team_a_id = '%s' AND team_b_id = '%s';" % ((sample['hometeam_id']), (sample['awayteam_id']))
            #print(select_string)
            try:
                cur.execute(select_string)
                result = cur.fetchone()
                if result:
                    statements = update_rivals(sample)
                    for statement in statements:
                        try:
                            #print(statement)
                            cur.execute(statement)
                            conn.commit()
                            print("Sucess: Rivalry Updated")
                        except:
                            print("Error: Could Not Commit Changes")
                            return False
                    try:
                        cur.close()
                        conn.close()
                    except:
                        print("Error: Could Not Close DB Connection")
                        return False
                else:
                    statements = create_rivals(sample)
                    for statement in statements:
                        try:
                            #print(statement)
                            cur.execute(statement)
                            conn.commit()
                            print("Sucess: Rivalry Created")
                        except:
                            print("Error: Could Not Commit Changes")
                            return False
                    try:
                        cur.close()
                        conn.close()
                    except:
                        print("Error: Could Not Close DB Connection")
                        return False
                    calculate_rivals(sample)
            except:
                print("Error: Could Not Execute SQL command to see if rivals already exist")
                return False
        else:
            print("Error: Could Not Establish Database Connection")
            return False
    else:
        print("Error: Not Enough Information To Complete Rivals Table")
        return False











