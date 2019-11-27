#team_name_dictionary
team_dict = {
    "Leinster Rugby": 1,
    "Leinster": 1,
    "leinster": 1,
    "Ulster Rugby": 2,
    "Ulster": 2,
    "ulster": 2,
    "Connacht Rugby": 3,
    "Connacht": 3,
    "connacht": 3,
    "Aironi Rugby": 13,
    "Newport Gwent Dragons": 12,
    "Dragons": 12,
    "Cardiff Blues": 11,
    "Ospreys": 9,
    "osperys": 9,
    "Zebre": 5,
    "zebre": 5,
    "Benetton Treviso": 6,
    "Treviso": 6,
    "treviso": 6,
    "Glasgow Warriors": 8,
    "Glasgow": 8,
    "glasgow": 8,
    "Edinburgh Rugby": 7,
    "Edinburgh": 7,
    "edinburgh": 7,
    "Munster Rugby": 4,
    "Munster": 4,
    "munster": 4,
    "Llanelli Scarlets": 10,
    "Scarlets": 10,
    "Llanelli": 10,

    # ENGLAND
    "Sale Sharks": 14,
    "Exeter Chiefs": 15,
    "Saracens": 16,
    "Bath Rugby": 17,
    "Bath": 17,
    "Northampton Saints": 18,
    "Northampton": 18,
    "Harlequin": 19,
    "Harlequins": 19,
    "Gloucester": 20,
    "London Irish": 21,
    "Worcester Warriors": 22,
    "Worcester": 22,
    "Wasps RFC": 23,
    "Wasps": 23,
    "London Welsh": 24,
    "Leicester Tigers": 25,
    "Leicester": 25,
    "Newcastle Falcons": 26,
    "Newcastle": 26,
    "Bristol": 27,

    # FRANCE top14
    "Montpellier": 28,
    "Mont-de-Marsan": 29,
    "Clermont Auvergne": 30,
    "Clermont": 30,
    "Grenoble": 31,
    "Stade Francais Paris": 32,
    "Stade Francais": 32,
    "Biarritz Olympique": 33,
    "Biarritz": 33,
    "Perpignan": 34,
    "Bayonne": 35,
    "Aviron Bayonnais": 35,
    "Toulon": 36,
    "Bordeaux-Begles": 37,
    "Bordeaux": 37,
    "Bordeaux Begles": 37,
    "Toulouse": 38,
    "Racing-Metro 92": 39,
    "SU Agen": 40,
    "Agen": 40,
    "Castres": 41,
    "Castres Olympique": 41,
    "Lyon Rugby": 42,
    "Lyon": 42,
    "La Rochelle": 43,
    "Brive": 44,
    "Oyonnax": 45,
    "Bourgoin-Jallieu": 46,
    "Section Paloise": 47,

    # france prod2
    "Narbonne": 48,
    "Carcassonnaise": 49,
    "Colomiers": 50,
    "Angouleme": 51,
    "Aurillac": 52,
    "Montauban": 53,
    "MN Montauban": 53,
    "Tarbes Pyrenees": 54,
    "Albi": 55,
    "Pays D Aix": 56,
    "US Dax": 57,
    "Dax": 57,
    "Massy": 58,
    "Auch": 59,
    "Beziers": 60,
    "Vannes": 61,
    "Bourg-en-Bresse": 62,
    "Perigueux": 63,
    "USON Nevers" : 100,
    "Rouen Normandie" : 101,
    "Valence Romans" : 102,

    # Italy League
    """
    "Rovigo": 64,  # added
    "Mogliano": 65,  # added
    "Fiamme Oro Roma": 66,  # added
    "Petrarca Padova": 67,  # added
    "Cammi Calvisano": 68,  # added
    "Lazio": 69,  # added
    "Cavalieri Prato": 70,  # added
    "San Dona": 71,  # added
    "L'Aquila Rugby": 72,  # added
    "Arix Viadana": 73,  # added
    "Reggio": 74,  # added
    "Capitolina": 75,  # added
    "Crociati": 76,  # added
    "Sitav Lyons Piacenza": 77,  # added
    "Mantovani": 78,  # NOT ADDED


    # OTHER CHALLANGE CUP TEAMS
    "Enisei-STM": 78,  # RUSSIA
    "Bucuresti": 79,  # ROMANIA
    "Timisoara Saracens": 81,  # ROMANIA
    "Olympus Rugby": 82,  # SPAIN
    "Bucharest Wolves": 80,  # ROMANIA
    """

    #SUPER RUGBY TEAMS 2011 - 2017++ BRUMBIES HAVE TO BE ADDED TWICE FOR SOME REASONE!
    "Brumbies" : 83,
    "Brumbies" : 83,
    "Bulls" : 84,
    "Cheetahs" : 85,
    "Chiefs" : 86,
    "Crusaders" : 87,
    "Highlanders" : 88,
    "Hurricanes" : 89,
    "Jaguares" : 90,
    "Lions" : 91,
    "Melbourne Rebels" : 92,
    "Melbourne" : 92,
    "Rebels" : 92,
    "Queensland Reds" : 93,
    "Reds" : 93,
    "Sharks" : 94,
    "Southern Kings" : 95,
    "Stormers" : 96,
    "Sunwolves" : 97,
    "Waratahs" : 98,
    "Western Force" : 99,
    "Force": 99,
    "Blues" : 82,

}

tournament_dict = {
    "pro12": 1,
    "pro14": 1,
    "avivapremiership": 2,
    "top14d1" : 3,
    "prod2" : 4,
    "championscup" : 5,
    "challangecup" : 6,
    "eccellenza" : 7,
    "anglowelsh" : 8,
    "superrugby" : 9,
}


def check_hometeam_name(post):
    if post['hometeam'] in team_dict:
        id = team_dict[post['hometeam']]
        return id
    else:
        return False

def check_awayteam_name(post):

    if post['awayteam'] in team_dict:
        id = team_dict[post['awayteam']]
        return id
    else:
        return False

def check_tournament_id(post):

    if post['tournament'] in tournament_dict:
        id = tournament_dict[post['tournament']]
        return id
    else:
        return False
