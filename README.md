# Summary
Tools to create a geolocation API similar to [that offered by Google](https://developers.google.com/maps/articles/geolocation)

# High Level Logic

1. Takes list of place names from [GeoNames](http://download.geonames.org/export/dump/)  
2. Parses and imports into MySQL DB  
3. Sets up API with Flask  
4. Responds to queries of text location strings with coordinates and country name  

# Dependencies

#Dependencies
1. [Flask](http://flask.pocoo.org/)  
2. [MySQLdb](https://pypi.python.org/pypi/MySQL-python/1.2.4)
3. [Requests](http://docs.python-requests.org/en/latest/)