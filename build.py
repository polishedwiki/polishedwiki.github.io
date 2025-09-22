from py import cache

print('===== SITE BUILDER =====')
print('Caching data files:')
cache.download()
update = cache.compare()
print('-----')
if update:
    print('Building site data:')
