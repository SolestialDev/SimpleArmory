import { getData } from '$api/_blizzard'
import { getJsonDb } from '$api/_db'
import { getProfile } from '$api/profile'
import { parseCollectablesObject } from '$api/_collectables'
import Cache from '$api/_cache'

const slots = {
    0: "Head",
    1: "Shoulder",
    2: "Body",
    3: "Chest",
    4: "Waist",
    5: "Legs",
    6: "Boots",
    7: "Wrist",
    8: "Hand",
    9: "Cloak",
    10: "Tabard",
    11: "Two-Hand",
    12: "Ranged",
    13: "Shield",
    15: "One-Hand"
};

let _cache;
export async function getTransmogItems(region, realm, character, type) {
    if (!_cache) {
        _cache = new Cache(region, realm, character);
    }
    else if (_cache.isValid(region, realm, character)) {
        return _cache.cache;
    }

    console.log(`Parsing transmog.json...`)


    // get profile
    const profile = await getProfile(region, realm, character);
    if (!profile || (profile.status && profile.status === 404)) {
        return undefined;
    }

    // get json
    const db = await getJsonDb("transmog");

    // get character collected
    const collected = await getData(region, realm, character, 'collections/transmogs');
    if (!collected || (collected.status && collected.status === 404)) {
        return undefined;
    }

    console.log(db[type])

    // combine
    _cache.update(
        region,
        realm,
        character,
        parseCollectablesObject(db[type], profile, collected, 'slots', 'appearances', false, false, type)
    )
    return _cache.cache;
}