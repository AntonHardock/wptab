#########################################
## Test different constellations
import bs4 as bs
import urllib.request
import pandas as pd
import importlib

import wptab
importlib.reload(wptab)
from wptab import get_tab

wiki_url1 = "https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains#Country_code_top-level_domains"
wiki_url2 = "https://de.wikipedia.org/wiki/COVID-19-Pandemie"  #see right floating table "Maßnahmen in China"

## head
hvals = {"Name[6]", "Entity", "Explanation", "Notes", "Registry[6]"}
target = get_tab(wiki_url1, hvals, search="head")
pd.DataFrame(target[1:], columns=target[0]).head()

## col
cvals = {"Bengali", "Bulgarian", "Chinese"}
target = get_tab(wiki_url1, cvals, search="column", t_id=3)
pd.DataFrame(target[1:], columns=target[0]).head(7)

## row
rvals = {".actor", "actors"}
target = get_tab(wiki_url1, rvals, search="row", t_id=4)
pd.DataFrame(target[1:], columns=target[0]).head()
