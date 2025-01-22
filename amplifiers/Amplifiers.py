class MatchData:
    def __init__(self, amplifier_users, amplifier_id, team1, team2):
        self.amplifier_users = amplifier_users
        self.amplifier_id = amplifier_id
        self.team1 = team1
        self.team2 = team2
        self.teams = [team1, team2]

    def get_current_score(self):
        return sum(self.team1.get_players().get_score()), sum(self.team2.get_players().get_score())


class PlayerScore:
    def __init__(self, player_id: int, score: int, combo: int, acc: float, misses: int, mods: str):
        self.player_id = player_id
        self.score = score
        self.combo = combo
        self.acc = acc
        self.misses = misses
        self.mods = mods

    def get_id(self) -> int:
        return self.player_id

    def get_score(self) -> int:
        return self.score

    def get_combo(self) -> int:
        return self.combo

    def get_acc(self) -> float:
        return self.acc

    def get_misses(self) -> int:
        return self.misses

    def get_mods(self) -> str:
        return self.mods

    def set_score(self, score: int):
        self.score = score

    def set_combo(self, combo: int):
        self.combo = combo

    def set_acc(self, acc: float):
        self.acc = acc

    def set_misses(self, misses: int):
        self.misses = misses

    def set_mods (self, mods: str):
        self.mods = mods


class Team:
    def __init__(self, players: [PlayerScore]):
        self.players = players

    def get_player_scores(self) -> [PlayerScore]:
        return self.players

    def get_player(self, player_id: int) -> PlayerScore:
        for player in self.players:
            if player.get_id() == player_id:
                return player
        raise ValueError(f"Player {player_id} not in team.")

    def get_score(self) -> [int]:
        return sum([player.get_score() for player in self.players])


class Amplifier:
    def __init__(self, amplifier_id: int):
        self.amplifier_id = amplifier_id

    def get_modified_score(self, data: MatchData) -> (int, int):
        """
        :return: Current score of the match based on Amplifier effect
        """
        pass

    def get_id(self) -> int:
        return self.amplifier_id

# Round up on a half
def round_up_on_half(value):
    return int(value + 0.5)

# Get the highest score for all amplifier teams, and multiply that score with the multiplier.
def get_highest_score(match: MatchData, multiplier):
    highest_score = max(score.get_score() for score in match.amplifier_users.get_player_scores())
    for score in match.amplifier_users.get_player_scores():
        if score.get_score() == highest_score:
            score.set_score(round_up_on_half(score.get_score() * multiplier))

# The Carry I
class TheCarryI(Amplifier):
    def __init__(self):
        super().__init__(1)

    def get_modified_score(self, match: MatchData) -> (int, int):
        get_highest_score(match, 1.2)
        return match.team1.get_score(), match.team2.get_score()


# The Carry II
class TheCarryII(Amplifier):
    def __init__(self):
        super().__init__(2)

    def get_modified_score(self, match: MatchData) -> (int, int):
        get_highest_score(match, 1.3)
        return match.team1.get_score(), match.team2.get_score()


# The Carry III
class TheCarryIII(Amplifier):
    def __init__(self):
        super().__init__(3)

    def get_modified_score(self, match: MatchData) -> (int, int):
        get_highest_score(match, 1.5)
        return match.team1.get_score(), match.team2.get_score()

# Poison I
class PoisonI(Amplifier):
    def __init__(self):
        super().__init__(4)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return match.team1.get_score(), match.team2.get_score() * 2
        else:
            return match.team1.get_score() * 2, match.team2.get_score()

# Poison II
class PoisonII(Amplifier):
    def __init__(self):
        super().__init__(5)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() * 1.75)
        else:
            return round_up_on_half(match.team1.get_score() * 1.75), match.team2.get_score()

# Poison III
class PoisonIII(Amplifier):
    def __init__(self):
        super().__init__(6)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() * 1.75)
        else:
            return round_up_on_half(match.team1.get_score() * 1.75), match.team2.get_score()


# Limit Break
class LimitBreak(Amplifier):
    def __init__(self):
        super().__init__(7)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(score.get_combo()) for score in match.team1.get_player_scores()]
        [score.set_score(score.get_combo()) for score in match.team2.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


# The King I
class TheKingI(Amplifier):
    def __init__(self):
        super().__init__(8)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() * 1.75), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() * 1.75)


