from gamescript import *


def run_dota(mode):
    tier_accepted = ["Tier_1"] # List of all accepted tournament tier
    excluded_tournaments = []
    run_game_script(mode, tier_accepted, excluded_tournaments, "dota2", "dota2")