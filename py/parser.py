import json

def build_dex(mod='base', dexOverride=False):
    data_file = open(f'_cache/{mod}/pokedex.ts')
    ts_data = data_file.readlines()
    data_file.close()
    # parse mons
    dex = {}
    if dexOverride:
        dex = dexOverride
    dexlist = {
        "mons": []
    }
    in_mon = False
    is_cosmetic = False
    name = ''
    dname = False
    bst = False
    types = False
    abil = False
    prevo = False
    evos = False
    for line in ts_data:
        if line.find('export const') > -1 or line.find('\t\t}') > -1 or line.find('//') > -1:
            continue
        elif line.find(': {') > -1 and in_mon == False: # open object
            in_mon = True
            name = line.split(':')[0].strip()
        elif in_mon and line.find('name:') > -1: # explicit name
            dname = line[line.find('"')+1:]
            dname = dname[:dname.find('"')]
        elif in_mon and line.find('baseStats:') > -1: # bst
            bst_s = line[line.find('{')+1:line.find('}')].split(',')
            for i in range(len(bst_s)):
                bst_s[i] = '"' + bst_s[i]
                bst_s[i] = bst_s[i].replace(' ', '').replace(':', '":')
            bst_s = '{' + ','.join(bst_s) + '}'
            bst = json.loads(bst_s)
        elif in_mon and line.find('types:') > -1: # type
            types_s = line[line.find('[')+1:line.find(']')].replace(' ', '').replace('"', '')
            types = types_s.split(',')
        elif in_mon and line.find('abilities:') > -1: # abilities
            abil_s = line[line.find('{')+1:line.find('}')]
            abil_s = abil_s.replace('0:', '').replace('1:', '').replace('H:', '').replace('S:', '')
            abil_s = abil_s.replace('"', '').replace(' ', '').replace('-', '').lower()
            abil = abil_s.split(',')
        elif in_mon and line.find('prevo:') > -1: # pre-evolutions
            prevo = line[line.find('"')+1:]
            prevo = prevo[:prevo.find('"')]
            prevo = prevo.lower().replace(' ', '').replace('.', '').replace('-', '').replace("\\u2019", '')
        elif in_mon and line.find('evos:') > -1: # evos
            evos_s = line[line.find('[')+1:line.find(']')].replace(' ', '').replace('"', '')
            evos_s = evos_s.lower().replace(' ', '').replace('.', '').replace('-', '').replace("\\u2019", '')
            evos = evos_s.split(',')
        elif in_mon and line.find('isCosmeticForme:') > -1: # special for polished formes
            is_cosmetic = True
        elif in_mon and line.find('\t},') > -1 or in_mon and line.find('    },') > -1: # close object
            in_mon = False
            if is_cosmetic:
                is_cosmetic = False
                continue
            if name == 'egg':
                continue
            dexlist['mons'].append(name)
            # enter or override fields
            if name not in dex:
                dex[name] = {}
            if dname:
                dex[name]['name'] = dname
                dname = False
            if bst:
                dex[name]['bst'] = bst
                bst = False
            if types:
                dex[name]['types'] = types
                types = False
            if abil:
                dex[name]['abilities'] = abil
                abil = False
            if prevo:
                dex[name]['prevo'] = prevo
                prevo = False
            if evos:
                dex[name]['evos'] = evos
                evos = False
    if dexOverride: # clear unused entries
        to_del = []
        for mon, data in dex.items():
            if mon not in dexlist['mons']:
                to_del.append(mon)
        for mon in to_del:
            del dex[mon]
    return dex, dexlist

