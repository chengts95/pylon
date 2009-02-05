#------------------------------------------------------------------------------
#  Copyright (c) 2008 Richard W. Lincoln
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#  IN THE SOFTWARE.
#------------------------------------------------------------------------------

""" Defines a base class for many graphs. """

#------------------------------------------------------------------------------
#  Imports:
#------------------------------------------------------------------------------

from enthought.traits.api \
    import HasTraits, Str, List, Instance, Bool, Property, Constant, ReadOnly

from node import Node
from edge import Edge
from common import id_trait, Alias

#------------------------------------------------------------------------------
#  "BaseGraph" class:
#------------------------------------------------------------------------------

class BaseGraph(HasTraits):
    """ Defines a representation of a graph in Graphviz's dot language """

    #--------------------------------------------------------------------------
    #  Trait definitions.
    #--------------------------------------------------------------------------

    # Optional unique identifier.
    ID = id_trait

    # Synonym for ID.
    name = Alias("ID", desc="synonym for ID") # Used by InstanceEditor

    # Main graph nodes.
    nodes = List(Instance(Node))

    # Graph edges.
    edges = List(Instance(Edge))

    # Separate layout regions.
    subgraphs = List(Instance("godot.subgraph.Subgraph"))

    # Clusters are encoded as subgraphs whose names have the prefix 'cluster'.
    clusters = List(Instance("godot.cluster.Cluster"))

    # Tab width to use for string representation.
    padding = Str("    ")

    # Graph attributes defined in the Dot language.
    dot_attributes = ReadOnly#Constant()

    #--------------------------------------------------------------------------
    #  Xdot trait definitions:
    #--------------------------------------------------------------------------

    # For a given graph object, one will typically a draw directive before the
    # label directive. For example, for a node, one would first use the
    # commands in _draw_ followed by the commands in _ldraw_.
    _draw_ = Str(desc="xdot drawing directive")

    # Label draw directive.
    _ldraw_ = Str(desc="xdot label drawing directive")

    #--------------------------------------------------------------------------
    #  Trait initialisers:
    #--------------------------------------------------------------------------

    def _dot_attributes_default(self):
        """ Trait initialiser.
        """
        return []

    #--------------------------------------------------------------------------
    #  "object" interface:
    #--------------------------------------------------------------------------

    def __str__(self):
        """ Return a string representing the graph when requested by str()
        (or print).

        @rtype:  string
        @return: String representing the graph.

        """
        graph = self
        s     = ""
        padding = "  "

        if self.ID:
            s = "%s %s {\n" % (s, self.ID)
        else:
            s = "%s {\n" % s

        # Graph attributes.
        for trait_name in self.dot_attributes:
            # Get the value of the trait for comparison with the default value.
            value = getattr(graph, trait_name)

            default = graph.trait(trait_name).default

            # FIXME: Alias/Synced traits default to None.
            # Only print attribute value pairs if not defaulted.
            if ( value != default ) and ( default is not None ):
                valstr = str(value)

                if isinstance( value, basestring ):
                    # Add double quotes to the value if it is a string.
                    valstr = '"%s"' % valstr

                s = "%s%s%s=%s;\n" % ( s, padding, trait_name, valstr )

        for node in graph.nodes:
            s = "%s%s%s" % ( s, padding+padding, str( node ) )
        for edge in graph.edges:
            s = "%s%s%s" % ( s, padding+padding, str( edge ) )
        for subgraph in graph.subgraphs:
            s = "%s%s%s" % ( s, padding, str( subgraph ) )
        for cluster in graph.clusters:
            s = "%s%s%s" % ( s, padding, str( cluster ) )

        s += "}\n"

        return s


    def __len__(self):
        """ Return the order of the graph when requested by len().

        @rtype:  number
        @return: Size of the graph.

        """

        return len(self.nodes)


    def __iter__(self):
        """ Return a iterator passing through all nodes in the graph.

        @rtype:  iterator
        @return: Iterator passing through all nodes in the graph.

        """

        for each in self.nodes:
            yield each


    def __getitem__(self, node):
        """ Return a iterator passing through all neighbours of the given node.

        @rtype:  iterator
        @return: Iterator passing through all neighbours of the given node.

        """

        for each_edge in self.edges:
            if (each_edge.from_node == node) or (each_edge.to_node == node):
                yield each_edge

    #--------------------------------------------------------------------------
    #  Event handlers:
    #--------------------------------------------------------------------------

    def _edges_changed(self, new):
        """ Handles the list of edges changing. """

        for each_edge in new:
            # Ensure the edge's nodes exist in the graph.
            if each_edge.from_node not in self.nodes:
                self.nodes.append(each_edge.from_node)
            if each_edge.to_node not in self.nodes:
                self.nodes.append(each_edge.to_node)

            # Initialise the edge's list of available nodes.
            each_edge._nodes = self.nodes


    def _edges_items_changed(self, event):
        """ Handles edges being added and removed. """

        for each_edge in event.added:
            # Ensure the edge's nodes exist in the graph.
            if each_edge.from_node not in self.nodes:
                self.nodes.append(each_edge.from_node)
            if each_edge.to_node not in self.nodes:
                self.nodes.append(each_edge.to_node)

            # Initialise the edge's list of available nodes.
            each_edge._nodes = self.nodes


#    def _nodes_changed(self, new):
#        """ Handles the list of nodes changing.  Maintains each edge's list
#        of available nodes.
#        """
#        all_nodes = [g.nodes for g in self.all_graphs]
#        # Set the list of nodes in the graph for each branch.
#        for graph in self.all_graphs:
#            for each_edge in graph.edges:
#                each_edge._nodes = all_nodes
#
#
#    def _nodes_items_changed(self, event):
#        """ Handles nodes being added and removed.  Maintains each edge's
#        list of available nodes.
#        """
#        all_nodes = [g.nodes for g in self.all_graphs]
#        # Set the list of nodes in the graph for each branch.
#        for graph in self.all_graphs:
#            for each_edge in graph.edges:
#                each_edge._nodes = all_nodes

# EOF -------------------------------------------------------------------------
