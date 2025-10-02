import os, shutil
from py import cache

# config vars
site_title = 'Polished Wiki'

__header_data = False

def build_header():
    f = open('pages/site-header.html')
    _head = f.read()
    f.close()
    return _head

def build_dex():
    print ('- dex')
    for mon in cache.searchData['dexlist']:
        __build_dex_page(mon)

def build_moves():
    print('- moves')
    for move in cache.searchData['movelist']:
        __build_move_page(move)

def build_items():
    print('- items')
    for item in cache.searchData['itemlist']:
        __build_item_page(item)

def build_abilities():
    print('- abilities')
    for ability in cache.searchData['abilitylist']:
        __build_ability_page(ability)

def build_tiers():
    print('- tiers')
    for tier in cache.searchData['tierlist']:
        __build_tier_page(tier)

def build_index():
    print('- index')
    f = open('pages/index.html')
    html = f.read()
    f.close()
    # parse mon list
    buf = '<div class="dex-head"><h2 id="title">Pokémon</h2><h2 id="tier">Tier</h2></div>'
    buf += __build_dex_list(cache.searchData['dexlist'])
    html = html.replace(__comment_tag('PAGE_BODY'), buf)
    # insert headers
    html = __insert_header(html)
    html = __insert_title(html)
    html = html.replace('SITE_INDEX', '')
    __save(html, 'index.html')

def copy_assets():
    print('- assets')
    shutil.copytree('pages/style', '_site/style', dirs_exist_ok=True)
    shutil.copytree('pages/assets', '_site/assets', dirs_exist_ok=True)


def __build_dex_page(mon):
    f = open('pages/dex.html')
    html_temp = f.read()
    f.close()
    if not os.path.isdir('_site/dex'):
        os.mkdir('_site/dex')
    if not os.path.isdir(f'_site/dex/{mon}'):
        os.mkdir(f'_site/dex/{mon}')
    data = cache.dexMod[mon]
    # name & mon display
    html = html_temp.replace('MON_NAME', __mon_name_format(data['name']))
    html = html.replace('MON_SPRITE', cache.spriteURLs[mon])
    # types
    buf = ''
    typeLen = len(data['types'])
    for i in range(typeLen):
        id = ''
        if typeLen == 1:
            id = 'only-type'
        elif i == 0:
            id ='first-type'
        buf += f'<img class="mon-type" id="{id}" src="{__type_img(data['types'][i])}">'
    html = html.replace(__comment_tag('MON_TYPE'), buf)
    # tier
    buf = f'<a href="../../tier/{cache.tiersMod[mon].lower()}">Tier: {cache.tiersMod[mon]}</a>'
    html = html.replace('MON_TIER', buf)
    # bst
    buf = ''
    for stat in ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']:
        statNum = data['bst'][stat.lower()]
        barDisplay = round(statNum * (100/255 * 0.8))
        if barDisplay < 1:
            barDisplay = 1
        elif barDisplay > 80:
            barDisplay = 80
        buf += f'<div class="stat">{stat}: {statNum}</div><div class="stat-bar" style="width: {barDisplay}%;"></div><br>'
    html = html.replace(__comment_tag('MON_STATS'), buf)
    # evolution
    prevEvos = []
    if 'prevo' in data or 'evos' in data:
        buf = '<div class="evo-link"><h3>Evolutions</h3>'
        if 'prevo' in data and data['prevo'] in cache.dexMod:
            prevEvos.append(data['prevo'])
            if 'prevo' in cache.dexMod[data['prevo']]:
                prevEvos.insert(0, cache.dexMod[data['prevo']]['prevo'])
        for evo in prevEvos:
            buf += f'<a href="../{evo}">{__insert_dex_evo(evo)}</a> &#8592; '
        buf += f'{__insert_dex_evo(mon)}'
        if 'evos' in data:
            buf += ' &#8594; '
            evoLen = len(data['evos'])
            for i in range(evoLen):
                if data['evos'][i] in cache.dexMod:
                    if i > 0:
                        buf += ' &nbsp;<i>or</i>&nbsp; '
                    buf += f'<a href="../{data['evos'][i]}">{__insert_dex_evo(data['evos'][i])}</a>'
                    if 'evos' in cache.dexMod[data['evos'][i]]:
                        buf += ' &#8594; '
                        nextEvoLen = len(cache.dexMod[data['evos'][i]]['evos'])
                        for j in range(nextEvoLen):
                            if j > 0:
                                buf += ' &nbsp;<i>or</i>&nbsp; '
                            nextEvo = cache.dexMod[data['evos'][i]]['evos'][j]
                            buf += f'<a href="../{nextEvo}">{__insert_dex_evo(nextEvo)}</a>'
        buf += '</div>'
    else:
        buf = ''
    html = html.replace(__comment_tag('MON_EVOLUTION'), buf)
    # overview (TODO: THIS IS PLACEHOLDER)
    html = html.replace(__comment_tag('MON_OVERVIEW'), 'No analysis is available for this species.')
    # abilities
    html = html.replace(__comment_tag('MON_ABILITY'), __build_ability_list(data['abilities'], '../../'))
    # moves
    monLearnset = data['learnset']
    for prevo in prevEvos:
        monLearnset += cache.dexMod[prevo]['learnset']
    monLearnset = list(dict.fromkeys(monLearnset))
    html = html.replace(__comment_tag('MON_MOVES'), __build_move_list(monLearnset, '../../'))
    # insert headers
    html = __insert_header(html)
    html = __insert_title(html)
    html = html.replace('SITE_INDEX', '../..')
    __save(html, 'index.html', f'dex/{mon}')

