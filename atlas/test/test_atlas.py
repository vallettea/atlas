import unittest
import datetime
import logging

from atlas.base import Atlas, Vertex, Edge

logging.disable(logging.CRITICAL)

class TestAtlas(unittest.TestCase):

    def setUp(self):
        self.atlas = Atlas("graph", "localhost")

    def test_execute(self):
        self.atlas.execute("g.makeType().name('name_as_string').dataType(String.class).unique(Direction.OUT).unique(Direction.IN).indexed(Vertex.class).indexed(Edge.class).makePropertyKey()")
        self.atlas.execute("g.addVertex(null,[name:'rand'])")
        result = self.atlas.execute("g.V('name', 'rand')")[0]

        self.assertEqual(result["_properties"]["name"], "rand")

    def test_save_vertex(self):
        v1 = Vertex(self.atlas, label="user", properties = {"name_as_string" : "toto",
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
        v2 = self.atlas.get_vertex("name_as_string", "toto")

        self.assertEqual(v1._id, v2._id)
        self.assertEqual(v1.label, v2.label)
        self.assertEqual(v1.properties["age_as_integer"].to_python(), v2.properties["age_as_integer"].to_python())

    def test_save_edge(self):
        v1 = Vertex(self.atlas, properties = {"name_as_string" : "tata"}).save()
        v2 = Vertex(self.atlas, properties = {"name_as_string" : "toto"}).save()
        e1 = Edge(self.atlas, v1, v2, label = "calls", properties = {"name_as_string" : "bidule"})
        e1.save()

        e2 = self.atlas.get_edge("name_as_string", "bidule")

        self.assertEqual(e1._id, e2._id)
        self.assertEqual(e1.label, e2.label)
        self.assertEqual(e1.v1._id, e2.v1._id)
        self.assertEqual(e1.v2._id, e2.v2._id)

    def test_outv_inv(self):
        v1 = Vertex(self.atlas, properties = {"name_as_string" : "1"}).save()
        v2 = Vertex(self.atlas, properties = {"name_as_string" : "2"}).save()
        v3 = Vertex(self.atlas, properties = {"name_as_string" : "3"}).save()
        e1 = Edge(self.atlas, v2, v1, label = "calls", properties = {"name_as_string" : "bidule"}).save()
        e2 = Edge(self.atlas, v3, v1, label = "calls", properties = {"name_as_string" : "machin"}).save()
        e3 = Edge(self.atlas, v3, v1, label = "likes", properties = {}).save()

        self.assertEqual(len(v3.outV()), 2)
        self.assertEqual(len(v3.outV("calls")), 1)

        self.assertEqual(len(v1.inV()), 3)
        self.assertEqual(len(v1.inV("likes")), 1)

    def test_vertex_function(self):
        alex = Vertex(self.atlas, properties = {"name_as_string" : "alex", "age_as_integer" : 28}).save()
        rand = Vertex(self.atlas, properties = {"name_as_string" : "rand", "age_as_integer" : 28}).save()
        mael = Vertex(self.atlas, properties = {"name_as_string" : "mael", "age_as_integer" : 31}).save()


        e1 = Edge(self.atlas, alex, rand, "friend", {}).save()
        e2 = Edge(self.atlas, alex, mael, "friend", {}).save()
        friends_of_friends = """me = g.v(_id)
                                             friends = me.both('friend').toList()
                                             me.both('friend').both('friend').dedup().except([me]).except(friends)"""

        result = rand.execute(friends_of_friends,  {})
        self.assertEqual(result[0]["_id"], mael._id)
        result = rand.execute(friends_of_friends,  {}, as_object = True)
        self.assertEqual(result[0].properties["age_as_integer"].to_python(), 31)



if __name__ == '__main__':
    unittest.main()





# print "test performance"
# import timeit
# from random import choice
# def add_graph(nn, ne, handler):
#   nodes = []
#   for i in range(nn):
#       v = Vertex(handler, properties = {
#               "name_as_string" : str(i),
#               "age_as_integer" : 9,
#               "registered_as_datetime" : datetime.datetime.now(),
#               "registered_date_as_date" : datetime.datetime.now().date(),
#               "registered_time_as_time" : datetime.datetime.now().time(),
#               "registered_since_as_timedelta" : datetime.datetime(2013, 5, 21, 13, 52, 41, 176589) - datetime.datetime.now(),
#               "uuid_as_uuid" : None,
#               "male_as_boolean" : True,
#               "income_as_float" : 39099888.3222,
#               "rate_as_decimal" : 3.8
#               })
#       v.save()
#       nodes += [v]
#   for i in range(ne):
#       v1 = choice(nodes)
#       v2 = choice(nodes)
#       while v2 == v1:
#           v2 = choice(nodes)
#       e = Edge(handler, v1, v2, "likes", properties = {"how_much_as_integer" : 2})
#       e.save()
# print "adding 5000 nodes and 5000 edges"
# from timeit import Timer
# t = Timer(lambda: add_graph(5000, 5000, atlas))
# print t.timeit(number=1)





# alex = Vertex(atlas, properties = {"name_as_string" : "alex", "age_as_integer" : 28}).save()
# rand = Vertex(atlas, properties = {"name_as_string" : "rand", "age_as_integer" : 28}).save()
# mael = Vertex(atlas, properties = {"name_as_string" : "mael", "age_as_integer" : 31}).save()


# e1 = Edge(atlas, alex, rand, "friend", {}).save()
# e2 = Edge(atlas, alex, mael, "friend", {}).save()
# friends_of_friends = """me = g.v(_id)
# friends = me.both('friend').toList()
# me.both('friend').both('friend').dedup().except([me]).except(friends)
# """

# print rand.execute(friends_of_friends,  {})
