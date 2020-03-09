## branch flexible-table-search
import bs4 as bs
import urllib.request

def get_tab(url, col_id, col_vals, wikitable_class='wikitable sortable'):
    '''Find a specific table from a wikipedia url and return it as a list of lists.
    Each list represents a table row, including the header. To target a specific table,
    two hints are required: A column id (col_id, zero based) and a set of one or more values that column contains (col_vals)
    The function parses all wikipedia tables of a given table class from top to bottom (default: wikitable sortable).
    For each table, only the specified column is parsed and searched for the target values.
    The search ends with the first match.
    '''
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    target = list()

    for table in soup.find_all('table', class_= wikitable_class):
        
        ## first row is skipped since it usually contains table header tags (th) and no table data tags (td)
        ## str.strip() required since additional whitespace + newline chars might be hidden in the html source
        column = (row.find_all('td')[col_id].text.strip() for row in table.find_all('tr')[1:]) 

        ## if firstrow contains all of the target values, extract table
        if col_vals.issubset(set(column)):
            target = table
            break 

    ## if target is an empty list, raise exception
    if not target: raise ValueError("Specified table not found. Maybe try another wikitable class?")

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