import time
import logging
import copy

from hslog.parser import LogParser
from hslog.packets import Block, TagChange
from hslog.export import FriendlyPlayerExporter, EntityTreeExporter
from hearthstone.enums import (
    CardType, ChoiceType, GameTag, OptionType, BlockType,
    PlayReq, PlayState, PowerType, State, Step, Zone
)

# logging.getLogger().setLevel(logging.CRITICAL)

start = time.time()
parser = LogParser()
with open("Power.log") as f:
    parser.read(f)

packet_tree = parser.games[0]
print("Reading packets took ", time.time()-start, "s.")
exporter = EntityTreeExporter(packet_tree)
export = exporter.export()
game = export.game
breeky = game.players[0]
bob = game.players[1]
print("Export took ", time.time()-start, "s.")


def get_current_minions(player):
    minions = []
    for e in player.entities:
        if e.tags[GameTag.CONTROLLER] == player.tags[GameTag.CONTROLLER] and e.zone == Zone.PLAY:
            if GameTag.CARDTYPE in e.tags.keys() and e.tags[GameTag.CARDTYPE] == CardType.MINION:
                minions.append(e)
    return minions


def packet_start(packet):
    if packet.__class__ == Block:
        if packet.type == BlockType.TRIGGER:
            if export.find_entity(packet.entity, "FULL_ENTITY").tags[GameTag.CARDTYPE] == CardType.MOVE_MINION_HOVER_TARGET:
                return True
    return False


def packet_end(packet):
    if packet.__class__ == TagChange:
        if packet.tag == GameTag.STEP and packet.value == Step.MAIN_END:
            return True
    return False


def get_packets_at_combat(packets, k):
    n = 0
    start = 0
    packets_kept = []
    for i, packet in enumerate(packets, k):
        packets_kept.append(packet)
        if not start:
            if packet_start(packet):
                n += 1
                if n == k:
                    start = i
        else:
            if packet_end(packet):
                break
    return packets_kept





def get_number_fights(packet_tree):
    n = 0
    for packet in packet_tree.packets:
        if packet.__class__ == Block:
            if packet.type == BlockType.TRIGGER and packet.entity == 10:
                n += 1
    return n


def get_starting_block():
    trigger_blocks = []
    for packet in packet_tree.packets:
        if packet.__class__ == Block:
            if packet.type == BlockType.TRIGGER:
                trigger_blocks.append(packet)
    for block in trigger_blocks:
        if export.find_entity(block.entity, "FULL_ENTITY").tags[GameTag.CARDTYPE] == CardType.MOVE_MINION_HOVER_TARGET:
            print(block.entity)


def print_board_at_combat(k):
    pt = copy.copy(packet_tree)
    pt.packets = []
    current_fight = 0
    for i, packet in enumerate(packet_tree.packets):
        if is_starting_block(packet):
            current_fight += 1
            if current_fight == k:
                n = 10
                if i+n < len(packet_tree.packets):
                    pt.packets = packet_tree.packets[:i+n]
                    break
    exporter = EntityTreeExporter(pt)
    export = exporter.export()
    if hasattr(export, "game"):
        game = export.game
        breeky = game.players[0]
        bob = game.players[1]
        bob.minions = get_current_minions(bob)
        breeky.minions = get_current_minions(breeky)
        print("Bob : ", bob.minions)
        print("Breeky : ", breeky.minions)
        print(breeky.minions[0].tags[GameTag.HEALTH])


# print_board_at_combat(8)
# print("Getting board took ", time.time()-start, "s.")



for packet in packet_tree.packets:
    if packet.__class__ == Block:
        if packet.type == BlockType.TRIGGER:
            if export.find_entity(packet.entity, "FULL_ENTITY").tags[GameTag.CARDTYPE] == CardType.MOVE_MINION_HOVER_TARGET:
                p = packet
                break
