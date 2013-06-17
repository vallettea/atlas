<div style="float: left; margin: 25px; width: 200px;"><img src="figs/atlas.png" /></div>

# Atlas
Atlas is aimed to be **lightweight**, **fast** and **generic** interface to Titan.

It is based on RexPro protocol and offers multi-sessions possibilities.

It enables to have typed (and rich) data structures associated with graph elements.

## Quick start

#### Create an Atlas instance and query the database:

    from atlas.base import Atlas
    atlas = Atlas("graph", "localhost")
    atlas.execute("g.V('name', name)", {name : "Alexandre"})

#### Create vertices and edges
All key of properties must contain the key word `_as_` followed by one of the folowing:

    - string
    - text
    - integer
    - datetime
    - date
    - time
    - timedelta
    - uuid
    - boolean
    - double
    - float
    - decimal

So for example:

    from atlas.base import Vertex, Edge
    import datetime
    v1 = Vertex(atlas, label="user", 
                properties = {"name_as_string" : "toto",
                                "age_as_integer" : 2,
                                "registered_as_datetime" : datetime.datetime.now(),
                                "income_as_float" : 3888.32,
                                "rate_as_decimal" : 3.2
                                })
    v1.save()
    v2 = Vertex(atlas, label="user", 
                properties = {"name_as_string" : "tata",
                                "age_as_integer" : 3,
                                "registered_as_datetime" : datetime.datetime.now(),
                                "income_as_float" : 5999.44,
                                "rate_as_decimal" : 5.2
                                })
    v2.save()
    e = Edge(atlas, v1, v2, "likes", 
            properties = {"how_much_as_integer" : 8})
    e.save()

You can also query vertices with a given property:

    v = atlas.get_vertex("name_as_string", "toto")
    e = atlas.get_edge("how_much_as_integer", 8)

but make sure you create an index **before adding nodes**:

    atlas.execute("g.makeType().name('name_as_string')
                    .dataType(String.class)
                    .unique(Direction.OUT)
                    .unique(Direction.IN)
                    .indexed(Vertex.class)
                    .makePropertyKey()")

#### Navigating the graph

    v1.out() #returns all the vertices poinited at by v1
    v1.out("likes") # only from edges having the label "likes"
## Differences with thunderdome

Atlas is different from thunderdome in various ways:

    + much more simple to tweek (no metaclasses)
    + less verbose because elements are defined in a generic way
    + much faster (because thunderdome uses REST)
    + is much closer to the structure of gremlin
    + gremlin queries can be written directly (no need of groovy scripts)
    - has no save strategies (yet)
    - has not yet a proper transactional protocol
    - properties should respect a *name_of_variable***_as_***type* syntax
    - no auto indices (they have to be defined manually)

# TODO

    -check if vertex exists before adding
    -implement functions for repetition calls
    - clarify the difference between long and integers
    - vertex.as_dict() should return properties in a readable way (use class representation as in django)



