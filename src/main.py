from savegame import SaveGame

#FILE_IN = "nameless-firered-project-a1.02 - Kopie.sav"
#FILE_OUT = "nameless-firered-project-a1.02.sav"
FILE_IN = "Pokemon Blattgruen (D) - Kopie.sav"
FILE_OUT = "Pokemon Blattgruen (D).sav"

if __name__ == "__main__":
    with open(FILE_IN, "rb") as f:
        data = f.read()

    savegame = SaveGame(data)
    for save in savegame.get_saves():
        team = save.get_team()
        print(team)
        team.into_bytes()
        #save.set_public_trainer_id(10001)

    output = savegame.into_bytes()

    with open(FILE_OUT, "wb") as f:
        f.write(output)
