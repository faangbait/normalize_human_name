import re
from typing import List

def normalize_parts(name: str) -> List[str]:
    """
    Given a name in any format (firstlast, lastfirst, honorifics, etc), return the name as an ordered list of component parts.
    """
    roman_first = ""
    roman_last = ""
    
    # 1. Are we in Last, First?
    # name_regex = r"^([a-zA-Z\u00C0-\u00FF\'\-]+)[,]([a-zA-Z\u00C0-\u00FF ]+[a-zA-Z\u00C0-\u00FF]*)[.]?$"
    name_regex = r"^([a-zA-Z\u00C0-\u05F4\'\-\.\ ]+)[,][ ]?((?!.*([M|J|S]r\.?|III|IV|V))[a-zA-Z\u00C0-\u05F4\'\-\.\ ]+)$"

    # Check (1) for matches
    result = re.match(name_regex, name)
    if result:
        res = []
        for val in result.groups():
            if val != None:
                res.append(val)
        res.reverse()
        return res

    # 2. Match Last, First Suffix
    name_regex = r"^([a-zA-Z\u00C0-\u05F4\'\-\.\ ]+)[,][ ]?([a-zA-Z\u00C0-\u05F4\'\-\.\ ]+) ([M|J|S]r\.?|III|IV|V)$"
    
    # Check (2) for matches
    result = re.match(name_regex, name)
    if result:
        res = []
        for val in result.groups():
            if val != None:
                res.append(val)
        return res[1], res[0], res[2]
    
    # 3. Match (First Middle Last)
    name_regex = r"^((?!.*[@\_\d])[A-Za-z\u00C0-\u05F4\'\-\.][\.A-Za-z\u00C0-\u05F4\'\-\.]+)[ ]?([A-Za-z\u00C0-\u05F4\'\-\.][A-Za-z\u00C0-\u05F4\'\-\.]*)?[ ]?([A-Za-z\u00C0-\u05F4\'\-\.][A-Za-z\u00C0-\u05F4\'\-\.]+)*[,]?[ ]?([M|J|S]r\.?|III|IV|V)?$"
    
    # Check (3) for matches
    result = re.match(name_regex, name)
    
    if result:
        res = []
        for val in result.groups():
            if val != None:
                res.append(val)
        return res

    # 4. Elon named this player
    name_regex = r"^(.*)$"
    
    # Check (4) for matches
    result = re.match(name_regex, name)
    
    if result:
        res = []
        for val in result.groups():
            if val != None:
                res.append(val)
        return res
    return []

def normalize(name: str) -> str:
    return " ".join(normalize_parts(name))

def test_name_parser():
    # Test helper function
    assert "Carlito Magnusson" == normalize("Carlito Magnusson")
    assert "Boško Abramović" == normalize("Abramović, Boško")

    # First Last
    assert "Jackmerius Tacktheritrix" == " ".join(normalize_parts("Jackmerius Tacktheritrix"))
    assert "L'Carpetron Dookmarriot" == " ".join(normalize_parts("L'Carpetron Dookmarriot"))
    
    # Last, First
    assert "Jacob Aagaard" == " ".join(normalize_parts("Aagaard, Jacob"))
    assert "Ibrahim Moizoos" == " ".join(normalize_parts("Moizoos, Ibrahim"))
    assert "Hingle McCringleberry" == " ".join(normalize_parts("McCringleberry, Hingle"))
    assert "J'Dinkalage Morgoone" == " ".join(normalize_parts("Morgoone, J'Dinkalage"))
    assert "Swirvithan L'Goodling-Splatt" == " ".join(normalize_parts("L'Goodling-Splatt, Swirvithan"))
    
    # Non-Latin Characters
    assert "Ralf Åkesson" == " ".join(normalize_parts("Ralf Åkesson"))
    assert "X-Wing @Aliciousness" == " ".join(normalize_parts("X-Wing @Aliciousness"))
    
    # F. Last
    assert "B. Adhiban" == " ".join(normalize_parts("B. Adhiban"))
    
    # Last Last, First Middle
    assert "Carlos Daniel Albornoz Cabrera" == " ".join(normalize_parts("Albornoz Cabrera, Carlos Daniel"))

    # Single Name
    assert "Ardiansyah" == " ".join(normalize_parts("Ardiansyah"))
    
    # Jr, Sr, III
    assert "Rogelio Antonio Jr." == " ".join(normalize_parts("Antonio, Rogelio Jr."))
    assert "D'squarius Green Jr." == " ".join(normalize_parts("D'squarius Green, Jr."))
    assert "D'Jasper Probincrux III" == " ".join(normalize_parts("Probincrux, D'Jasper III"))
    assert "T.J. A.J. R.J. Backslashinfourth V" == " ".join(normalize_parts("Backslashinfourth, T.J. A.J. R.J. V"))

    # Apostrophes
    assert "D'Marcus Williums" == " ".join(normalize_parts("D'Marcus Williums"))
    assert "T'variusness King" == " ".join(normalize_parts("King, T'variusness"))

    # Initials
    assert "T.J. Juckson" == " ".join(normalize_parts("T.J. Juckson"))
    assert "D'isiah T. Billings-Clyde" == " ".join(normalize_parts("D'isiah T. Billings-Clyde"))
    assert "Shakiraquan T.G.I.F Carter" == " ".join(normalize_parts("Carter, Shakiraquan T.G.I.F"))

    # Hyphenated
    assert "Tyroil Smoochie-Wallace" == " ".join(normalize_parts("Tyroil Smoochie-Wallace"))
    assert "Javaris Jamar Javarison-Lamar" == " ".join(normalize_parts("Javarison-Lamar, Javaris Jamar"))
    assert "Davoin Shower-Handel" == " ".join(normalize_parts("Davoin Shower-Handel"))
    
    # First Middle Last
    assert "Leoz Maxwell Jilliumz" == " ".join(normalize_parts("Leoz Maxwell Jilliumz"))
    assert "Xmus Jackson Flaxon Waxon" == " ".join(normalize_parts("Xmus Jackson Flaxon Waxon"))

    # TODO: Name displayed with Chinese characters should render Last First?
    assert "Wei Yi" == " ".join(normalize_parts("Wei Yi"))
