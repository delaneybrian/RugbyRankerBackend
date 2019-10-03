from sqlcrawl.main import start_all_crawlers
from Ranking.play_match import initate_analysis
from Ranking.calculatePositions import CalculatePositions

start_all_crawlers()
initate_analysis()
CalculatePositions()