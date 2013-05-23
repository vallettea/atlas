import datetime,  logging

from atlas.base import Atlas, Vertex, Edge, get_vertex

logger = logging.getLogger('atlas')
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
handler = logging.FileHandler("/Users/vallette/Desktop/log_%s.log" % "test_atlas")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Creating atlas")

atlas = Atlas("graph", "localhost", batchmode = False)

logger.info("sending gremlin messages:")
atlas.execute("g.makeType().name('vid').dataType(String.class).unique(Direction.OUT).unique(Direction.IN).indexed(Vertex.class).indexed(Edge.class).makePropertyKey()")
atlas.execute("g.addVertex(null,[vid:'stephen'])")

atlas.execute("g.V('vid', 'stephen')")


logger.info("creating a vertice with properties")
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

logger.info("querying a vertex and fill the object")
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

logger.info("making an edge")
e = Edge(atlas, v1, v3, "likes", properties = {"how_much_as_integer" : 8})
e.save()

v4 = Vertex(atlas, properties = {"name_as_string" : "titi",
				"age_as_integer" : 9,
				"registered_as_datetime" : datetime.datetime.now(),
				"registered_date_as_date" : datetime.datetime.now().date(),
				"registered_time_as_time" : datetime.datetime.now().time(),
				"registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
				"uuid_as_uuid" : None,
				"male_as_boolean" : True,
				"income_as_float" : 39099888.3222,
				"rate_as_decimal" : 3.8
				})
v4.save()
e = Edge(atlas, v1, v4, "likes", properties = {"how_much_as_integer" : 2})
e.save()
logger.info("getting all outgoing vertices")
outs = v1.outV("likes")
ins = v4.inV()


logger.info("test performance")
import timeit
from random import choice
def add_graph(nn, ne, handler):
	nodes = []
	for i in range(nn):
		v = Vertex(handler, properties = {
				"name_as_string" : str(i),
				"age_as_integer" : 9,
				"registered_as_datetime" : datetime.datetime.now(),
				"registered_date_as_date" : datetime.datetime.now().date(),
				"registered_time_as_time" : datetime.datetime.now().time(),
				"registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
				"uuid_as_uuid" : None,
				"male_as_boolean" : True,
				"income_as_float" : 39099888.3222,
				"rate_as_decimal" : 3.8
				})
		v.save()
		nodes += [v]
	for i in range(ne):
		v1 = choice(nodes)
		v2 = choice(nodes)
		while v2 == v1:
			v2 = choice(nodes)
		e = Edge(handler, v1, v2, "likes", properties = {"how_much_as_integer" : 2})
		e.save()
logger.info("adding 5000 nodes and 5000 edges")
from timeit import Timer
t = Timer(lambda: add_graph(5000, 5000, atlas))
print t.timeit(number=1)



logger.info("adding function to a vertex:")

alex = Vertex(atlas, properties = {"name_as_string" : "alex", "age_as_integer" : 28}).save()
rand = Vertex(atlas, properties = {"name_as_string" : "rand", "age_as_integer" : 28}).save()
mael = Vertex(atlas, properties = {"name_as_string" : "mael", "age_as_integer" : 31}).save()


e1 = Edge(atlas, alex, rand, "friend", {}).save()
e2 = Edge(atlas, alex, mael, "friend", {}).save()
friends_of_friends = """me = g.v(_id)
friends = me.both('friend').toList()
me.both('friend').both('friend').dedup().except([me]).except(friends)
"""

print rand.execute(friends_of_friends,  {})
