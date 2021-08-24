from repo.search import SearchManager

manager =SearchManager()
wave = manager.search_waves([1],[1,2])
print(wave)