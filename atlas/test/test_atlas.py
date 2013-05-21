import datetime

from atlas.base import Atlas, Vertex
import atlas.properties as prop
# from atlas.properties import Text, Decimal


atlas = Atlas("graph", "localhost", batchmode = False)

# # sending gremlin messages:
# atlas.execute("g.makeType().name('vid').dataType(String.class).unique(Direction.OUT).unique(Direction.IN).indexed(Vertex.class).indexed(Edge.class).makePropertyKey()")
# atlas.execute("g.addVertex(null,[vid:'stephen'])")

# atlas.execute("g.V('vid', 'stephen')")


# creating a vertice with properties
v1 = Vertex(atlas, properties = {"name" : prop.String("toto"),
								 "age" : prop.Integer(2), 
							     "registered" : prop.DateTime(datetime.datetime.now()),
							     "registered_date" : prop.Date(datetime.datetime.now().date()),
							     "registered_time" : prop.Time(datetime.datetime.now().time()),
							     "registered_since" : prop.TimeDelta(datetime.datetime(2013, 5, 21, 13, 52, 41, 176589)-datetime.datetime.now()),
							     "uuid" : prop.UUID(),
							     "male" : prop.Boolean(True),
							     "income" : prop.Float(39009888.3222),
							     "rate" : prop.Decimal(3.2)
							     })