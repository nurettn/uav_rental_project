from enum import Enum


class TeamEnum(Enum):
    WING = "Wing"
    FUSELAGE = "Fuselage"
    TAIL = "Tail"
    AVIONICS = "Avionics"
    ASSEMBLY = "Assembly"
    NOTEAM = "NoTeam"


TEAM_PART_MAPPING = {
    TeamEnum.WING.value: ["Wing"],
    TeamEnum.FUSELAGE.value: ["Fuselage"],
    TeamEnum.TAIL.value: ["Tail"],
    TeamEnum.AVIONICS.value: ["Avionics"],
    TeamEnum.ASSEMBLY.value: [],
    TeamEnum.NOTEAM.value: [],
}
