import logging
from struct import unpack, pack

from section import Section
from size import SECTION_SIZE

logger = logging.getLogger()

class SaveBlock:
    def __init__(self, data):
        self.sections = list()
        for i in range(14):
            start = SECTION_SIZE * i
            stop = SECTION_SIZE * (i + 1)
            section = Section(data[start:stop])
            self.sections.append(section)

    def get_save_index(self):
        return self.sections[0].save_index

    def set_public_trainer_id(self, new_id):
        for section in self.sections:
            if section.id == 0:
                section.set_public_trainer_id(new_id)
    def get_public_trainer_id(self):
        for section in self.sections:
            if section.id == 0:
                return section.get_public_trainer_id()
        return None
    
    def read_team(self):
        for section in self.sections:
            if section.id == 1:
                return section.read_team()
        return None

    def read_team_raw(self):
        for section in self.sections:
            if section.id == 1:
                return section.read_team_raw()
        return None

    def write_team(self, team):
        logger.info("Writing team to save")
        for section in self.sections:
            if section.id == 1:
                section.write_team(team)
                logger.info("Wrote team to save")
                return
        logger.warn("Could not find section for team")

    def into_bytes(self):
        data = bytes()
        for section in self.sections:
            data = data + section.into_bytes()
        return data

    def print_cs_info(self):
        for section in self.sections:
            section.print_cs_info()

    def __str__(self):
        output = "Saveblock:\n"
        for section in self.sections:
            output += "{}\n".format(section)
        return output