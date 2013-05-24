import logging

from rexpro import RexProConnection

from atlas import properties as atlas_prop

logger = logging.getLogger("atlas")


class Atlas(object):
    def __init__(self, graph_name, hostname, username = None, password = None, batchmode = False):
        self.graph_name = graph_name
        self.username = username
        self.password = password
        self.batchmode = batchmode
        self.conn = RexProConnection(hostname, 8184, graph_name)

        #self.conn.execute("g.makeType().name('vid').dataType(String.class).unique(Direction.OUT).unique(Direction.IN).indexed(Vertex.class).indexed(Edge.class).makePropertyKey()")

        if self.batchmode:
            self.execute("bg = new BatchGraph(g, VertexIDType.STRING, 1000) ;")

    def execute(self, query, params = {}):

        try:
            content = self.conn.execute(query, params, isolate = False, transaction = False)
        except:
            logger.info("==========================================================================")
            logger.info(query)
            logger.info(params)
            logger.info("==========================================================================")
            
            logger.info("--------->")
            logger.info(content)
            logger.info("==========================================================================")

        return content

def make_prop(properties):
        # make properties from given input, the type is labeled after _as_
        typed_properties = {}
        for key, value in properties.items():
            prop_type = key.split("_as_")[-1]
            Prop = atlas_prop.label_type[prop_type]
            v = Prop(value)
            typed_properties[key] = v
        return typed_properties

class Vertex(object):
    def __init__(self, handler, label = None, properties = {}):
        self.handler = handler
        self.label = label
        if label:
            properties.update({"label_as_string" : label})
        self.properties = make_prop(properties)
        if len(properties.keys()) > 0:
            prop_string = ", [" + ", ".join([k + ":" + k for k in self.properties.keys()]) + "]"
        else:
            prop_string = ""
        self.save_query = "g.addVertex(null %s)" % prop_string
        self._id = None

    def save(self):
        params = {k : v.to_database() for k,v in self.properties.items()}
        content = self.handler.execute(self.save_query, params)
        self._id = content["_id"]
        return self

    def execute(self, script, params):
        params.update({"_id" : self._id})
        content = self.handler.execute(script, params)
        return content

    def outV(self, label = ""):
        if label != "":
            label = "'" + label + "'"
        contents = self.handler.execute("v = g.v(%s)\n v.out(%s)" % (self._id, label))
        vertices = []
        for content in contents:
            label = content["_properties"].pop("label_as_string")
            vertex = Vertex(self.handler, label = label, properties = content["_properties"])
            vertex._id = content["_id"]
            vertices += [vertex]
        return vertices

    def inV(self, label = ""):
        if label != "":
            label = "'" + label + "'"
        contents = self.handler.execute("v = g.v(%s)\n v.in(%s)" % (self._id, label))
        vertices = []
        for content in contents:
            label = content["_properties"].pop("label_as_string")
            vertex = Vertex(self.handler, label = label, properties = content["_properties"])
            vertex._id = content["_id"]
            vertices += [vertex]
        return vertices


def get_vertex(handler, key, value):
    if isinstance(value, basestring):
        content = handler.execute("g.V('%s', '%s')" % (key, value))
    else:
        content = handler.execute("g.V('%s', %s)" % (key, str(value)))
    if len(content) > 1:
        logger.info("More than one vertex found.")
    elif len(content) == 0:
        logger.info("No vertex found.")
    else:
        content = content[0]
        label = content["_properties"].pop("label_as_string")
        vertex = Vertex(handler, label = label, properties = content["_properties"])
        vertex._id = content["_id"]
        return vertex

class Edge(object):
    def __init__(self, handler, v1, v2, label, properties = {}):
        self.handler = handler
        self.v1 = v1
        self.v2 = v2
        self.label = label
        self.properties = make_prop(properties)
        if len(properties.keys()) > 0:
            prop_string = ", [" + ", ".join([k + ":" + k for k in self.properties.keys()]) + "]"
        else:
            prop_string = ""
        self.save_query = "v1 = g.v(v1_id); v2 = g.v(v2_id); g.addEdge(null, v1, v2, label %s)" % prop_string
        self._id = None

    def save(self):
        params = {'v1_id' : self.v1._id, 'v2_id' : self.v2._id, 'label' : self.label}
        params.update({k : v.to_database() for k,v in self.properties.items()})
        content = self.handler.execute(self.save_query, params)
        self._id = content["_id"]
        return self





