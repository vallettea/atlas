import datetime,  logging

from atlas.base import Atlas, Vertex, Edge, get_vertex

logger = logging.getLogger('root')
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
handler = logging.FileHandler("/Users/vallette/Desktop/log_%s.log" % "test_atlas")
handler.setFormatter(formatter)
logger.addHandler(handler)

# from atlas.properties import Text, Decimal


atlas = Atlas("graph", "localhost", batchmode = False)

# # sending gremlin messages:
# atlas.execute("g.makeType().name('vid').dataType(String.class).unique(Direction.OUT).unique(Direction.IN).indexed(Vertex.class).indexed(Edge.class).makePropertyKey()")
# atlas.execute("g.addVertex(null,[vid:'stephen'])")

# atlas.execute("g.V('vid', 'stephen')")


# # creating a vertice with properties
# v1 = Vertex(atlas, properties = {"name_as_string" : "toto",
# 				"age_as_integer" : 2,
# 				"registered_as_datetime" : datetime.datetime.now(),
# 				"registered_date_as_date" : datetime.datetime.now().date(),
# 				"registered_time_as_time" : datetime.datetime.now().time(),
# 				"registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
# 				"uuid_as_uuid" : None,
# 				"male_as_boolean" : True,
# 				"income_as_float" : 39009888.3222,
# 				"rate_as_decimal" : 3.2
# 				})
# v1.save()

# # querying a vertex and fill the object
# v2 = get_vertex(atlas, "name_as_string", "toto")

# v3 = Vertex(atlas, properties = {"name_as_string" : "tata",
# 				"age_as_integer" : 3,
# 				"registered_as_datetime" : datetime.datetime.now(),
# 				"registered_date_as_date" : datetime.datetime.now().date(),
# 				"registered_time_as_time" : datetime.datetime.now().time(),
# 				"registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
# 				"uuid_as_uuid" : None,
# 				"male_as_boolean" : False,
# 				"income_as_float" : 39099888.3222,
# 				"rate_as_decimal" : 4.8
# 				})
# v3.save()

# # making an edge
# e = Edge(atlas, v1, v3, "likes", properties = {"how_much_as_integer" : 8})
# e.save()

# v4 = Vertex(atlas, properties = {"name_as_string" : "titi",
# 				"age_as_integer" : 9,
# 				"registered_as_datetime" : datetime.datetime.now(),
# 				"registered_date_as_date" : datetime.datetime.now().date(),
# 				"registered_time_as_time" : datetime.datetime.now().time(),
# 				"registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
# 				"uuid_as_uuid" : None,
# 				"male_as_boolean" : True,
# 				"income_as_float" : 39099888.3222,
# 				"rate_as_decimal" : 3.8
# 				})
# v4.save()
# e = Edge(atlas, v1, v4, "likes", properties = {"how_much_as_integer" : 2})
# e.save()
# # getting all outgoing vertices
# outs = v1.outV("likes")
# ins = v4.inV()


# test batch mode
import timeit
def add_nodes(n, handler):
	for i in range(n):
		v = Vertex(handler, properties = {
				# "name_as_string" : str(i),
				# "age_as_integer" : 9,
				# "registered_as_datetime" : datetime.datetime.now(),
				# "registered_date_as_date" : datetime.datetime.now().date(),
				# "registered_time_as_time" : datetime.datetime.now().time(),
				# "registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
				# "uuid_as_uuid" : None,
				# "male_as_boolean" : True,
				# "income_as_float" : 39099888.3222,
				# "rate_as_decimal" : 3.8
				})
		v.save(str(i))
# adding 500 nodes in normal way
from timeit import Timer
t = Timer(lambda: add_nodes(5000, atlas))
print t.timeit(number=1)


