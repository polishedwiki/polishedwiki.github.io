from py import cache, parser, pager
import sys, json, os

print('===== SITE BUILDER =====')
update = False
if '-nodl' not in sys.argv:
    print('Caching data files:')
    cache.download()
    update = cache.compare()
    print('-----')
if update or '-nocache' in sys.argv:
    print(f'Building site data:\n- base dex')
    dexBase, dexListBase = parser.build_dex()
    print(f'- {cache.mod} dex')
    dexMod, dexListMod = parser.build_dex(cache.mod, dexBase)
    print(f'- {cache.mod} learnsets')
    dexMod = parser.build_learnset(dexMod, cache.mod)
    print('- base moves')
    movesBase, movesListBase = parser.build_moves()
    movesBase = parser.fill_move_text(movesBase)
    print(f'- {cache.mod} moves')
    movesMod, movesListMod = parser.build_moves(cache.mod, movesBase)
    print('- base items')
    itemsBase, itemListBase = parser.build_items()
    print(f'- {cache.mod} items')
    itemsMod, itemListMod = parser.build_items(cache.mod, itemsBase)
    print(f'- {cache.mod} abilities')
    abilityListMod = parser.get_ability_list(dexMod)
    abilityBase = parser.build_abilities(abilityListMod)
    abilityMod = parser.build_abilities(abilityListMod, cache.mod, abilityBase)
    print(f'- {cache.mod} tiers')
    tiersBase, tierListBase = parser.build_format_tiers(dexMod)
    tiersMod, tierListMod = parser.build_format_tiers(dexMod, cache.mod, tiersBase)
    print(f'- {cache.mod} types')
    typeListMod = parser.get_type_list(dexMod)
    print('- dex icons', end='\r')
    iconURLs = cache.icons(dexMod)
    print('- dex sprites', end='\r')
    spriteURLs = cache.sprites(dexMod)
    print('- saving cache')
    for name, data in [['dexMod', dexMod], ['movesMod', movesMod], ['itemsMod', itemsMod], ['abilityMod', abilityMod], ['tiersMod', tiersMod], ['iconURLs', iconURLs], ['spriteURLs', spriteURLs]]:
        f = open(f'_cache/{name}.json', 'w')
        f.write(json.dumps(data))
        f.close()
    searchData = {
        "dexlist": dexListMod['mons'],
        "movelist": movesListMod['moves'],
        "itemlist": itemListMod['items'],
        "abilitylist": abilityListMod['abilities'],
        "tierlist": tierListMod,
        "typelist": typeListMod,
    }
    f = open('_cache/search-data.json', 'w')
    f.write(json.dumps(searchData))
    f.close()
    cache.dexMod = dexMod
    cache.movesMod = movesMod
    cache.itemsMod = itemsMod
    cache.abilityMod = abilityMod
    cache.tiersMod = tiersMod
    cache.iconURLs = iconURLs
    cache.spriteURLs = spriteURLs
    cache.searchData = searchData
else:
    print('Loading cache:')
    for name in ['dexMod', 'movesMod', 'itemsMod', 'abilityMod', 'tiersMod', 'iconURLs', 'spriteURLs', 'search-data']:
        print(f'- {name}')
        f = open(f'_cache/{name}.json')
        fdata = f.read()
        f.close()
        if name == 'dexMod':
            cache.dexMod = json.loads(fdata)
        elif name == 'movesMod':
            cache.movesMod = json.loads(fdata)
        elif name == 'itemsMod':
            cache.itemsMod = json.loads(fdata)
        elif name == 'abilityMod':
            cache.abilityMod = json.loads(fdata)
        elif name == 'tiersMod':
            cache.tiersMod = json.loads(fdata)
        elif name == 'iconURLs':
            cache.iconURLs = json.loads(fdata)
        elif name == 'spriteURLs':
            cache.spriteURLs = json.loads(fdata)
        elif name == 'search-data':
            cache.searchData = json.loads(fdata)
print('-----\nPaginating:')
if not os.path.isdir('_site'):
    os.mkdir('_site')
pager.__header_data = pager.build_header()
pager.build_dex()
pager.build_moves()
pager.build_items()
pager.build_abilities()
pager.build_tiers()
pager.build_types()
pager.build_index()
pager.build_search()
pager.copy_assets()
print('===== FINISHED =====')
