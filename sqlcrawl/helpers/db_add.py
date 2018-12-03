import psycopg2
import datetime
import urllib.parse


#LOCAL
"""
HOST = 'localhost'
DBNAME = 'rugbyrankreduced'
USER = 'briandelaney'
PASSWORD = 'quqaiwii1!'
PORT = '5432'
"""
#HEROKU CLOUD
HOST = 'ec2-107-22-251-55.compute-1.amazonaws.com'
DBNAME = 'd3orpk49e09mue'
USER = 'mqzqulyozmcfft'
PASSWORD = '56739d733534a0f11f903a82cc51aaed547da4707ac4b600927f39f4c64d5218'
PORT = '5432'

print(HOST)
#"postgres://iyaiiyrpuplanq:b326b8d95e8512f6bba9153d83b400435805bc609dc5305c4feaa4d632ab5460@ec2-23-23-237-68.compute-1.amazonaws.com:5432/dfl7jms7uer30d"

def connect():
    try:
        #DEVELOPMENT CONNECTION
        conn_string = "host= " + HOST + " dbname= " + DBNAME + " user= " + USER + " password= " + PASSWORD
        conn = psycopg2.connect(
            database=DBNAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        return conn
    except:
        print("Error: Unable to connect to the database")
        return False


def add_match(post):
    if post:
        if post["hometeam"] and post["hometeam_score"] and post['awayteam_id'] and post['hometeam_id'] and post["awayteam"] and post["tournament"] and post["awayteam_score"] and post["match_date"] and post["_id"] and post["added_on"] and post['tournament_id']:
            conn =  connect()
            if conn:
                  try:
                      cur = conn.cursor()
                  except:
                      print("Error: Could Not Create Database Cursor")
                  if cur:
                      try:
                          insert_str = "INSERT INTO elo_match (id, hometeam_score, awayteam_score, created_date, match_date, calculated, tournament_id, hometeam_id, awayteam_id, awayteam_rating_after, hometeam_rating_after, awayteam_rating_before, hometeam_rating_before) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 0, 0, 0, 0);" % (post["_id"], post["hometeam_score"],post["awayteam_score"], datetime.datetime.now().date(), (post["match_date"]).date(), 'false', (post["tournament_id"]), post['hometeam_id'], post['awayteam_id'])
                          print(insert_str)
                          cur.execute(insert_str)
                          try:
                              conn.commit()
                              cur.close()
                              conn.close()
                              print("Sucess: Match Added to Database")
                              return True
                          except Exception as e:
                              print("Error: Could not Commit Database Changes")
                              return False
                      except Exception as e:
                          print(e)
                          print("Error: Could Not Execute SQL Insert For Match")
                          return False
                  else:
                      print("Error: Could Not Get Database Cursor")
                      return False
            else:
                print("Error: Could Not Establish Database Connection")
                return False
        else:
            print("Error: Not All Elements Present")
            return False
    else:
        print("Error: No Data To Pass to Database For Match")