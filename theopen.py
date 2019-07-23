import requests
import json

leaf_league = {
    "embrey": "Koepka,Schauffele,Fleetwood,Stenson,Oosthuizen,McDowell",
    "strangeway": "McIlroy,Molinari,Kuchar,Day,Matsuyama,Mickelson",
    "moore": "Rahm,Fowler,Thomas,Wallace,Cabrera_Bello,Pepperell",
    "kruse": "Johnson Dustin,DeChambeau,Cantlay,Scott,Finau,Leishman",
    "moberly": "Rose,Woods,Woodland,Casey,Simpson,Watson",
    "alexander": "Reed,Reavie,Kisner,Fitzpatrick,Bradley,Lowry",
}


def get_data():
    return [{"name": k, "golfers": v} for k, v in get_leaf_players().items()]

#version1 - Life, Universe, and Everything
def calculate_score(player, golf_round):
    return 42

# version 2
# def calculate_score(player, golf_round):
#     player_data = get_data()
#     total_score = 0
#     golfers = []
#     for p in player_data:
#         if p['name'] == player.lower():
#             golfers = p['golfers']
#             break
#     for g in golfers:
#         total_score += g[golf_round]
#     return total_score


#version3
# def calculate_score(player, golf_round):
#     player_data = get_data()
#     golfers = [p['golfers'] for p in player_data if p['name'] == player.lower()][0]
#     print([g[golf_round] for g in golfers])
#     return sum(sorted([g[golf_round] for g in golfers])[:4])

#version4 - show coverage tool next
# def calculate_score(player, golf_round):
#     player_data = get_data()
#     golfers = [p['golfers'] for p in player_data if p['name'] == player.lower()][0]
#     round_scores = [g[golf_round] for g in golfers if g[golf_round] is not None]
#     # print(f"Scores: {round_scores}")
#     # sorted_scores = sorted(round_scores)
#     # return sum(round_scores)
#     return sum(sorted(round_scores)[:4])


def fetch_golfers():
    url = "https://www.theopen.com/api/sitecore/PlayerInformation/GetPlayersInfo"
    return requests.get(url).json()["players"]

def fetch_scores():
    url = "https://scores.load.theopen.com/api/ScoringFrontEndGet?code=kwJKhs3cRZhB/u6H4ABYNONphQPayNLJ6wDaqd3TxV1voIwTagtADQ==&feedType=traditional&env=live"
    return requests.get(url).json()

def get_leaf_players():
    open_players = fetch_golfers()
    scores = fetch_scores()

    leafer_player_ids = {}
    for leafer, players in leaf_league.items():
        names = players.split(",")
        if leafer not in leafer_player_ids.keys():
            leafer_player_ids[leafer] = []
        for n in names:
            name_list = n.split()
            last_name, first_name = name_list[0].strip().lower(), None
            if len(name_list) == 2:
                first_name = name_list[1].strip().lower()
            last_name = last_name.replace("_", " ")
            found = False
            for p in open_players:
                if last_name == p["lastName"].lower() and first_name is None:
                    found = True
                elif (
                    last_name == p["lastName"].lower()
                    and first_name == p["firstName"].lower()
                ):
                    found = True
                if found:
                    populate_round_scores(p, scores)
                    leafer_player_ids[leafer].append(p)
                    break
            # else:
            #     print("Cound not find: {0} - {1}".format(last_name, first_name))

    return leafer_player_ids


def populate_round_scores(golfer, scores):
    for p in scores["players"]:
        if p["id"] == golfer["playerId"]:
            for golf_round in ["r1", "r2", "r3", "r4"]:
                golfer[golf_round] = p[golf_round]


def main():
    url = "https://www.theopen.com/api/sitecore/PlayerInformation/GetPlayersInfo"
    with open("players.json", "w") as f:
        json.dump(requests.get(url).json(), f)

    with open("scores.json", "w") as f:
        url = "https://scores.load.theopen.com/api/ScoringFrontEndGet?code=kwJKhs3cRZhB/u6H4ABYNONphQPayNLJ6wDaqd3TxV1voIwTagtADQ==&feedType=traditional&env=live"
        json.dump(requests.get(url).json(), f)


if __name__ == "__main__":
    main()
