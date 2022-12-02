import os

hand = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}
wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
values = {"rock": 1, "paper": 2, "scissors": 3}
scores = {"win": 6, "tie": 3, "lose": 0}
#  part 2
needed_outcome = {"X": "lose", "Y": "tie", "Z": "win"}


def get_input(fn):
    with open(fn, "r") as f:
        return f.read().strip()


def get_score(played, outcome):
    score = scores[outcome] + values[played]
    return score


def get_outcome(player1, player2):
    """returns the outcome of the round for each player"""
    if player1 == player2:
        return "tie", "tie"
    elif player2 == wins[player1]:
        return "win", "lose"
    else:
        return "lose", "win"


def play_round(round: str):
    """returns the score for player 1 and the score for player 2"""
    p1, p2 = round.split(" ")
    p1 = hand[p1]
    p2 = hand[p2]
    outcome_p1, outcome_p2 = get_outcome(p1, p2)
    score_p1 = get_score(p1, outcome_p1)
    score_p2 = get_score(p2, outcome_p2)
    return (score_p1, score_p2)


def play_game_1():
    scores_p1, scores_p2 = [], []
    for item in rounds:
        result = play_round(item)
        scores_p1.append(result[0])
        scores_p2.append(result[1])
    print(sum(scores_p1), sum(scores_p2))


def play_round_2(round: str):
    """returns the score for player 1 and the score for player 2"""
    p1, o2 = round.split(" ")
    p1 = hand[p1]
    # o2 is the outcome needed as XYZ:
    o2 = needed_outcome[o2]
    # o2 is the outcome needed as 'win|tie|lose':
    if o2 == "tie":
        p2 = p1[:]
    elif o2 == "win":
        p2 = wins[wins[p1]]
    else:
        p2 = wins[p1]

    outcome_p1, outcome_p2 = get_outcome(p1, p2)
    score_p1 = get_score(p1, outcome_p1)
    score_p2 = get_score(p2, outcome_p2)
    # print(p1, p2, o2, score_p1, score_p2)

    return (score_p1, score_p2)


def play_game_2():
    scores_p1, scores_p2 = [], []
    for item in rounds:
        result = play_round_2(item)
        scores_p1.append(result[0])
        scores_p2.append(result[1])
    print(sum(scores_p1), sum(scores_p2))


if __name__ == "__main__":
    input = get_input(os.path.join("./inputs", "2022__2.txt"))
    rounds = input.split("\n")
    play_game_1()
    play_game_2()