def __build_move_page(move):
    f = open('pages/data.html')
    html_temp = f.read()
    f.close()
    if not os.path.isdir('_site/move'):
        os.mkdir('_site/move')
    if not os.path.isdir(f'_site/move/{move}'):
        os.mkdir(f'_site/move/{move}')
    # move
    data = cache.movesMod[move]
    html = html_temp.replace('DATA_NAME', data['name'])
    buf = __build_move_list([move], '../../')
    # mon learnset list
    monsWithMove = []
    for mon in cache.searchData['dexlist']:
        if move in cache.dexMod[mon]['learnset']:
            monsWithMove.append(mon)
    monsWithMove.sort()
    buf += '<h2 id="move-header">Move Compatibility</h2>'
    buf += __build_dex_list(monsWithMove, '../../')
    html = html.replace(__comment_tag('PAGE_BODY'), buf)
    # insert headers
    html = __insert_header(html)
    html = __insert_title(html)
    html = html.replace('SITE_INDEX', '../..')
    __save(html, 'index.html', f'move/{move}')

def __build_ability_page(ability):
    f = open('pages/data.html')
    html_temp = f.read()
    f.close()
    if not os.path.isdir('_site/ability'):
        os.mkdir('_site/ability')
    if not os.path.isdir(f'_site/ability/{ability}'):
        os.mkdir(f'_site/ability/{ability}')
    # ability
    data = cache.abilityMod[ability]
    html = html_temp.replace('DATA_NAME', data['name'])
    buf = __build_ability_list([ability], '../../')
    # mon ability list
    monsWithAbility = []
    for mon in cache.searchData['dexlist']:
        if ability in cache.dexMod[mon]['abilities']:
            monsWithAbility.append(mon)
    monsWithAbility.sort()
    buf += '<h2 id="ability-header">Ability Compatibility</h2>'
    buf += __build_dex_list(monsWithAbility, '../../')
    html = html.replace(__comment_tag('PAGE_BODY'), buf)
    # insert headers
    html = __insert_header(html)
    html = __insert_title(html)
    html = html.replace('SITE_INDEX', '../..')
    __save(html, 'index.html', f'ability/{ability}')

def __build_item_page(item):
    f = open('pages/data.html')
    html_temp = f.read()
    f.close()
    if not os.path.isdir('_site/item'):
        os.mkdir('_site/item')
    if not os.path.isdir(f'_site/item/{item}'):
        os.mkdir(f'_site/item/{item}')
    # item
    data = cache.itemsMod[item]
    html = html_temp.replace('DATA_NAME', data['name'])
    buf = __build_item_list([item], '../../')
    html = html.replace(__comment_tag('PAGE_BODY'), buf)
    # insert headers
    html = __insert_header(html)
    html = __insert_title(html)
    html = html.replace('SITE_INDEX', '../..')
    __save(html, 'index.html', f'item/{item}')

def __build_tier_page(tier):
    f = open('pages/data.html')
    html_temp = f.read()
    f.close()
    nameFlat = tier.lower()
    if not os.path.isdir('_site/tier'):
        os.mkdir('_site/tier')
    if not os.path.isdir(f'_site/tier/{nameFlat}'):
        os.mkdir(f'_site/tier/{nameFlat}')
    # tier
    html = html_temp.replace('DATA_NAME', tier)
    monsInTier = []
    for mon in cache.searchData['dexlist']:
        if cache.tiersMod[mon] == tier:
            monsInTier.append(mon)
    monsInTier.sort()
    buf = f'<h2 id="tier-header">{tier} Tier</h2>'
    buf += __build_dex_list(monsInTier, '../../')
    html = html.replace(__comment_tag('PAGE_BODY'), buf)
    # insert headers
    html = __insert_header(html)
    html = __insert_title(html)
    html = html.replace('SITE_INDEX', '../..')
    __save(html, 'index.html', f'tier/{nameFlat}')