# The King II
class TheKingII(Amplifier):
    def __init__(self):
        super().__init__(9)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() * 2), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() * 2)


# Dude That Fingerlock
class DudeThatFingerlock(Amplifier):
    def __init__(self):
        super().__init__(10)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * min(1.2, 1 + (score.get_misses() / 200)))) for score in
         match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()

# Cold Clear Eyes I
class ColdClearEyesI(Amplifier):
    def __init__(self):
        super().__init__(11)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() * 1.05), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() * 1.05)


# Cold Clear Eyes II
class ColdClearEyesII(Amplifier):
    def __init__(self):
        super().__init__(13)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() * 1.15), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() * 1.15)


# Cold Clear Eyes III
class ColdClearEyesIII(Amplifier):
    def __init__(self):
        super().__init__(13)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() * 1.2), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() * 1.2)


# Turn It Up
class TurnItUp(Amplifier):
    def __init__(self):
        super().__init__(14)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * 1.75)) for score in match.team1.get_player_scores() if
         "EZ" in score.get_mods()]
        [score.set_score(round_up_on_half(score.get_score() * 1.75)) for score in match.team2.get_player_scores() if
         "EZ" in score.get_mods()]
        return match.team1.get_score(), match.team2.get_score()


# Gambler
class Gambler(Amplifier):
    def __init__(self):
        super().__init__(15)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * 1.25)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


# Make It Rock
class MakeItRock(Amplifier):
    def __init__(self):
        super().__init__(18)

    def get_modified_score(self, match: MatchData) -> (int, int):
        set_team = match.team2 if match.amplifier_users == match.team1 else match.team1
        [score.set_score(round_up_on_half(score.get_score() * 1.25)) for score in set_team.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()

# Yin and Yang Get Scores
def yin_and_yang_get_team_info(match: MatchData, team, multiplier):
    highest_score_player = max(team.get_player_scores(), key=lambda player_score: player_score.get_score(),
                               default=None)
    highest_score_index = team.get_player_scores().index(highest_score_player)
    acc = team.get_player_scores()[1 - highest_score_index].get_acc()
    multiplier = multiplier if team == match.amplifier_users else 1.0
    return round_up_on_half(highest_score_player.get_score() * acc / 100 * multiplier)

# Yin and Yang I
class YinAndYangI(Amplifier):
    def __init__(self):
        super().__init__(19)

    def get_modified_score(self, match: MatchData) -> (int, int):
        team1_score = yin_and_yang_get_team_info(match, match.team1, 1.05)
        team2_score = yin_and_yang_get_team_info(match, match.team2, 1.05)

        return team1_score, team2_score


# Yin and Yang II
class YinAndYangII(Amplifier):
    def __init__(self):
        super().__init__(20)

    def get_modified_score(self, match: MatchData) -> (int, int):
        team1_score = yin_and_yang_get_team_info(match, match.team1, 1.1)
        team2_score = yin_and_yang_get_team_info(match, match.team2, 1.1)

        return team1_score, team2_score


# Yin and Yang III
class YinAndYangIII(Amplifier):
    def __init__(self):
        super().__init__(21)

    def get_modified_score(self, match: MatchData) -> (int, int):
        team1_score = yin_and_yang_get_team_info(match, match.team1, 1.15)
        team2_score = yin_and_yang_get_team_info(match, match.team2, 1.15)

        return team1_score, team2_score


# Classic Farmer
class ClassicFarmer(Amplifier):
    def __init__(self):
        super().__init__(23)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * 1.05)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()

# AccDance
class AccDance(Amplifier):
    def __init__(self):
        super().__init__(24)

    def get_modified_score(self, match: MatchData) -> (float, float):
        team1_score = round((match.team1.get_player_scores()[0].get_acc() + match.team1.get_player_scores()[1].get_acc()) / 2, 2)
        team2_score = round((match.team2.get_player_scores()[0].get_acc() + match.team2.get_player_scores()[1].get_acc()) / 2, 2)
        return team1_score, team2_score


