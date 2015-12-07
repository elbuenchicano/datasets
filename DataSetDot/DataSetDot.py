#dot language package : pip install graphviz
import graphviz as gv
import glob, os
import functools

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph


def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

################################################################################
styles = {
    'graph': {
        'label': 'Datasets - SSIG',
        'fontsize': '16',
        'fontcolor': 'gray',
        'rankdir': 'LR',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'none',
        'fontcolor': 'black',
        'color': 'beige',
        'style': 'filled',
        'fillcolor': 'beige',
    },
    'edges': {
        'color': 'black',
        'fontname': 'Courier',
        'fontsize': '12',
        'fontcolor': 'gray',
    }
}

################################################################################
###############################################################################
#get the last name
def ridofTwoPoitns_Back(str):
    clean   = str.replace(":","")
    clean   = clean.replace("\\","")
    return clean

###############################################################################
#get the last name
def getLastName(root):
    root_splitted   = root.split("\\")
    root_name       = root_splitted[len(root_splitted)-1]
    return root_name

###############################################################################
#label builder makes the table for the node label
def builderLabel(root, full):
    str = '< <TABLE bgcolor="beige" cellspacing="0" border="0" cellborder="0">'
    str = str + '<TR><TD href="' + full + '">'
    str = str + getLastName(root)
    str = str + '</TD></TR> </TABLE>>'
    return str

###############################################################################
#directory: source directory
def buildGraph(directory, outDirectory):
    #svg html format
    #creating the graph base
    graph = functools.partial(gv.Graph, format='svg')
    edges = []
    #appending the root
    cleanD  = ridofTwoPoitns_Back(directory)
    nodes   = [(cleanD, {'label': builderLabel(directory, directory)})]

    #walking trouhgt directory
    for root, dirs, files in os.walk(dir):
        print(root)
        for dire in dirs:
            full    = os.path.join(root, dire)
            lbl     = builderLabel(dire, full)
            cleanD  = ridofTwoPoitns_Back(full)
            cleanR  = ridofTwoPoitns_Back(root)
            nodes.append(
                (cleanD, {'label': lbl})
            )
            edges.append(
                (cleanR, cleanD)
            )

        for file in files:
            if file.endswith(".info"):
            #print(os.path.join(root, file))
                print(file)
    out = add_edges(
        add_nodes(graph(),nodes),
        edges
    ) 
    out = apply_styles(out, styles)
    out.render(outDirectory)
    
#end buildgraph
################################################################################

#g1 = gv.Graph(format='svg')
#g1.node('A')
#g1.node('B')
#g1.edge('A', 'B')
#print(g1.source)
#filename = g1.render(filename='s:/Documents/g1')


#graph = functools.partial(gv.Graph, format='svg')
#digraph = functools.partial(gv.Digraph, format='svg')

#stri = "d:\graderia"

#nodes = [ 'B', ('C', {})]
#lbl = builderLabel(stri)
##nodes.append(('A', {'label': '<<TABLE bgcolor="beige" cellspacing="0" border="0" cellborder="0"> <TR><TD href="http:www.google.com">OUR BUSINESS SERVICES</TD></TR> </TABLE>>'}))
#nodes.append(('A', {'label': lbl}))

#edges = [
#    ('A', 'B'),
#    ('B', 'C'),
#    (('A', 'C'), {}),
#]


#g6 = add_edges(
#    add_nodes(graph(), [
#        ('A', {'label': '<<TABLE bgcolor="beige" cellspacing="0" border="0" cellborder="0"> <TR><TD href="http:www.google.com">OUR BUSINESS SERVICES</TD></TR> </TABLE>>'}),
#        ('B', {'label': 'Node B'}),
#        'C'
#    ]),
#    [
#        ('A', 'B'),
#        ('A', 'C'),
#        ('B', 'C')
#    ]
#)

#g6 = add_edges(
#    add_nodes(graph(),nodes),
#    edges
#)

#g6 = apply_styles(g6, styles)
#g6.render('s:/Documents/g1')

######################################################################################
######################################################################################
######################################################################################
if __name__ == "__main__":
    dir     = "z:\\"
    outdir  = "s:/Documents/g1"
    buildGraph(dir, outdir)
    
    