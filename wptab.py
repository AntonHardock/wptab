## branch flexible-table-search
## allow search by row or header
import bs4 as bs
import urllib.request
import pandas as pd

def get_tab(source, t_vals, search="head", t_id=0, wikitable_class='wikitable sortable'):
    '''Find a specific table from a wikipedia url and return it as a list of lists.
    Source: either  be url or instance of bs.BeautifulSoup() (remove when tests are done)
    Each list represents a table row, including the header. RENEW THIS PART
    Default is looking through header
    If column or row is targeted, default col/row Id is 0. 
    '''
    target = list()

    if not isinstance(source, bs.BeautifulSoup): 
        source = urllib.request.urlopen(source).read()
        source = bs.BeautifulSoup(source, 'lxml')

    for table in source.find_all('table', class_= wikitable_class):
        
        ## str.strip() required for parsing since additional whitespace + newline chars might be hidden in the html source 
        if search == "head":
            ## first row is skipped since it usually contains table header tags (th) and no table data tags (td)
            x = (th.text.strip() for th in table.find_all('th'))
        elif search == "row":
            t_id += 1 #add one since the header will be the first row found
            x = (d.text.strip() for d in table.find_all('tr')[t_id].find_all('td'))
        elif search == "column":
            x = (row.find_all('td')[t_id].text.strip() for row in table.find_all('tr')[1:])
        else:
            raise ValueError("Parameter 'search' must be 'head', 'row', or 'column'")

        ## if target head/row/column contains all of the target values, extract table
        if t_vals.issubset(set(x)):
            target = table
            break 

    ## if target is an empty list, raise exception
    if not target: raise ValueError("No table found. Try other target values or another wikitable class")

    ## parse the table data into a list of lists
    rows = list()
    for row in target.find_all('tr'):
        row = [d.text.strip() for d in row.find_all('td')]
        rows.append(row)

    # remove first row if it is an empty list
    if not rows[0]: del rows[0] 

    # get the header and insert as first row
    header = [th.text.strip() for th in target.find_all('th')]    
    rows.insert(0, header)
    
    return rows
