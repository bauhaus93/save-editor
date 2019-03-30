from struct import unpack, pack
    
from saveblock import SaveBlock
from size import SAVE_BLOCK_SIZE, HOF_OFFSET, HOF_SIZE, MG_ER_OFFSET, MG_ER_SIZE, REC_BAT_OFFSET, REC_BAT_SIZE

class SaveGame:
    def __init__(self, data):
        self.saves = [SaveBlock(data[:SAVE_BLOCK_SIZE]),
                       SaveBlock(data[SAVE_BLOCK_SIZE:])]
        self.hof = data[HOF_OFFSET:HOF_OFFSET + HOF_SIZE]
        self.mger = data[MG_ER_OFFSET:MG_ER_OFFSET + MG_ER_SIZE]
        self.rec_bat = data[REC_BAT_OFFSET:REC_BAT_OFFSET + REC_BAT_SIZE]
    def get_active_save(self):
        if self.saves[0].get_save_index() > self.saves[1].get_save_index():
            return self.saves[0]
        return self.saves[1]
    def get_saves(self):
        return self.saves
    def into_bytes(self):
        return self.saves[0].into_bytes() + self.saves[1].into_bytes() + self.hof + self.mger + self.rec_bat
    def __str__(self):
        return "Savegame:\n\n{}\n{}".format(self.saves[0], self.saves[1])