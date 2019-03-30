from struct import unpack, pack

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
        encrypted_data = unpack("<48s", pkmn_data[32:80])[0]
        self.data = crypt_data(encrypted_data, self.ot_id, self.personality)
        self.status_condition = unpack("<L", pkmn_data[80:84])[0]
        self.level = unpack("<B", pkmn_data[84:85])[0]
        self.pokerus = unpack("<B", pkmn_data[85:86])[0]
        self.curr_hp, self.total_hp = unpack("<HH", pkmn_data[86:90])
        self.stats = unpack("<5H", pkmn_data[90:])
        
        self.load_evs()
    
    #evs not like in vanilla frlg, must look further
    def load_evs(self):
        ev_sub_offset = 12 * get_substructure_index(self.personality, 'E')
        self.evs = unpack("<6B", self.data[ev_sub_offset:ev_sub_offset + 6])

    def __str__(self):
        output = "Pkmn:\n"
        output += "\tPersonality:\t{}\n".format(get_personality(self.personality))
        output += "\tLevel:\t\t{:3}\n".format(self.level)
        output += "\thp:\t\t{}/{}\n".format(self.curr_hp, self.total_hp)
        output += "\tStats:"
        output += "\tAtt:\t{:3}\n\t\tDef:\t{:3}\n\t\tSpd:\t{:3}\n\t\tSpAtt:\t{:3}\n\t\tSpDef:\t{:3}\n".format(*self.stats)
        output += "\tEVs:"
        output += "\tHP:\t{:3}\n\t\tAtt:\t{:3}\n\t\tDef:\t{:3}\n\t\tSpd:\t{:3}\n\t\tSpAtt:\t{:3}\n\t\tSpDef:\t{:3}\n".format(*self.evs)
        output += "\tChecksum:\t0x{:04X}\n".format(self.checksum)
        return output

    def into_bytes(self):
        output = bytes()
        output += pack("<LL10sH7sBHH48sLBBHH5H",
            self.personality, self.ot_id, self.nickname, self.language, self.ot_name,
            self.markings, self.checksum, self.unknown, self.data, self.status_condition, self.level,
            self.pokerus, self.curr_hp, self.total_hp, *self.stats)
        #todo handle EVs
        if len(output) != 100:
            print("Pokemon.into_bytes(): data not of size 100:", len(output))
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
