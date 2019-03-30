import logging

from pokemon import Pokemon

logger = logging.getLogger()

class Team:

    def __init__(self, team_data, team_size):
        self.pkmn_list = list()
        self.trail = team_data[team_size * 100:]
        for offset in range(0, team_size * 100, 100):
            pkmn = Pokemon(team_data[offset:offset + 100])
            self.pkmn_list.append(pkmn)

    def get_size(self):
        return len(self.pkmn_list)

    def max_ivs(self):
        for pkmn in self.pkmn_list:
            pkmn.max_ivs()

    def __str__(self):
        return "\n".join(str(pkmn) for pkmn in self.pkmn_list)

    def into_bytes(self):
        output = bytes()
        for pkmn in self.pkmn_list:
            output += pkmn.into_bytes()
        output += self.trail
        if len(output) != 600:
            logger.error("Team.into_bytes(): Unexpected result size: expected = {}, was = {}".format(6 * 100, len(output)))
            exit(1)
        return output
