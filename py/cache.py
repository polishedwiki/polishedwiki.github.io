import urllib.request, os, shutil, filecmp

# config vars
repo = 'CCC200/DH2'
mod = 'polishedcrystal'

__data_files = ['abilities.ts', 'formats-data.ts', 'items.ts', 'learnsets.ts', 'moves.ts', 'pokedex.ts', 'scripts.ts']
__data_files_special = ['text-abilities.ts', 'text-items.ts', 'text-moves.ts']

def download():
    if not os.path.isdir('_cache'):
        os.mkdir('_cache')
    if not os.path.isdir('_cache/.tmp'):
        os.mkdir('_cache/.tmp')
    if not os.path.isdir('_cache/.tmp/base'):
        os.mkdir('_cache/.tmp/base')
    if not os.path.isdir(f'_cache/.tmp/{mod}'):
        os.mkdir(f'_cache/.tmp/{mod}')
    for f in __data_files:
        print(f'- {f.replace('.ts', '')}')
        urllib.request.urlretrieve(__data_url(f), f'_cache/.tmp/base/{f}')
        urllib.request.urlretrieve(__data_url(f, mod), f'_cache/.tmp/{mod}/{f}')
    for f in __data_files_special: # convert to proper URL format before download
        f_url = f.replace('-', '/')
        print(f'- {f.replace('.ts', '')}')
        urllib.request.urlretrieve(__data_url(f_url), f'_cache/.tmp/base/{f}')

def compare():
    if not os.path.isdir('_cache/base') or not os.path.isdir(f'_cache/{mod}'):
        __init_copy()
        return True
    change = False
    for n in ['base', mod]:
        m_data = filecmp.cmpfiles(f'_cache/.tmp/{n}', f'_cache/{n}', __data_files)
        if len(m_data[1]) > 0:
            print(f'{n} data update: {', '.join([s.replace('.ts', '') for s in m_data[1]])}')
            for f in m_data[1]:
                shutil.copyfile(f'_cache/.tmp/{n}/{f}', f'_cache/{n}/{f}')
            change = True
    return change

def icons(dex):
    urls = {}
    counter = 0
    for name, data in dex.items():
        counter += 1
        print(f'- dex icons {counter}/{len(dex)}', end='\r')
        try:
            url = __data_url(f'sprites/icons/{name}.png', mod)
            urllib.request.urlopen(url)
        except:
            try:
                url = __smogon_icon_url(name)
                urllib.request.urlopen(url)
            except:
                url = 'SITE_INDEXassets/question.png'
        urls[name] = url
    print(f'- dex icons {counter}/{len(dex)}')
    return urls

def sprites(dex):
    urls = {}
    counter = 0
    for name, data in dex.items():
        counter += 1
        print(f'- dex sprites {counter}/{len(dex)}', end='\r')
        try:
            url = __data_url(f'sprites/front/{__showdown_mon_url_format(name, False)}.png', mod)
            urllib.request.urlopen(url)
        except:
            url = __smogon_sprite_url(name)
        urls[name] = url
    print(f'- dex sprites {counter}/{len(dex)}')
    return urls

def __showdown_mon_url_format(mon, isIcon=True):
    # specific
    if isIcon:
        if 'mrmime' in mon:
            mon = mon.replace('mrmime', 'mr-mime')
        elif 'tauros' in mon and 'combat' in mon:
            mon = mon.replace('combat', '-combat')
        elif 'tauros' in mon and 'blaze' in mon:
            mon = mon.replace('blaze', '-blaze')
        elif 'tauros' in mon and 'aqua' in mon:
            mon = mon.replace('aqua', '-aqua')
        elif mon == 'nidoranf':
            mon = 'nidoran-f'
        elif mon == 'nidoranm':
            mon = 'nidoran-m'
        elif mon == 'hooh':
            mon = 'ho-oh'
        elif mon == 'mimejr':
            mon = 'mime-jr'
        elif mon == 'porygonz':
            mon = 'porygon-z'
        elif mon == 'mrrime':
            mon = 'mr-rime'
    if mon == 'ursalunabloodmoon':
        mon = 'ursaluna-bloodmoon'
    # regional
    if 'alola' in mon:
        mon = mon.replace('alola', '-alola')
    elif 'galar' in mon:
        mon = mon.replace('galar', '-galar')
    elif 'hisui' in mon:
        mon = mon.replace('hisui', '-hisui')
    elif 'paldea' in mon:
        mon = mon.replace('paldea', '-paldea')
    return mon

def __smogon_icon_url(mon):
    mon = __showdown_mon_url_format(mon)
    return f'https://www.smogon.com/forums/media/minisprites/{mon}.png'

def __smogon_sprite_url(mon):
    mon = __showdown_mon_url_format(mon, False)
    return f'https://play.pokemonshowdown.com/sprites/gen5/{mon}.png'

def __data_url(file, mod=False):
    return f'https://raw.githubusercontent.com/{repo}/master/data/{f'mods/{mod}/{file}' if mod else file}'

def __init_copy():
    if not os.path.isdir('_cache/base'):
        os.mkdir('_cache/base')
    if not os.path.isdir(f'_cache/{mod}'):
        os.mkdir(f'_cache/{mod}')
    for f in __data_files:
        if not os.path.isfile(f'_cache/base/{f}'):
            shutil.copyfile(f'_cache/.tmp/base/{f}', f'_cache/base/{f}')
        if not os.path.isfile(f'_cache/{mod}/{f}'):
            shutil.copyfile(f'_cache/.tmp/{mod}/{f}', f'_cache/{mod}/{f}')
    for f in __data_files_special:
        if not os.path.isfile(f'_cache/base/{f}'):
            shutil.copyfile(f'_cache/.tmp/base/{f}', f'_cache/base/{f}')
