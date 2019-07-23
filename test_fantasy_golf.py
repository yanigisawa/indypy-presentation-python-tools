import pytest
import mock
import json
from theopen import calculate_score

leaf_league = {
    "embrey": "Koepka,Schauffele,Fleetwood,Stenson,Oosthuizen,McDowell",
    "strangeway": "McIlroy,Molinari,Kuchar,Day,Matsuyama,Mickelson",
    "moore": "Rahm,Fowler,Thomas,Wallace,Cabrera_Bello,Pepperell",
    "kruse": "Johnson Dustin,DeChambeau,Cantlay,Scott,Finau,Leishman",
    "moberly": "Rose,Woods,Woodland,Casey,Simpson,Watson",
    "alexander": "Reed,Reavie,Kisner,Fitzpatrick,Bradley,Lowry",
}

def mock_fetch_golfers():
    with open('players.json', 'r') as f:
        return json.load(f)['players']

def mock_fetch_scores():
    with open('scores.json', 'r') as f:
        return json.load(f)

expected_scores = [

    #v1 - Life, Universe and Everything
    ('Embrey', 'r1', 42),

    #v2 - Sum All Scores
    # ('Embrey', 'r1', 423)

    #v3 - List Comprehensions - Top 4 Only
    # ('Embrey', 'r1', 276), ('Embrey', 'r2', 270), ('Embrey', 'r3', 269), ('Embrey', 'r4', 293),

    #v4 - Edge Case
    # ('Alexander', 'r1', 279), ('Alexander', 'r2', 274),
    # ('Alexander', 'r3', 274), ('Alexander', 'r4', 289)
]

@mock.patch('theopen.fetch_golfers')
@mock.patch('theopen.fetch_scores')
@pytest.mark.parametrize("player,golf_round,score", expected_scores)
def test_round_score(scores, golfers, player, golf_round, score):
    scores.side_effect = mock_fetch_scores
    golfers.side_effect = mock_fetch_golfers
    assert score == calculate_score(player, golf_round)
