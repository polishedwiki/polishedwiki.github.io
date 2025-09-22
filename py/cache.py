import urllib.request, os, shutil, filecmp

# config vars
repo = 'CCC200/DH2'
mod = 'polishedcrystal'

__data_files = ['abilities.ts', 'items.ts', 'moves.ts', 'pokedex.ts', 'scripts.ts']

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
