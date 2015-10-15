# Summary
Tools to create a geolocation API similar to [that offered by Google](https://developers.google.com/maps/articles/geolocation)

# High Level Logic

1. Takes list of place names from [GeoNames](http://download.geonames.org/export/dump/)  
2. Parses and imports into MySQL DB  
3. Sets up API with Flask  
4. Responds to queries of text location strings with coordinates and country name  

# DB Schema

There are two tables `places` and `admin1`

1. `places` lists all place names and maps to coordinates and other info

| `name` | `clean_name` | `lat` | `lon` | `country` | `population` | `elevation` | `admin_name` | `feature` |
| ----------|-------------|-----|----|---|-------|--------|--------|-------- |
| Suhūl az̧ Z̧afrah | suhūl az̧ z̧afrah | 22.75 | 53.1667 | AE | 0 | 119 | 00 | 00 | PLN |

2. `admin1` lists all first level administrative divisions e.g. in the US, these are states such as New York or Arizona

| `code`| `name` | `ascii_name` | `pop` | `country` | `admin_code` |
|------|------------|-------------|-------|---------|---------|------ |
| 0 | AD.06 | Sant Julià de Loria | Sant Julia de Loria | 3039162 | AD |

# API Call

Set up API with 

`python app.py`

Which serves to http://127.0.0.1:5000/  

Query DB for `location` with http://127.0.0.1:5000/loc=\<location\>  

# Gotchas

The following values sometimes appear in the admin level 1 column

00/0 = the entire country
Values that do not appear in `admin1` table are not regular part of country
e.g. the Tunb islands of UAE: feature code is ISL and admin code is 11

# Dependencies

#Dependencies
1. [Flask](http://flask.pocoo.org/)  
2. [MySQLdb](https://pypi.python.org/pypi/MySQL-python/1.2.4)
3. [Requests](http://docs.python-requests.org/en/latest/)

# Todo

1. Add in clues e.g. likely country, region, timezone or language  
2. Add in fuzzy matching e.g. Al Raqqah/Al Raqah  
3. Automatically query Google API and update DB  
4. Add in admin level 2 as well as level 1  