import logging
from struct import unpack, pack

from util import hexdump

# thoughts/knowledge on structure in nameless firered
# (regarding difference to structure of vanilla frlg)
# "data" field not encrypted
# checksum not used (always 0)
# ev block in data field always third block (data+24) 

# offsets relative to data field
EV_OFFSET = 24  
IV_OFFSET = 36 + 4

logger = logging.getLogger()

class Pokemon:

    def __init__(self, pkmn_data):
        self.personality = unpack("<L", pkmn_data[0:4])[0]
        self.ot_id = unpack("<L", pkmn_data[4:8])[0]
        self.nickname = unpack("<10s", pkmn_data[8:18])[0]
        self.language = unpack("<H", pkmn_data[18:20])[0]
        self.ot_name = unpack("<7s", pkmn_data[20:27])[0]
        self.markings = unpack("<B", pkmn_data[27:28])[0]
        self.checksum = unpack("<H", pkmn_data[28:30])[0]
        self.unknown = unpack("<H", pkmn_data[30:32])[0]
        self.data = unpack("<48s", pkmn_data[32:80])[0]
        self.status_condition = unpack("<L", pkmn_data[80:84])[0]
        self.level = unpack("<B", pkmn_data[84:85])[0]
        self.pokerus = unpack("<B", pkmn_data[85:86])[0]
        self.curr_hp, self.total_hp = unpack("<HH", pkmn_data[86:90])
        self.stats = unpack("<5H", pkmn_data[90:])
        
        self.load_evs()
        self.load_misc()
        self.write_misc()

    def max_ivs(self):
        logger.info("Maxing IVs for Pokemon: {} -> {}".format(sum(self.ivs), 31 * 6))
        for i in range(len(self.ivs)):
            self.ivs[i] = 31
        self.write_misc()
    
    def load_evs(self):
        self.evs = unpack("<6B", self.data[EV_OFFSET:EV_OFFSET + 6])

    def load_misc(self):
        value = unpack("<l", self.data[IV_OFFSET:IV_OFFSET + 4])[0]
        self.ivs = [value >> (5 * i) & 0x1F for i in range(6)]
        self.egg = (value >> 30) & 1
        self.ability = (value >> 31) & 1

    def write_evs(self):
        self.data = self.data[:EV_OFFSET] + pack("<6B", *self.evs) + self.data[EV_OFFSET + 6:]

    def write_misc(self):
        new_value = (self.egg << 30) | (self.ability << 31)
        for (i, iv) in enumerate(self.ivs):
            new_value |= (iv << (5 * i))
        self.data = self.data[:IV_OFFSET] + pack("<L", new_value) + self.data[IV_OFFSET + 4:]

    def __str__(self):
        output = "Pkmn:\n"
        output += "\tPersonality:\t{}\n".format(get_personality(self.personality))
        output += "\tLevel:\t\t{:3}\n".format(self.level)
        output += "\thp:\t\t{}/{}\n".format(self.curr_hp, self.total_hp)
        output += "\tStats:"
        output += "\tAtt:\t{:3}\n\t\tDef:\t{:3}\n\t\tSpd:\t{:3}\n\t\tSpAtt:\t{:3}\n\t\tSpDef:\t{:3}\n".format(*self.stats)
        output += "\tIVs:\tTotal:\t{:3}\n".format(sum(self.ivs))
        output += "\t\tHP:\t{:3}\n\t\tAtt:\t{:3}\n\t\tDef:\t{:3}\n\t\tSpd:\t{:3}\n\t\tSpAtt:\t{:3}\n\t\tSpDef:\t{:3}\n".format(*self.ivs)
        output += "\tEVs:\tTotal:\t{:3}\n".format(sum(self.evs))
        output += "\t\tHP:\t{:3}\n\t\tAtt:\t{:3}\n\t\tDef:\t{:3}\n\t\tSpd:\t{:3}\n\t\tSpAtt:\t{:3}\n\t\tSpDef:\t{:3}\n".format(*self.evs)
        output += "\tChecksum:\t0x{:04X}\n".format(self.checksum)
        return output

    def into_bytes(self):
        output = bytes()
        output += pack("<LL10sH7sBHH48sLBBHH5H",
            self.personality, self.ot_id, self.nickname, self.language, self.ot_name,
            self.markings, self.checksum, self.unknown, self.data, self.status_condition, self.level,
            self.pokerus, self.curr_hp, self.total_hp, *self.stats)
        if len(output) != 100:
            logger.error("Pokemon.into_bytes(): Unexpected result size: expected = {}, was = {}".format(100, len(output)))
            exit(1)
        return output


def crypt_data(data, ot_id, personality):
    data_decr = bytes()
    key = ot_id ^ personality
    for i in range(0, len(data), 4):
        decr_val = unpack("<L", data[i:i + 4])[0] ^ key
        data_decr += pack("<L", decr_val)
    return data_decr

def get_substructure_index(personality, sub_char):
    val = personality % 24
    if val == 0: return "GAEM".find(sub_char)
    if val == 1: return "GAME".find(sub_char)
    if val == 2: return "GEAM".find(sub_char)
    if val == 3: return "GEMA".find(sub_char)
    if val == 4: return "GMAE".find(sub_char)
    if val == 5: return "GMEA".find(sub_char)

    if val == 6: return "AGEM".find(sub_char)
    if val == 7: return "AGME".find(sub_char)
    if val == 8: return "AEGM".find(sub_char)
    if val == 9: return "AEMG".find(sub_char)
    if val == 10: return "AMGE".find(sub_char)
    if val == 11: return "AMEG".find(sub_char)

    if val == 12: return "EGAM".find(sub_char)
    if val == 13: return "EGMA".find(sub_char)
    if val == 14: return "EAGM".find(sub_char)
    if val == 15: return "EAMG".find(sub_char)
    if val == 16: return "EMGA".find(sub_char)
    if val == 17: return "EMAG".find(sub_char)

    if val == 18: return "MGAE".find(sub_char)
    if val == 19: return "MGEA".find(sub_char)
    if val == 20: return "MAGE".find(sub_char)
    if val == 21: return "MAEG".find(sub_char)
    if val == 22: return "MEGA".find(sub_char)
    if val == 23: return "MEAG".find(sub_char)

def get_personality(personality):
    val = personality % 25
    if val == 0:    return "hardy"
    if val == 1:    return "lonely"
    if val == 2:    return "brave"
    if val == 3:    return "adamant"
    if val == 4:    return "naughty"
    if val == 5:    return "bold"
    if val == 6:    return "docile"
    if val == 7:    return "relaxed"
    if val == 8:    return "impish"
    if val == 9:    return "lax"
    if val == 10:    return "timid"
    if val == 11:    return "hasty"
    if val == 12:    return "serious"
    if val == 13:    return "jolly"
    if val == 14:    return "naive"
    if val == 15:    return "modest"
    if val == 16:    return "mild"
    if val == 17:    return "quiet"
    if val == 18:    return "bashful"
    if val == 19:    return "rash"
    if val == 20:    return "calm"
    if val == 21:    return "gentle"
    if val == 22:    return "sassy"
    if val == 23:    return "careful"
    if val == 24:    return "quirky"
