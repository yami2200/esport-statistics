from gamescript import *


def run_cs(mode):
    tier_accepted = ["S-Tier"] # List of all accepted tournament tier
    excluded_tournaments = []
    run_game_script(mode, tier_accepted, excluded_tournaments, "counterstrike", "cs")