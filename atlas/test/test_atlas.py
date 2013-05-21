from atlas.base import Atlas


atlas = Atlas("graph", "localhost", batchmode = False)

# sending gremlin messages:
atlas.execute("g.makeType().name('vid').dataType(String.class).unique(Direction.OUT).unique(Direction.IN).indexed(Vertex.class).indexed(Edge.class).makePropertyKey()")
atlas.execute("g.addVertex(null,[vid:'stephen'])")

atlas.execute("g.V('vid', 'stephen')")
