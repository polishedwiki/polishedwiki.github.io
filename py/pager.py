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
    for mon, data in cache.dexMod.items():
        __build_dex_page(mon)

def build_index():
    print('- index')
    f = open('pages/index.html')
    html = f.read()
    f.close()
    # parse mon list
    buf = '<div class="dex-head"><h2 id="title">Pokémon</h2><h2 id="tier">Tier</h2></div>'
    buf += '<div class="dex-list" align="center">'
    for mon, data in cache.dexMod.items():
        nameUTF = __mon_name_format(data['name'])
        buf += f'<a href="dex/{mon}"><img id="dex-icon" src="{cache.iconURLs[mon]}"><span id="dex-name">{nameUTF}</span>'
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
    buf += "</div>"
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
    html = html.replace('MON_TIER', cache.tiersMod[mon])
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
    if 'prevo' in data or 'evos' in data:
        buf = '<div class="evo-link"><h3>Evolutions</h3>'
        prevEvos = []
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
                        nextEvo = cache.dexMod[data['evos'][i]]['evos'][0]
                        buf += f' &#8594; <a href="../{nextEvo}">{__insert_dex_evo(nextEvo)}</a>'
        buf += '</div>'
    else:
        buf = ''
    html = html.replace(__comment_tag('MON_EVOLUTION'), buf)
    # overview (TODO: THIS IS PLACEHOLDER)
    html = html.replace(__comment_tag('MON_OVERVIEW'), 'No analysis is available for this species.')
    # abilities
    html = html.replace(__comment_tag('MON_ABILITY'), __build_ability_list(data['abilities'], '../../'))
    # moves
    html = html.replace(__comment_tag('MON_MOVES'), __build_move_list(data['learnset'], '../../'))
    # insert headers
    html = __insert_header(html)
    html = __insert_title(html)
    html = html.replace('SITE_INDEX', '../..')
    __save(html, 'index.html', f'dex/{mon}')

def __build_ability_list(abilities, path=''):
    buf = '<div class="ability-list" align="center">'
    for a in abilities:
        ability = cache.abilityMod[a]
        buf += f'<a href="{path}ability/{a}" {'id="ability-single"' if len(abilities) == 1 else ''}><span id="ability-name">{ability['name']}</span>{ability['desc']}</a>'
    buf += '</div>'
    return buf

def __build_move_list(moves, path=''):
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
