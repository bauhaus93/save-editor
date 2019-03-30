import logging
from struct import unpack, pack

from size import SECTION_FOOTER_OFFSET, SECTION_FOOTER_MARK, TEAM_SIZE_OFFSET, TEAM_PKMN_OFFSET, TEAM_PKMN_SIZE
from team import Team

logger = logging.getLogger()

class Section:
    def __init__(self, data):
        self.data = data
        self.id, self.checksum, self.save_index = unpack("<HH4xL", data[SECTION_FOOTER_OFFSET:SECTION_FOOTER_OFFSET + 12])

    def set_public_trainer_id(self, new_id):
        raw_id = unpack("<L", self.data[0xA:0xA + 4])[0]
        public_id = raw_id & 0xFFFF
        secret_id = raw_id >> 16
        raw_id = new_id | (secret_id << 16)
        self.data = self.data[:0xA] + pack("<L", raw_id) + self.data[0xA + 4:]
        self.update_checksum()
        logger.info("Setting new trainer id: {} -> {}".format(public_id, new_id))
        
    def get_public_trainer_id(self):
        raw_id = unpack("<L", self.data[0xA:0xA + 4])[0]
        public_id = raw_id & 0xFFFF
        #_secret_id = raw_id >> 16
        return public_id

    def read_team_size(self):
        return unpack("<L", self.data[TEAM_SIZE_OFFSET:TEAM_SIZE_OFFSET + 4])[0]

    def read_team(self):
        return Team(self.read_team_raw(), self.read_team_size())

    def read_team_raw(self):
        return self.data[TEAM_PKMN_OFFSET:TEAM_PKMN_OFFSET + TEAM_PKMN_SIZE]

    def write_team_size(self, size):
        self.data = self.data[:TEAM_SIZE_OFFSET] + pack("<L", size) + self.data[TEAM_SIZE_OFFSET + 4:]

    def write_team(self, team):
        self.write_team_size(team.get_size())
        self.data[:TEAM_PKMN_OFFSET] + team.into_bytes() + self.data[TEAM_PKMN_OFFSET + TEAM_PKMN_SIZE:]
        self.update_checksum()

    def write_footer(self):
        self.data = self.data[:SECTION_FOOTER_OFFSET] + pack("<HHLL", self.id, self.checksum, SECTION_FOOTER_MARK, self.save_index) + self.data[SECTION_FOOTER_OFFSET + 12:]
        
    def update_checksum(self):
        self.checksum = self.calculate_checksum()
        self.write_footer()

    def calculate_checksum(self):
        cs = 0
        data_size = get_section_size(self.id)
        unpack_str = "<{}L".format(data_size // 4)
        words = unpack(unpack_str, self.data[:data_size])
        for w in words:
            cs += w
        return ((cs & 0xFFFF) + ((cs >> 16) & 0xFFFF)) & 0xFFFF
    
    def into_bytes(self):
        return self.data

    def cs_differs(self):
        return self.checksum != self.calculate_checksum()

    def print_cs_info(self):
        diff = self.checksum - self.calculate_checksum()
        logger.info("id = {:2}, is = {:6}, calc = {:6}, diff = {:6}, 0x{:06X}".format(self.id, self.checksum, self.calculate_checksum(), diff, diff))

    def __str__(self):
        return "section id = {}, checksum = {}, save_index = {}".format(self.id, self.checksum, self.save_index)

def get_section_size(section_id):
    if section_id == 0:
        return 3884
    if section_id == 4:
        return 3848
    if section_id == 13:
        return 2000
    return 3968