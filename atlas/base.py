import logging

from rexpro import RexProConnection

from atlas import properties as atlas_prop

logger = logging.getLogger(__name__)


class Atlas(object):
    def __init__(self, graph_name, hostname, username = None, password = None, batchmode = False):
        self.graph_name = graph_name
        self.username = username
        self.password = password
        self.batchmode = batchmode
        self.conn = RexProConnection(hostname, 8184, graph_name)
        
        #execute_query("g.makeType().name('vid').dataType(String.class).unique(Direction.OUT).unique(Direction.IN).indexed(Vertex.class).indexed(Edge.class).makePropertyKey()")

        if batchmode:
            execute_query("bg = new BatchGraph(g, VertexIDType.STRING, 1000) ; bg.setVertexIdKey('vid');")   

    def execute(self, query, params = {}):
        
        print "=========================================================================="
        print query
        print params
        print "=========================================================================="
        content = self.conn.execute(query, params, isolate = False)
        print "--------->"
        print content
        print "=========================================================================="

        return content


class Vertex(object):
    def __init__(self, handler, properties = {}):
        self.handler = handler
        self.properties = properties
        self._id = None

    def save(self):
        # make properties from given input, the type is labeled after _as_
        typed_properties = {}
        for key, value in self.properties.items():
            prop_type = key.split("_as_")[-1]
            Prop = atlas_prop.label_type[prop_type]
            v = Prop(value)
            typed_properties[key] = v

        property_list = "[" + ", ".join([k + ":" + str(v.to_database()) for k, v in typed_properties.items()]) + "]"
        content = self.handler.execute("g.addVertex(null, %s)" % property_list)
        self._id = content["_id"]

    def outV(self, label = ""):
        if label != "":
            label = "'" + label + "'"
        contents = self.handler.execute("v = g.v(%s)\n v.out(%s)" % (self._id, label))
        vertices = []
        for content in contents:
            properties = {}
            for key, value in content["_properties"].items():
                prop_type = key.split("_as_")[-1]
                Prop = atlas_prop.label_type[prop_type]
                v = Prop(value).to_python()
                properties[key] = v            
            vertex = Vertex(self.handler, properties)
            vertex._id = content["_id"]
            vertices += [vertex]
        return vertices


def get_vertex(handler, key, value):
    content = handler.execute("g.V('%s', '%s')" % (key, str(value)))
    if len(content) > 1:
        print "More than one vertex found."
    elif len(content) == 0:
        print "No vertex found."
    else:
        content = content[0]
        properties = {}
        for key, value in content["_properties"].items():
            prop_type = key.split("_as_")[-1]
            Prop = atlas_prop.label_type[prop_type]
            v = Prop(value).to_python()
            properties[key] = v            
        vertex = Vertex(handler, properties)
        vertex._id = content["_id"]
        return vertex

class Edge(object):
    def __init__(self, handler, v1, v2, label, properties = {}):
        self.handler = handler
        self.v1 = v1
        self.v2 = v2
        self.label = label
        self.properties = properties
        self._id = None

    def save(self):
        typed_properties = {}
        for key, value in self.properties.items():
            prop_type = key.split("_as_")[-1]
            Prop = atlas_prop.label_type[prop_type]
            v = Prop(value)
            typed_properties[key] = v
        property_list = "[" + ", ".join([k + ":" + str(v.to_database()) for k, v in typed_properties.items()]) + "]"
        content = self.handler.execute("v1 = g.v(%s)\n v2 = g.v(%s)\n g.addEdge(null, v1, v2, '%s', %s)"
                                         % (self.v1._id, self.v2._id, self.label, property_list))
        self._id = content["_id"]







