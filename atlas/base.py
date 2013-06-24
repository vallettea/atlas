import logging
from rexpro import RexProConnection
from atlas import properties as atlas_prop

logger = logging.getLogger("atlas")

############### VERTEX ##############

class Vertex(object):
    """The class representing a node in the graph database.

        Vertex(handler, label=None, properties={})
        - handler is an atlas instance
        - label is not compulsory
        - properties is a dictionnary of the attributes

        example:
            v = Vertex(atlas, label="user", properties = {"name_as_string" : "toto",
                                                                                "age_as_integer" : 2,
                                                                                "registered_as_datetime" : datetime.datetime.now(),
                                                                                "male_as_boolean" : True,
                                                                                "income_as_float" : 39009888.3222,
                                                                                "rate_as_decimal" : 3.2
                                                                                })
    """

    def __init__(self, handler, label=None, properties={}):
        self.handler = handler
        self.label = label
        if label:
            properties.update({"label_as_string":  label})
        self.properties = make_prop(properties)
        if len(properties.keys()) > 0:
            prop_string = ", [" + ", ".join([k + ":" + k for k in self.properties.keys()]) + "]"
        else:
            prop_string = ""
        self.save_query = "g.addVertex(null %s)" % prop_string
        self._id = None

    def __repr__(self):
        return "atlas.Vertex %s: %s" % (str(self._id), str(self.label))

    def save(self):
        """Saves the vertex in the database"""
        params = {k : v.to_database() for k,v in self.properties.items()}
        content = self.handler.execute(self.save_query, params)
        self._id = content["_id"]
        return self

    def execute(self, script, params, as_object = False):
        """Makes a vertex centric query from the vertex.

            if as_object = False, then the raw result is returned,
            otherwise, vertex and edge objects are returned.

            example:
            v.execute("g.v(_id).both('friend').toList()", {})

            note that "_id" is automatically added.
        """
        dbparams = {}
        for key, value in params.items():
            splited = key.rsplit('_as_', 1)
            if len(splited) == 2:
                prop_type = splited[-1]
                Prop = atlas_prop.label_type[prop_type]
                v = Prop(value)
                dbparams[key] = v.to_database()
            else:
                dbparams[key] = value

        dbparams.update({"_id":  self._id})
        contents = self.handler.execute(script, dbparams)
        if not as_object:
            return contents
        else:
            to_return = []
            for content in contents:
                element = self.handler.mk_object_from_result(content)
                to_return += [element]
            return to_return

    def outV(self, label=""):
        """returns a list of vertex objects pointed at by v, linked by an edge having label"""
        if label != "":
            label = "'" + label + "'"
        contents = self.handler.execute("v = g.v(%s)\n v.out(%s)" % (self._id, label))
        vertices = []
        for content in contents:
            vertex = self.handler.mk_object_from_result(content)
            vertices += [vertex]
        return vertices

    def inV(self, label=""):
        """returns a list of vertex objects pointing to v, linked by an edge having label"""
        if label != "":
            label = "'" + label + "'"
        contents = self.handler.execute("v = g.v(%s)\n v.in(%s)" % (self._id, label))
        vertices = []
        for content in contents:
            vertex = self.handler.mk_object_from_result(content)
            vertices += [vertex]
        return vertices


############### EDGE ##############

class Edge(object):
    """The class representing an edge in the graph database.

        Edge(handler, label=None, properties={})
        - handler is an atlas instance
        - label is not compulsory
        - properties is a dictionnary of the attributes

        example:
            e = Edge(atlas, v1, v4, "likes", properties = {"how_much_as_integer" : 2})
    """
    def __init__(self, handler, v1, v2, label, properties={}):
        self.handler = handler
        self.v1 = v1
        self.v2 = v2
        self.label = label
        if label:
            properties.update({"label_as_string":  label})
        self.properties = make_prop(properties)
        if len(properties.keys()) > 0:
            prop_string = ", [" + ", ".join([k + ":" + k for k in self.properties.keys()]) + "]"
        else:
            prop_string = ""
        self.save_query = "v1 = g.v(v1_id); v2 = g.v(v2_id); g.addEdge(null, v1, v2, label %s)" % prop_string
        self._id = None

    def __repr__(self):
        return "atlas.Edge %s: %s" % (str(self._id), str(self.label))

    def save(self):
        """Saves the vertex in the database"""
        params = {'v1_id' : self.v1._id, 'v2_id' : self.v2._id, 'label' : self.label}
        params.update({k : v.to_database() for k,v in self.properties.items()})
        content = self.handler.execute(self.save_query, params)
        self._id = content["_id"]
        return self

