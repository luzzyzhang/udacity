# -*- coding: utf-8 -*-
ta_data = [('Peter', 'USA', 'CS262'),
           ('Andy', 'USA', 'CS212'),
           ('Sarah', 'England', 'CS101'),
           ('Gundega', 'Latvia', 'CS373'),
           ('Job', 'USA', 'cs387'),
           ('Sean', 'USA', 'CS253')]


ta_facts = [name + ' lives in ' + country + ' teach for ' + course for name, country, course in ta_data]

for row in ta_facts:
    print row