# Synchronised I
class SynchronisedI(Amplifier):
    def __init__(self):
        super().__init__(25)

    def get_modified_score(self, match: MatchData) -> (int, int):
        base_multiplier = 1.1
        acc_difference = abs(match.amplifier_users.get_player_scores()[0].get_acc() -
                             match.amplifier_users.get_player_scores()[1].get_acc())
        if acc_difference >= 2:
            base_multiplier = 1.0
        else:
            base_multiplier -= 0.0025 * acc_difference
        [score.set_score(round_up_on_half(score.get_score() * base_multiplier)) for score in
         match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


# Synchronised II
class SynchronisedII(Amplifier):
    def __init__(self):
        super().__init__(26)

    def get_modified_score(self, match: MatchData) -> (int, int):
        base_multiplier = 1.2
        acc_difference = abs(match.amplifier_users.get_player_scores()[0].get_acc() -
                             match.amplifier_users.get_player_scores()[1].get_acc())
        if acc_difference >= 4:
            base_multiplier = 1.0
        else:
            base_multiplier -= 0.0025 * acc_difference
        [score.set_score(round_up_on_half(score.get_score() * base_multiplier)) for score in
         match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


# Go With The Flow
class GoWithTheFlow(Amplifier):
    def __init__(self):
        super().__init__(27)

    def get_modified_score(self, match: MatchData) -> (int, int):
        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() * 1.15), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() * 1.15)


# Loadbearer I
class LoadbearerI(Amplifier):
    def __init__(self):
        super().__init__(31)

    def get_modified_score(self, match: MatchData) -> (int, int):
        score_difference = abs(match.amplifier_users.get_player_scores()[0].get_score() -
                               match.amplifier_users.get_player_scores()[1].get_score())
        score_added = max(score_difference * 0.25, 150000)

        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() + score_added), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() + score_added)


# Loadbearer II
class LoadbearerII(Amplifier):
    def __init__(self):
        super().__init__(32)

    def get_modified_score(self, match: MatchData) -> (int, int):
        score_difference = abs(match.amplifier_users.get_player_scores()[0].get_score() -
                               match.amplifier_users.get_player_scores()[1].get_score())
        score_added = max(score_difference * 0.5, 300000)

        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() + score_added), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() + score_added)


# Loadbearer III
class LoadbearerIII(Amplifier):
    def __init__(self):
        super().__init__(33)

    def get_modified_score(self, match: MatchData) -> (int, int):
        score_difference = abs(match.amplifier_users.get_player_scores()[0].get_score() -
                               match.amplifier_users.get_player_scores()[1].get_score())
        score_added = max(score_difference * 0.75, 400000)

        if match.amplifier_users == match.team1:
            return round_up_on_half(match.team1.get_score() + score_added), match.team2.get_score()
        else:
            return match.team1.get_score(), round_up_on_half(match.team2.get_score() + score_added)


# The Dragon Consumes I
class TheDragonConsumesI(Amplifier):
    def __init__(self):
        super().__init__(33)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * 1.1)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


# The Dragon Consumes II
class TheDragonConsumesII(Amplifier):
    def __init__(self):
        super().__init__(34)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * 1.2)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


# The Dragon Consumes III
class TheDragonConsumesIII(Amplifier):
    def __init__(self):
        super().__init__(35)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * 1.3)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


# JTBFREAKS
class JTBFREAKS(Amplifier):
    def __init__(self):
        super().__init__(37)

    def get_modified_score(self, match: MatchData) -> (int, int):
        team1_score = match.team1.get_player_scores()[0].get_combo() + match.team1.get_player_scores()[1].get_combo()
        team2_score = match.team2.get_player_scores()[0].get_combo() + match.team2.get_player_scores()[1].get_combo()
        return team1_score + team2_score


# Desperation I
class DesperationI(Amplifier):
    def __init__(self):
        super().__init__(38)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * 0.7)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()


# Desperation II
class DesperationII(Amplifier):
    def __init__(self):
        super().__init__(38)

    def get_modified_score(self, match: MatchData) -> (int, int):
        [score.set_score(round_up_on_half(score.get_score() * 0.85)) for score in match.amplifier_users.get_player_scores()]
        return match.team1.get_score(), match.team2.get_score()