def build_learnset(dex, mod='base'):
    data_file = open(f'_cache/{mod}/learnsets.ts')
    ts_data = data_file.read()
    data_file.close()
    ts_data = ts_data.replace('hijumpkick', 'highjumpkick') # polished override
    # parse learnset
    for mon, data in dex.items():
        slice_data = ts_data[ts_data.find(mon+':'):]
        slice_data = slice_data[slice_data.find('learnset'):]
        slice_data = slice_data[slice_data.find('{')+1:slice_data.find('},')]
        slice_data = slice_data.split('],')
        for i in range(len(slice_data)):
            slice_data[i] = slice_data[i][:slice_data[i].find(':')]
            slice_data[i] = slice_data[i].strip().replace(' ', '')
        slice_data.pop() # remove empty last element
        dex[mon]['learnset'] = slice_data
    return dex

def build_moves(mod='base', moveOverride=False):
    data_file = open(f'_cache/{mod}/moves.ts')
    ts_data = data_file.readlines()
    data_file.close()
    # parse moves
    moves = {}
    if moveOverride:
        moves = moveOverride
    movelist = {
        "moves": []
    }
    in_move = False
    non_standard = False
    name = ''
    dname = False
    cat = False
    acc = False
    bp = False
    pp = False
    type = False
    desc = False
    for line in ts_data:
        if line.find('export const') > -1 or line.find('\t\t}') > -1 or line.find('//') > -1:
            continue
        elif line.find(': {') > -1 and in_move == False: # open object
            in_move = True
            name = line.split(':')[0].strip().replace('"', '')
            if name == 'hijumpkick': # polished override
                name = 'highjumpkick'
        elif in_move and line.find('name:') > -1: # explicit name
            dname = line[line.find('"')+1:]
            dname = dname[:dname.find('"')]
        elif in_move and line.find('category:') > -1: # phys/spec category
            cat = line[line.find('"')+1:]
            cat = cat[:cat.find('"')]
        elif in_move and line.find('accuracy:') > -1: # accuracy
            acc_s = line[line.find(':')+1:line.find(',')]
            acc = acc_s.strip()
            acc = '100' if acc == 'true' else acc
        elif in_move and line.find('basePower:') > -1: # bp
            bp_s = line[line.find(':')+1:line.find(',')]
            bp = bp_s.strip()
        elif in_move and line.find('pp:') > -1: # pp
            pp_s = line[line.find(':')+1:line.find(',')]
            pp = pp_s.strip()
        elif in_move and line.find('type:') > -1: # type
            type = line[line.find('"')+1:]
            type = type[:type.find('"')]
        elif in_move and line.find('shortDesc:') > -1:
            desc = line[line.find('"')+1:]
            desc = desc[:desc.find('"')]
        elif in_move and moveOverride and line.find('isNonstandard:') > -1:
            non_standard = True
        elif in_move and line.find('\t},') > -1 or in_move and line.find('    },') > -1: # close object
            in_move = False
            if non_standard:
                non_standard = False
                continue
            movelist['moves'].append(name)
            # enter or override fields
            if name not in moves:
                moves[name] = {}
            if dname:
                moves[name]['name'] = dname
                dname = False
            if cat:
                moves[name]['category'] = cat
                cat = False
            if type:
                moves[name]['type'] = type
                type = False
            if acc:
                moves[name]['accuracy'] = acc
                acc = False
            if bp:
                moves[name]['bp'] = bp
                bp = False
            if pp:
                moves[name]['pp'] = pp
                pp = False
            if desc:
                moves[name]['desc'] = desc
                desc = False
    if moveOverride: # clear unused entries
        to_del = []
        for move, data in moves.items():
            if move not in movelist['moves']:
                to_del.append(move)
        for move in to_del:
            del moves[move]
    return moves, movelist

