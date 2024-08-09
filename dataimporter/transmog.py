#!/usr/bin/env python3

from .fixer import WowToolsFixer
from .tools import changelog, icat

IGNORE_APPEARANCE_ID = [
]

SLOTS = {
    0: 'Head',
    1: 'Shoulder',
    2: 'Body',
    3: 'Chest',
    4: 'Waist',
    5: 'Legs',
    6: 'Boots',
    7: 'Wrist',
    8: 'Hand',
    9: 'Cloak',
    10: 'Tabard',
    11: 'Two-Hand',
    12: 'Ranged',
    13: 'Shield',
    15: 'One-Hand'
}

class TransmogFixer(WowToolsFixer):

    def _store_init(self, appearance):
        self.appearances = appearance
        self.id_to_old_appearances = {}

        self.dbc_appearances = {
            e['ID']: e for e in self.dbc_get_table('itemappearance')
        }
    
        self.register_old_appearances()

    def register_old_appearances(self):
        for cat in self.appearances:
            for subcat in cat['subcats']:
                for item in subcat['items']:
                    self.id_to_old_transmog_items[int(item['ID'])] = item

    def get_appearance(self, appearance_id):
        appearance_id = str(appearance_id)

        # Icon
        icon_id = self.dbc_appearances[appearance_id]['DefaultIconFileDataID']
        icon_name = self.get_icon_name(int(icon_id))

        return {
            'ID': int(appearance_id),
            'icon': icon_name,
        }

    def fix_missing_appearance(self, appearance_id):
        appearance = self.get_appearance(appearance_id)
        if appearance is None:
            return

        displaytype = self.dbc_appearances[appearance_id]['DisplayType']

        if int(displaytype) == 14:
            return

        changelog('Appearance {} missing '
                .format(appearance_id, appearance['ID']))

        icat(self.appearances, SLOTS[int(displaytype)], 'TODO')['items'].append(appearance)

    def fix_missing_appearances(self):
        for appearance_id in self.dbc_appearances:
            if (int(appearance_id) not in self.id_to_old_appearances
                    and int(appearance_id) not in IGNORE_APPEARANCE_ID):
                self.fix_missing_appearance(appearance_id)

    def fix_types_data(self):
        for cat in self.appearances:
            for subcat in cat['subcats']:
                for item in subcat['items']:
                    fixed_appearance = self.get_appearance(int(item['ID']))
                    item['ID'] = fixed_appearance['ID']

                    if (
                        fixed_appearance['icon'] != '0'
                        and item['icon'].lower()
                            != fixed_appearance['icon'].lower()
                    ):
                        item['icon'] = fixed_appearance['icon']

    def run(self):
        self.fix_missing_appearances()
        self.fix_types_data()
        return [self.appearances]
