from gamescript import *


def run_lol(mode):
    tier_accepted = ["S-Tier"] # List of all accepted tournament tier
    excluded_tournaments = ["All-Star/2013", "All-Star/2014", "All-Star/2015", "All-Star/2016", "All-Star/2017", "All-Star/2018",
                            "All-Star/2020", "Mid-Season Invitational/2020", "Rift Rivals/LCK-LPL-LMS-VCS/2019", "Rift Rivals/NA-EU/2019",
                            "Rift Rivals/LCK-LPL-LMS/2018", "Rift Rivals/LLN-CLS-CBLOL/2018", "Rift Rivals/NA-EU/2018", "Rift Rivals/LCL-TCL-VCS/2018",
                            "Rift Rivals/SEA-LJL-OPL/2018", "Rift Rivals/LCL-TCL/2017", "Rift Rivals/LCK-LPL-LMS/2017", "Rift Rivals/NA-EU/2017",
                            "Rift Rivals/LLN-CLS-CBLOL/2017", "Rift Rivals/GPL-LJL-OPL/2017"]
    run_game_script(mode, tier_accepted, excluded_tournaments, "leagueoflegends", "lol")