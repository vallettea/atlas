import datetime

from atlas.base import Atlas, Vertex, Edge, get_vertex

# from atlas.properties import Text, Decimal


atlas = Atlas("graph", "localhost", batchmode = False)

# # sending gremlin messages:
# atlas.execute("g.makeType().name('vid').dataType(String.class).unique(Direction.OUT).unique(Direction.IN).indexed(Vertex.class).indexed(Edge.class).makePropertyKey()")
# atlas.execute("g.addVertex(null,[vid:'stephen'])")

# atlas.execute("g.V('vid', 'stephen')")


# creating a vertice with properties
v1 = Vertex(atlas, properties = {"name_as_string" : "toto",
								 "age_as_integer" : 2, 
							     "registered_as_datetime" : datetime.datetime.now(),
							     "registered_date_as_date" : datetime.datetime.now().date(),
							     "registered_time_as_time" : datetime.datetime.now().time(),
							     "registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
							     "uuid_as_uuid" : None,
							     "male_as_boolean" : True,
							     "income_as_float" : 39009888.3222,
							     "rate_as_decimal" : 3.2
							     })
v1.save()

# querying a vertex and fill the object
v2 = get_vertex(atlas, "name_as_string", "toto")

v3 = Vertex(atlas, properties = {"name_as_string" : "tata",
								 "age_as_integer" : 3, 
							     "registered_as_datetime" : datetime.datetime.now(),
							     "registered_date_as_date" : datetime.datetime.now().date(),
							     "registered_time_as_time" : datetime.datetime.now().time(),
							     "registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
							     "uuid_as_uuid" : None,
							     "male_as_boolean" : False,
							     "income_as_float" : 39099888.3222,
							     "rate_as_decimal" : 4.8
							     })
v3.save()

e = Edge(atlas, v1, v3, "likes", properties = {"how_much_as_integer" : 8})
e.save()