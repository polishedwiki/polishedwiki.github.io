import os, shutil

# config vars
site_title = 'Polished Wiki'

__header_data = False

def build_header():
    f = open('pages/site-header.html')
    _head = f.read()
    f.close()
    return _head

def build_index(dex, ability, tiers, icons):
    print('- index')
    f = open('pages/index.html')
    html = f.read()
    f.close()
    # parse mon list
    buf = '<div class="dex-head"><h2 id="title">Pokémon</h2><h2 id="tier">Tier</h2></div>'
    buf += '<div class="dex-list" align="center">'
    for mon, data in dex.items():
        nameUTF = data['name'].encode().decode('unicode-escape')
        buf += f'<a href="dex/{mon}"><img id="dex-icon" src="{icons[mon]}"><span id="dex-name">{nameUTF}</span>'
        buf += '<div class="dex-type"><h6 id="type-title">Type</h6><br>'
        for type in data['types']:
            buf += f'<img src="https://play.pokemonshowdown.com/sprites/types/{type}.png">'
        abilityNames = []
        for a in data['abilities']:
            abilityNames.append(ability[a]['name'])
        buf += f'</div><span id="dex-abilities"><h6>Abilities</h6><br>{' / '.join(abilityNames)}</span>'
        for stat in ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe']:
            buf += f'<div class="dex-bst"><h6>{stat}</h6><br>{data['bst'][stat.lower()]}</div>'
        buf += f'<h3 id="dex-tier">{tiers[mon]}</h3></a>'
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


def __comment_tag(n):
    return f'<!-- {n} -->'

def __insert_header(html):
    html = html.replace(__comment_tag('SITE_HEADER'), __header_data)
    return html

def __insert_title(html):
    html = html.replace('SITE_TITLE', site_title)
    return html

def __save(data, n, path=''):
    if not os.path.isdir('_site'):
        os.mkdir('_site')
    html = open(f'_site/{path}/{n}', 'w', encoding='utf-8')
    html.write(data)
    html.close()
