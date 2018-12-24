import numpy as np
from readinput import read_input
import pdb
import copy
import time


class Group:

    __slots__ = ['id', 'type', 'num_units',
                 'hit_points', 'weaknesses', 
                 'immunities', 'damage', 'damage_type', 'initiative']
    def __init__(self, id_, typ, num_units, 
                 hit_points, weaknesses, 
                 immunities, damage, damage_type, initiative):
        self.id = id_
        self.type = typ
        self.num_units = num_units
        self.hit_points = hit_points
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.damage = damage
        self.damage_type = damage_type
        self.initiative = initiative
    
    def get_effective_power(self):
        return self.num_units*self.damage

    def take_damage(self, damage):
        while damage >= self.hit_points:
            self.num_units -= 1
            damage -= self.hit_points
            
    def is_dead(self):
        return self.num_units <= 0

    def __str__(self):
        return '{}: Group {}, {} units, {} hp, {} weaknesses, {} immunities, {} {} damage, {} initiative, {} EP;'\
                .format(self.type, self.id, self.num_units, self.hit_points,
                       self.weaknesses, self.immunities, self.damage,
                       self.damage_type, self.initiative, self.get_effective_power())

    def __repr__(self):
        return str(self)


def get_damage_potential(g1, g2):
    if g1.type == g2.type:
        return 0
    elif g1.damage_type in g2.immunities:
        return 0
    damage = g1.get_effective_power()
    if g1.damage_type in g2.weaknesses:
        return damage*2
    else:
        return damage


def is_over(groups):
    types = set()
    for group in groups:
        types.add(group.type)
        if len(types) > 1:
            return False
    return True


def print_groups(groups):
    for g in groups:
        print(g)
        print()


inp = [l.replace('\n', '') for l in read_input('input.txt', str)]

groups = []

id_ = 1
typ = "Immune System"
for line in inp:
    if 'Immune System' in line:
        continue
    elif 'Infection' in line:
        typ = 'Infection'
        continue
    elif not line:
        continue
    num_units = int(line.split(' units each')[0])
    hit_points = int(line.split(' ')[4])
    
    weak_immun_list = line.split('hit points ')[1]\
            .split(' with an attack')[0]

    weaknesses = []
    immunities = []
    if 'weak' in weak_immun_list or 'immune' in weak_immun_list:
        weak_immun_list = weak_immun_list\
                .replace('(', '').replace(')', '')
        wi_split = weak_immun_list.split(';')
        for part in wi_split:
            if 'weak' in part:
                npart = part.split('weak to ')[1]
                weaknesses.extend(npart.split(', '))
            elif 'immune' in part:
                npart = part.split('immune to ')[1]
                immunities.extend(npart.split(', '))

    damage = int(line.split('that does ')[1].split(' ')[0])
    damage_type = line.split(' damage at initiative')[0].split(' ')[-1]
    initiative = int(line.split(' ')[-1])
    group = Group(id_, typ, num_units, hit_points,
                  weaknesses, immunities, damage, damage_type, initiative)
    groups.append(group)
    id_ += 1


while not is_over(groups):

    #pdb.set_trace()
    groups_to_remove = set()
    # selection phase
    attacks = {}
    gets_attacked = set()
    groups_sorted = sorted(groups, key=lambda g: (g.get_effective_power(),
                                               g.initiative),
                        reverse=True)
    for group in groups_sorted:
        group_to_attack = max(filter(lambda g: g.id not in gets_attacked,
                                     groups), 
                              key=lambda g: (
                                  get_damage_potential(group, g),
                                  g.get_effective_power(),
                                  g.initiative))
        if get_damage_potential(group, group_to_attack) == 0:
            attacks[group.id] = None
        else:
            attacks[group.id] = group_to_attack
            gets_attacked.add(group_to_attack.id)

    # attacking phase
    for group in sorted(groups, key=lambda g: g.initiative, reverse=True):
        if group in groups_to_remove:
            # you are dead, you can't attack
            continue

        group_to_attack = attacks[group.id]
        if group_to_attack is not None:
            # attack
            damage = get_damage_potential(group, group_to_attack)
            group_to_attack.take_damage(damage)
            if group_to_attack.is_dead():
                groups_to_remove.add(group_to_attack)

    for group in groups_to_remove:
        groups.remove(group)

print("Winning army has", sum(g.num_units for g in groups))