############### ATLAS ##############

class Atlas(object):
    """Atlas is what holds the link to the titan graph database."""

    def __init__(self, graph_name, hostname, username=None, password=None, nb_commit=1000):
        self.graph_name = graph_name
        self.username = username
        self.password = password
        self.conn = RexProConnection(hostname, 8184, graph_name)
        self.nb_commit = nb_commit
        self.nb_execute = 0

    def execute(self, query, params={}):
        """Executes a gremlin command on the database with the given params."""
        try:
            content = self.conn.execute(query, params, isolate=False, transaction=False)
            self.nb_execute += 1
            if self.nb_execute == self.nb_commit:
                self.conn.execute("g.commit()", {}, isolate = False)
                self.nb_execute = 0
            return content
        except:
            logger.info("========================================================================")
            logger.info(query)
            logger.info(params)
            logger.info("========================================================================")


    def get_vertex_by_id(self, vid):
        """Given a _id, returns a vertex object"""
        contents = self.execute("g.v(id)", {"id":  vid})
        if len(contents) == 0:
            logger.info("No vertex found.")
        elif len(contents) > 1:
            logger.info("More than one vertex found.")
            content = contents
        else:
            content = contents
        vertex = self.mk_object_from_result(content)
        return vertex


    def get_vertex(self, key, value):
        """Vertex lookup: g.V(key, value)"""
        if isinstance(value, basestring):
            contents = self.execute("g.V('%s', '%s')" % (key, value))
        else:
            contents = self.execute("g.V('%s', %s)" % (key, str(value)))
        if len(contents) == 0:
            logger.info("No vertex found.")
        elif len(contents) > 1:
            logger.info("More than one vertex found.")
            content = contents[0]
        else:
            content = contents[0]
        vertex = self.mk_object_from_result(content)
        return vertex


    def get_edge(self, key, value):
        """Edge lookup: g.E(key, value)"""
        if isinstance(value, basestring):
            contents = self.execute("g.E('%s', '%s')" % (key, value))
        else:
            contents = self.execute("g.E('%s', %s)" % (key, str(value)))
        if len(contents) == 0:
            logger.info("No edge found.")
        elif len(contents) > 1:
            logger.info("More than one edge found.")
            content = contents[0]
        else:
            content = contents[0]
        edge = self.mk_object_from_result(content)
        return edge

    def mk_object_from_result(self, content):
        """makes a vertex or en edge from the raw result dictionnary"""
        if content["_properties"].has_key("label_as_string"):
            label = content["_properties"].pop("label_as_string")
        else:
            label = None

        if content["_type"] == "vertex":
            vertex = Vertex(self, label = label, properties = content["_properties"])
            vertex._id = content["_id"]
            return vertex
        elif content["_type"] == "edge":
            v1 = self.get_vertex_by_id(content["_outV"])
            v2 = self.get_vertex_by_id(content["_inV"])
            edge = Edge(self, v1, v2, label = label, properties = content["_properties"])
            edge._id = content["_id"]
            return edge


# helpers

def make_prop(properties):
    """makes dictionnary of atlas properties from given input dictionnary.Each key must contain the  _as_ keyword."""
    typed_properties = {}
    for key, value in properties.items():
        prop_type = key.rsplit('_as_', 1)
        Prop = atlas_prop.label_type[prop_type]
        v = Prop(value)
        typed_properties[key] = v
    return typed_properties