def __build_ability_list(abilities, path=''):
    abilities.sort()
    buf = '<div class="ability-list" align="center">'
    for a in abilities:
        ability = cache.abilityMod[a]
        buf += f'<a href="{path}ability/{a}" {'id="ability-single"' if len(abilities) == 1 else ''}><span id="ability-name">{ability['name']}</span>{ability['desc']}</a>'
    buf += '</div>'
    return buf

def __build_item_list(items, path=''):
    items.sort()
    buf = '<div class="item-list" align="center">'
    for i in items:
        item = cache.itemsMod[i]
        buf += f'<a href="{path}item/{i}" {'id="item-single"' if len(items) == 1 else ''}><span id="item-name">{item['name']}</span>{item['desc']}</a>'
    buf += '</div>'
    return buf

def __build_move_list(moves, path=''):
    moves.sort()
    buf = '<div class="move-list" align="center">'
    for m in moves:
        move = cache.movesMod[m]
        # name / category / type
        buf += f'<a href="{path}move/{m}" {'id="move-single"' if len(moves) == 1 else ''}><span id="move-name">{move['name']}</span>'
        buf += f'<div class="move-detail" align="center"><h6>Category</h6><br><img src="{__category_img(move['category'])}"></div>'
        buf += f'<div class="move-detail" align="center"><h6>Type</h6><br><img src="{__type_img(move['type'])}"></div>'
        # bp
        try:
            bp = int(move['bp'])
            if bp < 1:
                bp = '—'
        except:
            bp = '—'
        buf += f'<div class="move-detail" align="center"><h6>Power</h6><br>{bp}</div>'
        # accuracy
        try:
            acc = int(move['accuracy'])
            if acc <= 1:
                acc= '—'
            else:
                acc = f'{acc}%'
        except:
            acc = '—'
        buf += f'<div class="move-detail" align="center"><h6>Accuracy</h6><br>{acc}</div>'
        # pp / desc
        buf += f'<div class="move-detail" align="center"><h6>PP</h6><br>{move['pp']}</div>'
        buf += f'<div id="move-desc">{move['desc']}</div>'
        buf += '</a>'
    buf += '</div>'
    return buf

def __build_dex_list(mons, path=''):
    mons.sort()
    buf = '<div class="dex-list" align="center">'
    for mon in mons:
        data = cache.dexMod[mon]
        nameUTF = __mon_name_format(data['name'])
        buf += f'<a href="{path}dex/{mon}"><img id="dex-icon" src="{cache.iconURLs[mon]}"><span id="dex-name">{nameUTF}</span>'
        buf += '<div class="dex-type"><h6 id="type-title">Type</h6><br>'
        for type in data['types']:
            buf += f'<img src="{__type_img(type)}">'
        abilityNames = []
        for a in data['abilities']:
            abilityNames.append(cache.abilityMod[a]['name'])
        buf += f'</div><span id="dex-abilities"><h6>Abilities</h6><br>{' / '.join(abilityNames)}</span>'
        for stat in ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']:
            buf += f'<div class="dex-bst"><h6>{stat}</h6><br>{data['bst'][stat.lower()]}</div>'
        buf += f'<h3 id="dex-tier">{cache.tiersMod[mon]}</h3></a>'
    buf += '</div>'
    return buf

def __comment_tag(n):
    return f'<!-- {n} -->'

def __insert_header(html):
    html = html.replace(__comment_tag('SITE_HEADER'), __header_data)
    return html

def __insert_title(html):
    html = html.replace('SITE_TITLE', site_title)
    return html

def __insert_dex_evo(mon):
    return f'<img id="evo-icon" src="{cache.iconURLs[mon]}"> <span id="evo-name">{__mon_name_format(cache.dexMod[mon]['name'])}</span>'

def __type_img(t):
    return f'https://play.pokemonshowdown.com/sprites/types/{t}.png'

def __category_img(c):
    return f'https://play.pokemonshowdown.com/sprites/categories/{c}.png'

def __mon_name_format(name):
    return name.encode().decode('unicode-escape')

def __save(data, n, path=''):
    if not os.path.isdir('_site'):
        os.mkdir('_site')
    html = open(f'_site/{path}/{n}', 'w', encoding='utf-8')
    html.write(data)
    html.close()
