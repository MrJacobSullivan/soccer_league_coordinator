import csv


def catalog_players():
    """Catalog the players using the included .csv file."""
    list_of_players = []

    with open('soccer_players.csv', newline='') as soccer_players_csv:
        csv_reader = csv.DictReader(soccer_players_csv, delimiter=',')
        rows = list(csv_reader)

        player_name = None
        player_height = None
        player_experience = None
        player_guardians = None

        for player in rows[0:]:
            player_name = player['Name']
            player_height = int(player['Height (inches)'])
            player_guardians = player['Guardian Name(s)']

            if player['Soccer Experience'] == 'YES':
                player_experience = True
            else:
                player_experience = False

            list_of_players.append({'name': player_name,
                                    'height': player_height,
                                    'experience': player_experience,
                                    'guardians': player_guardians})

        return list_of_players


def sort_by_experience(league):
    """Sort the players based on their experience."""
    experienced = []
    inexperienced = []

    for player in league:
        if player['experience']:
            experienced.append(player)
        else:
            inexperienced.append(player)

    return experienced, inexperienced


def sort_by_height(exp_players, inexp_players):
    """Sort the players by height."""
    sorted_players = []

    key = lambda custom: custom['height']
    exp_players = sorted(exp_players, key=key, reverse=True)
    inexp_players = sorted(inexp_players, key=key, reverse=True)

    for i in range(0, len(exp_players) + len(inexp_players)):
        if i % 2 == 0:
            sorted_players.append(exp_players.pop())
        else:
            sorted_players.append(inexp_players.pop())

    return sorted_players


def make_teams(players):
    """Create the teams based on height and experience."""
    dragons = []
    sharks = []
    raptors = []

    for player in players[::3]:
        player['team'] = 'Sharks'
        dragons.append(player)

    del players[::3]

    for player in players[::2]:
        player['team'] = 'Dragons'
        sharks.append(player)

    del players[::2]

    for player in players:
        player['team'] = 'Raptors'
        raptors.append(player)

    league = dragons + sharks + raptors

    return league


def write_letter(player):
    """Write letters to the guardians."""
    if player['team'] == 'Dragons':
        practice = 'March 17, 1pm'
    elif player['team'] == 'Sharks':
        practice = 'March 17, 3pm'
    elif player['team'] == 'Raptors':
        practice = 'March 18, 1pm'

    letter = (
        "Dear {0[guardians]},\n"
        "Your child {0[name]} has been assigned to the soccer team {0[team]}!\n"
        "Your child's first practice will be {time}.\n"
        "We are excited to see you there.\n"
    ).format(player, time=practice)

    return letter


if __name__ == '__main__':
    # catalog the players from the included .csv file
    players = catalog_players()

    # sort the players based on experience
    exp_players, inexp_players = sort_by_experience(players)

    # converge the players based on height
    sorted_players = sort_by_height(exp_players, inexp_players)

    # divides the players into teams
    league = make_teams(sorted_players)

    # write a letter to each parent
    for player in league:
        letter = write_letter(player)
        filename = '{}.text'.format(player['name'].replace(' ', '_').lower())
        with open(filename, 'w') as f:
            f.write(letter)
