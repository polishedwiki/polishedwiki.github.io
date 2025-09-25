from py import cache, parser, pager
import sys, json

dexMod = False
movesMod = False
abilityMod = False
iconURLs = False

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
    print(f'- {cache.mod} abilities')
    abilityListMod = parser.get_ability_list(dexMod)
    abilityBase = parser.build_abilities(abilityListMod)
    abilityMod = parser.build_abilities(abilityListMod, cache.mod, abilityBase)
    print(f'- dex icons', end='\r')
    iconURLs = cache.icons(dexMod)
    print('- saving cache')
    for name, data in [['dexMod', dexMod], ['movesMod', movesMod], ['abilityMod', abilityMod], ['iconURLs', iconURLs]]:
        f = open(f'_cache/{name}.json', 'w')
        f.write(json.dumps(data))
        f.close()
else:
    print('Loading cache:')
    for name in ['dexMod', 'movesMod', 'abilityMod', 'iconURLs']:
        print(f'- {name}')
        f = open(f'_cache/{name}.json')
        fdata = f.read()
        f.close()
        if name == 'dexMod':
            dexMod = json.loads(fdata)
        elif name == 'movesMod':
            movesMod = json.loads(fdata)
        elif name == 'abilityMod':
            abilityMod = json.loads(fdata)
        elif name == 'iconURLs':
            iconURLs = json.loads(fdata)
print('-----\nPaginating:')
pager.__header_data = pager.build_header()
pager.build_index(dexMod, iconURLs)
pager.copy_assets()
print('===== FINISHED =====')
