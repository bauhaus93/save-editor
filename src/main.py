import logging

from savegame import SaveGame
from util import setup_logger

FILE_IN = "nameless-firered-project-a1.02 - Kopie.sav"
FILE_OUT = "nameless-firered-project-a1.02.sav"
#FILE_IN = "Pokemon Blattgruen (D) - Kopie.sav"
#FILE_OUT = "Pokemon Blattgruen (D).sav"

if __name__ == "__main__":
    setup_logger()
    logger = logging.getLogger()

    logger.info("Opening savegame: '{}'".format(FILE_IN))
    with open(FILE_IN, "rb") as f:
        data = f.read()

    savegame = SaveGame(data)
    save = savegame.get_active_save()
    #team = save.read_team()
    #team.max_ivs()
    #save.write_team(team)
    save.set_public_trainer_id(10001)

    output = savegame.into_bytes()

    logger.info("Writing savegame: '{}'".format(FILE_OUT))
    with open(FILE_OUT, "wb") as f:
        f.write(output)
