from gamescript import *


def run_rl(mode):
    tier_accepted = ["S-Tier"] # List of all accepted tournament tier
    excluded_tournaments = ["Collegiate Rocket League/2023/World Championship", "Collegiate Rocket League/2022/World Championship"]
    run_game_script(mode, tier_accepted, excluded_tournaments, "rocketleague", "rl")