def build_items(mod='base', itemOverride=False):
    data_file = open(f'_cache/{mod}/{'text-items' if mod == 'base' else 'items'}.ts')
    ts_data = data_file.readlines()
    data_file.close()
    # parse moves
    items = {}
    if itemOverride:
        items = itemOverride
    itemlist = {
        "items": []
    }
    in_item = False
    name = ''
    dname = False
    desc = False
    for line in ts_data:
        if line.find('export const') > -1 or line.find('\t\t}') > -1 or line.find('//') > -1:
            continue
        elif line.find(': {') > -1 and in_item == False: # open object
            in_item = True
            name = line.split(':')[0].strip().replace('"', '')
        elif in_item and line.find('name:') > -1: # explicit name
            dname = line[line.find('"')+1:]
            dname = dname[:dname.find('"')]
        elif in_item and line.find('shortDesc:') > -1:
            desc = line[line.find('"')+1:]
            desc = desc[:desc.find('"')]
        elif in_item and line.find('\t},') > -1 or in_item and line.find('    },') > -1: # close object
            in_item = False
            itemlist['items'].append(name)
            # enter or override fields
            if name not in items:
                items[name] = {}
            if dname:
                items[name]['name'] = dname
                dname = False
            if desc:
                items[name]['desc'] = desc
                desc = False
    if itemOverride: # clear unused entries
        to_del = []
        for item, data in items.items():
            if item not in itemlist['items']:
                to_del.append(item)
        for item in to_del:
            del items[item]
    return items, itemlist

def fill_move_text(moves):
    data_file = open('_cache/base/text-moves.ts')
    ts_data = data_file.read()
    data_file.close()
    for move, data in moves.items():
        if 'desc' not in data:
            slice_data = ts_data[ts_data.find(move+':'):]
            slice_data = slice_data[slice_data.find('shortDesc:'):]
            slice_data = slice_data[slice_data.find('"')+1:]
            slice_data = slice_data[:slice_data.find('"')]
            moves[move]['desc'] = slice_data
    return moves

def build_abilities(abilitylist, mod='base', abilityOverride=False):
    data_file = open(f'_cache/{mod}/{'text-abilities' if mod == 'base' else 'abilities'}.ts')
    ts_data = data_file.read()
    data_file.close()
    # parse abilities
    abilities = {}
    if abilityOverride:
        abilities = abilityOverride
    for a in abilitylist['abilities']:
        if ts_data.find(a+':') > -1:
            if a not in abilities:
                abilities[a] = {}
            slice_data_str = ts_data[ts_data.find(a+':'):]
            if slice_data_str.find('name:') > -1:
                slice_data = slice_data_str[slice_data_str.find('name:'):]
                slice_data = slice_data[slice_data.find('"')+1:]
                slice_data = slice_data[:slice_data.find('"')]
                abilities[a]['name'] = slice_data
            if slice_data_str.find('shortDesc:') > -1:
                slice_data = slice_data_str[slice_data_str.find('shortDesc:'):]
                slice_data = slice_data[slice_data.find('"')+1:]
                slice_data = slice_data[:slice_data.find('"')]
                abilities[a]['desc'] = slice_data
    return abilities

def get_ability_list(dex):
    a_list = []
    for mon, data in dex.items():
        if 'abilities' in data:
            a_list += data['abilities']
    a_list = list(dict.fromkeys(a_list))
    abilitylist = {
        'abilities': a_list
    }
    return abilitylist

def build_format_tiers(dex, mod='base', tierOverride=False):
    data_file = open(f'_cache/{mod}/formats-data.ts')
    ts_data = data_file.read()
    data_file.close()
    # parse formats
    tiers = {}
    tierList = []
    if tierOverride:
        tiers = tierOverride
    for name, data in dex.items():
        if ts_data.find(name+':') > -1:
            slice_data_str = ts_data[ts_data.find(name+':'):]
            if slice_data_str.find('tier:') > -1:
                slice_data = slice_data_str[slice_data_str.find('tier:'):]
                slice_data = slice_data[slice_data.find('"')+1:]
                slice_data = slice_data[:slice_data.find('"')]
                tiers[name] = slice_data
                if slice_data not in tierList:
                    tierList.append(slice_data)
    return tiers, tierList

def get_type_list(dex):
    t_list = []
    for mon, data in dex.items():
        if 'types' in data:
            t_list += data['types']
    t_list = list(dict.fromkeys(t_list))
    return t_list
