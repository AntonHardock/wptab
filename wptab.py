import urllib.request
import bs4 as bs


def get_tab(url, t_vals, search="head", t_id=0,
            wikitable_class="wikitable sortable"):
    """Extract a specific table from a wikipedia URL and return it as a list
    of lists. Each nested list represents a table row, including the header.
    Tables of a predefined html class (default 'wikitable sortable') are
    searched from top to bottom.
    Find a specific table requires a set object of target values (t_vals).
    Those values can be looked up in each header (default),
    or in a particular row / column of each table (search='row' /
    search='column'). The latter options require a row / column id
    (t_id, default=0). For example, search="row" and t_id=2 will go
    through the third row of each table.
    """
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, "lxml")
    target = list()

    for table in soup.find_all("table", class_=wikitable_class):

        # extract data entries from header or target row / target column
        if search == "head":
            # strip() required for parsing as source code might
            # contain additional whitespace + newline chars
            x = (h.text.strip() for h in table.find_all("th"))
        elif search == "row":
            try:
                # first row excluded as it is usually empty
                # (containing th, but not td tags)
                rows = table.find_all("tr")[1:]
                x = (d.text.strip() for d in rows[t_id].find_all("td"))
            except IndexError:
                continue
        elif search == "column":
            try:
                # first row excluded as it is usually empty
                # (containing th, but not td tags)
                rows = table.find_all("tr")[1:]
                x = (d.find_all("td")[t_id].text.strip() for d in rows)
            except IndexError:
                continue
        else:
            raise ValueError("Parameter 'search' must be "
                             "'head', 'row', or 'column'")

        # if target values are subset of extracted data,
        # keep table and break loop
        if t_vals.issubset(set(x)):
            target = table
            break

    # if target remained an empty list, raise error
    if not target:
        raise ValueError("No table found. Try other target values "
                         "or another wikitable class")

    # parse the table data into a list of lists
    rows = list()
    for row in target.find_all("tr"):
        row = [d.text.strip() for d in row.find_all("td")]
        rows.append(row)

    # remove first row if it is an empty list
    if not rows[0]:
        del rows[0]

    # get the header and insert as first row
    header = [th.text.strip() for th in target.find_all("th")]
    rows.insert(0, header)

    return rows
