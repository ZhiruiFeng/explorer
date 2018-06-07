Through preprocessing.py

"USA-road-d.NY.gr", "USA-road-t.BAY.gr" are directed graphs, but the get_weight
of i->j is equal to j->i, which works like the undirected graphs.

"rome99.road" is a 'real' directed graphs.
SO it is suitable for doing the DIG-FastMap test.
