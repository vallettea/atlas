import logging

from rexpro import RexProConnection

from atlas.properties import *

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
            execute_query("bg = new BatchGraph(g,VertexIDType.STRING,1000) ; bg.setVertexIdKey('vid');")   

    def execute(self, query, params = {}):
        
        print "=========================================================================="
        print query
        print params
        print "=========================================================================="
        content = self.conn.execute(query, params, isolate = False)
        print "--------->"
        print content
        print "=========================================================================="

        if not isinstance(content, list):
            content = [content]

        to_integer = ['_id', '_inV', '_outV']

        for elem in content:
            if isinstance(elem, dict):
                if elem.has_key('_id') and elem['_type'] == 'vertex':
                    elem['_id'] = int(elem['_id'])
                # if elem.has_key('_inV') and elem['_type'] == 'edge':
                #     elem['_inV'] = int(elem['_inV'])
                # if elem.has_key('_outV') and elem['_type'] == 'edge':
                #     elem['_outV'] = int(elem['_outV'])        

        # because rexpro puts thing under a property dictionnary
        for elem in content:
            if isinstance(elem, dict):
                if elem.has_key('_properties'):
                    elem.update(elem['_properties'])
                    del elem['_properties']


        logger.info(content)
        return content


class Vertex(object):
    def __init__(self, handler, properties = {}, functions = {}):
        self.handler = handler
        self.properties = properties
        self.functions = functions
        self.save()


    def save(self):
        property_list = "[" + ", ".join([k + ":" + str(v.to_database()) for k, v in self.properties.items()]) + "]"
        self.handler.execute("g.addVertex(null, %s)" % property_list)










