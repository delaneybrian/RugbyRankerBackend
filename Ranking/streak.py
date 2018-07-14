from sqlcrawl.helpers.db_add import connect

def streak(dict):
    print(dict)
    if "hometeam_id" in dict and "awayteam_id" in dict and "awayteam_score" in dict and "hometeam_score" in dict:
        conn = connect()
        if conn:
            print("Connection to Database Established")
            cur = conn.cursor()

            # SECTION TO GET STREAKS
            select_string = "SELECT current_streak, max_streak, played_matches FROM elo_team WHERE id = %s;" % (dict['hometeam_id'])
            try:
                cur.execute(select_string)
                result = cur.fetchone()
                hometeamCurrentStreak = (result[0])
                hometeamMaxStreak = (result[1])
                homePlayedMatches = (result[2])
            except:
                print("Error: Could Not Get Hometeam Streak")
                return False
            select_string = "SELECT current_streak, max_streak, played_matches FROM elo_team WHERE id = %s;" % (dict['awayteam_id'])
            try:
                cur.execute(select_string)
                result = cur.fetchone()
                awayteamCurrentStreak = (result[0])
                awayteamMaxStreak = (result[1])
                awayPlayedMatches = (result[2])
            except:
                print("Error: Could Not Get Awayteam Streak")
                return False

            #SECTION TO UPDATE STREAK VARIABLES
            if dict['hometeam_score'] > dict['awayteam_score']:
                hometeamCurrentStreak = hometeamCurrentStreak + 1
                if hometeamCurrentStreak > hometeamMaxStreak:
                    hometeamMaxStreak = hometeamMaxStreak + 1
                awayteamCurrentStreak = 0
            elif dict['hometeam_score'] < dict['awayteam_score']:
                awayteamCurrentStreak = awayteamCurrentStreak + 1
                if awayteamCurrentStreak > awayteamMaxStreak:
                    awayteamMaxStreak = awayteamMaxStreak + 1
                hometeamCurrentStreak = 0
            else:
                hometeamCurrentStreak = 0
                awayteamCurrentStreak = 0


            #SECTION TO UPDATE PLAYED MATCHES
            homePlayedMatches = homePlayedMatches + 1
            awayPlayedMatches = awayPlayedMatches + 1


            # PRINT STREAKS
            #print("************** Current Streak *************")
            #print("hometeamCurrentStreak " + str(dict['hometeam_id']) + ": " + str(hometeamCurrentStreak))
            #print("awayteamCurrentStreak " + str(dict['awayteam_id']) + ": " + str(awayteamCurrentStreak))
            #print("hometeamMaxStreak " + str(dict['hometeam_id']) + ": " + str(hometeamMaxStreak))
            #print("awayteamMaxStreak " + str(dict['awayteam_id']) + ": " + str(awayteamMaxStreak))


            # UPDATE STREAK IN DATABASE
            insert_string = "UPDATE elo_team SET current_streak = %s, max_streak = %s WHERE id = %s;" % (hometeamCurrentStreak, hometeamMaxStreak, dict['hometeam_id'])
            try:
                cur.execute(insert_string)
            except:
                print("Error: Could Not Update Streak For Hometeam")
                return False
            insert_string = "UPDATE elo_team SET current_streak = %s, max_streak = %s WHERE id = %s;" % (awayteamCurrentStreak, awayteamMaxStreak, dict['awayteam_id'])
            try:
                cur.execute(insert_string)
            except:
                print("Error: Could Not Update Streak For Awayteam")
                return False
            try:
                conn.commit()
            except:
                print('Error: Could Not Commit Update To Streak')

            # UPDATE PLAYED MATCHES IN DATABASE
            insert_string = "UPDATE elo_team SET played_matches = %s WHERE id = %s;" % (homePlayedMatches, dict['hometeam_id'])
            try:
                cur.execute(insert_string)
            except:
                print("Error: Could Not Update Played Matches For Hometeam")
                return False
            insert_string = "UPDATE elo_team SET played_matches = %s WHERE id = %s;" % (awayPlayedMatches, dict['awayteam_id'])
            try:
                cur.execute(insert_string)
            except:
                print("Error: Could Not Update Played Matches For Awayteam")
                return False
            try:
                conn.commit()
            except:
                print('Error: Could Not Commit Update To Played Matches For Team')

            try:
                cur.close()
                conn.close()
            except:
                print('Error: Could not close database connection for streak')
        else:
            print("Error: Could Not Establish Connection To Database")
            return False


matches = [
{'awayteam_id': '1', 'awayteam_score': 54, 'hometeam_rating': 1367.138899616341, 'hometeam_id': '12', 'match_date': '2017-02-24 00:00:00+00:00', 'match_id': '20170224newportgwentdragonsleinsterrugby', 'hometeam_score': 22, 'awayteam_rating': 1689.861100383659},
{'awayteam_id': '11', 'awayteam_score': 18, 'hometeam_rating': 1345.113301127813, 'hometeam_id': '1', 'match_date': '2017-02-24 00:00:00+00:00', 'match_id': '20170224edinburghrugbycardiffblues', 'hometeam_score': 17, 'awayteam_rating': 1456.886698872187},
{'awayteam_id': '12', 'awayteam_score': 9, 'hometeam_rating': 1544.1975720594885, 'hometeam_id': '11', 'match_date': '2017-02-18 00:00:00+00:00', 'match_id': '20170218connachtrugbynewportgwentdragons', 'hometeam_score': 14, 'awayteam_rating': 1381.8024279405115},
{'awayteam_id': '11', 'awayteam_score': 30, 'hometeam_rating': 1613.4551541928877, 'hometeam_id': '1', 'match_date': '2017-02-24 00:00:00+00:00', 'match_id': '20170224munsterrugbyllanelliscarlets', 'hometeam_score': 21, 'awayteam_rating': 1666.5448458071123},
{'awayteam_id': '1', 'awayteam_score': 25, 'hometeam_rating': 1546.7342343946118, 'hometeam_id': '11', 'match_date': '2017-02-18 00:00:00+00:00', 'match_id': '20170218ospreysmunsterrugby', 'hometeam_score': 23, 'awayteam_rating': 1641.2657656053882},
{'awayteam_id': '1', 'awayteam_score': 7, 'hometeam_rating': 1639.4725651634064, 'hometeam_id': '12', 'match_date': '2017-02-17 00:00:00+00:00', 'match_id': '20170217llanelliscarletszebre', 'hometeam_score': 42, 'awayteam_rating': 1359.5274348365936},
{'awayteam_id': '1', 'awayteam_score': 10, 'hometeam_rating': 1675.3695149570462, 'hometeam_id': '11', 'match_date': '2017-02-17 00:00:00+00:00', 'match_id': '20170217leinsterrugbyedinburghrugby', 'hometeam_score': 39, 'awayteam_rating': 1361.6304850429538},
{'awayteam_id': '12', 'awayteam_score': 40, 'hometeam_rating': 1368.472294570552, 'hometeam_id': '11', 'match_date': '2017-02-12 00:00:00+00:00', 'match_id': '20170212benettontrevisoleinsterrugby', 'hometeam_score': 14, 'awayteam_rating': 1669.527705429448}
]

for dict in matches:
    streak(dict)