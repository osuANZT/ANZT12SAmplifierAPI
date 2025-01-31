import json
from flask import Flask, jsonify, request
from flask_cors import CORS
from amplifiers.Amplifiers import *

app = Flask(__name__)
CORS(app)

# Load player/team/amplifier data
with open("data.json", "r") as f:
    data = json.load(f)

# The number is the amplifier ID
amplifiers = {
    1: TheCarryI(),
    2: TheCarryII(),
    3: TheCarryIII(),
    4: PoisonI(),
    5: PoisonII(),
    6: PoisonIII(),
    7: LimitBreak(),
    8: TheKingI(),
    9: TheKingII(),
    10: DudeThatFingerlock(),
    11: ColdClearEyesI(),
    12: ColdClearEyesII(),
    13: ColdClearEyesIII(),
    14: TurnItUp(),
    15: Gambler(),
    18: MakeItRock(),
    19: YinAndYangI(),
    20: YinAndYangII(),
    21: YinAndYangIII(),
    24: AccDance(),
    25: SynchronisedI(),
    26: SynchronisedII(),
    27: GoWithTheFlow(),
    28: LoadbearerI(),
    29: LoadbearerII(),
    30: LoadbearerIII(),
    33: TheDragonConsumesI(),
    34: TheDragonConsumesII(),
    35: TheDragonConsumesIII(),
    37: JTBFREAKS(),
    38: DesperationI(),
    39: DesperationII(),
    41: Roulette()
}


@app.route('/score')
def score():
    # Retrieve query parameters (Flask didn't like the default values)
    team_name = request.args.get('team_name')
    amplifier_id = request.args.get('amplifier_id')
    player1_id = request.args.get('player1_id')
    player1_score = request.args.get('player1_score')
    player1_combo = request.args.get('player1_combo')
    player1_acc = request.args.get('player1_acc')
    player1_misses = request.args.get('player1_misses')
    player1_mods = request.args.get('player1_mods')

    player2_id = request.args.get('player2_id')
    player2_score = request.args.get('player2_score')
    player2_combo = request.args.get('player2_combo')
    player2_acc = request.args.get('player2_acc')
    player2_misses = request.args.get('player2_misses')
    player2_mods = request.args.get('player2_mods')

    player3_id = request.args.get('player3_id')
    player3_score = request.args.get('player3_score')
    player3_combo = request.args.get('player3_combo')
    player3_acc = request.args.get('player3_acc')
    player3_misses = request.args.get('player3_misses')
    player3_mods = request.args.get('player3_mods')

    player4_id = request.args.get('player4_id')
    player4_score = request.args.get('player4_score')
    player4_combo = request.args.get('player4_combo')
    player4_acc = request.args.get('player4_acc')
    player4_misses = request.args.get('player4_misses')
    player4_mods = request.args.get('player4_mods')

    # Convert params to right type
    player1_id, player2_id, player3_id, player4_id = int(player1_id), int(player2_id), int(player3_id), int(player4_id)
    player1_score, player2_score, player3_score, player4_score = int(player1_score), int(player2_score), int(player3_score), int(player4_score)
    player1_combo, player2_combo, player3_combo, player4_combo = int(player1_combo), int(player2_combo), int(player3_combo), int(player4_combo)
    player1_acc, player2_acc, player3_acc, player4_acc = float(player1_acc), float(player2_acc), float(player3_acc), float(player4_acc)
    player1_misses, player2_misses, player3_misses, player4_misses = int(player1_misses), int(player2_misses), int(player3_misses), int(player4_misses)
    amplifier_id = int(amplifier_id)

    # Data > objects (for sanity)
    p1 = PlayerScore(player1_id, player1_score, player1_combo, player1_acc, player1_misses, player1_mods)
    p2 = PlayerScore(player2_id, player2_score, player2_combo, player2_acc, player2_misses, player2_mods)
    team1 = Team([p1, p2])

    p3 = PlayerScore(player3_id, player3_score, player3_combo, player3_acc, player3_misses, player3_mods)
    p4 = PlayerScore(player4_id, player4_score, player4_combo, player4_acc, player4_misses, player4_mods)
    team2 = Team([p3, p4])

    # Determine which players belong to the given team
    team_players = data["teams"].get(team_name)
    if team_players is None:
        return jsonify({"error": "Team not found"}), 404

    if player1_id not in team_players and player2_id not in team_players and player3_id not in team_players and player4_id not in team_players:
        return jsonify({"error": "No players from the given team are found in the match data."}), 404

    # Determine if players are out of order from teams
    # Check if players are out of order and reorder them
    if (player1_id in team_players) != (player2_id in team_players):
        player_scores = [p1, p2, p3, p4]
        # Find the index of the player who should be swapped
        swap_index = 2 if player3_id in team_players else 3

        if player1_id not in team_players:
            player_scores[0], player_scores[swap_index] = player_scores[swap_index], player_scores[0]
        else:
            player_scores[1], player_scores[swap_index] = player_scores[swap_index], player_scores[1]

        # Create team objects with reordered players
        team1 = Team(player_scores[:2])
        team2 = Team(player_scores[2:])


    # Identify the team for the amplifier
    amplifier_users = team1 if player1_id in team_players or player2_id in team_players else team2
    match = MatchData(amplifier_users, amplifier_id, team1, team2)

    # Find the corresponding amplifier instance
    amplifier = amplifiers.get(amplifier_id)
    if amplifier is None:
        return jsonify({"error": "Invalid amplifier ID"}), 404

    modified_scores = amplifier.get_modified_score(match)

    return jsonify(
        {
            "team1_score":  modified_scores[0],
            "team2_score":  modified_scores[1],
            "team1_players:": [pid.get_id() for pid in team1.get_player_scores()],
            "team2_players:": [pid.get_id() for pid in team2.get_player_scores()]
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
