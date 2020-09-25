import time
import logging
import copy
from typing import List

from hslog.parser import LogParser
from hslog.packets import Block, TagChange, Packet, PacketTree
from hslog.export import FriendlyPlayerExporter, EntityTreeExporter
from hearthstone.enums import (
    CardType, ChoiceType, GameTag, OptionType, BlockType,
    PlayReq, PlayState, PowerType, State, Step, Zone
)
from hearthstone.entities import Player


class StateExporter:

    def __init__(self, filepath="Power.log"):
        self.parser: LogParser = LogParser()
        with open(filepath) as f:
            self.parser.read(f)
        self.packet_tree: PacketTree = self.parser.games[0]
        self.exporter: EntityTreeExporter = EntityTreeExporter(self.packet_tree)
        self.export: EntityTreeExporter = self.exporter.export()

    def _packet_start(self, packet: Packet):
        if packet.__class__ == Block:
            if packet.type == BlockType.TRIGGER:
                if self.export.find_entity(packet.entity, "FULL_ENTITY").tags[GameTag.CARDTYPE] == CardType.MOVE_MINION_HOVER_TARGET:
                    return True
        return False

    def _packet_end(self, packet: Packet):
        if packet.__class__ == TagChange:
            if packet.tag == GameTag.STEP and packet.value == Step.MAIN_END:
                return True
        return False

    def get_packets_at_combat(self, packets: List[Packet], k: int):
        n = 0
        start = 0
        packets_kept = []
        for i, packet in enumerate(packets, k):
            packets_kept.append(packet)
            if not start:
                if self._packet_start(packet):
                    n += 1
                    if n == k:
                        start = i
            else:
                if self._packet_end(packet):
                    break
        return packets_kept

    def get_current_minions(self, player: Player):
        minions = []
        for e in player.entities:
            if e.tags[GameTag.CONTROLLER] == player.tags[GameTag.CONTROLLER] and e.zone == Zone.PLAY:
                if GameTag.CARDTYPE in e.tags.keys() and e.tags[GameTag.CARDTYPE] == CardType.MINION:
                    minions.append(e)
        return minions
