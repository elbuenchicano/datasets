#dot language package : pip install graphviz
import graphviz as gv
import glob, os
import functools 
import fileinput
import queue
from   collections import deque

class DirectoryNode:
    father_ = ""
    name_   = ""
    tags_   = "" 
    id_     = ""
    
    def __init__(self, name, fatherid, id, tags):
        self.name_   = name
        self.father_ = fatherid
        self.id_     = id
        self.tags_   = tags

################################################################################

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
def listdir_fullpath(d, token):
    list    = []
    hasflag = False
    infof   = ""
    for f in os.listdir(d):
        full = os.path.join(d, f)
        if f.find(token) > -1:
            hasflag = True
            infof   = full
            
        if os.path.isdir(full) == True:
            list.append(full)

    if hasflag == True:
        return (list, infof)
    return ([],"")

################################################################################
def readTagsFromFile(filename):
    for line in open(filename):
        pos  = line.find("tags:")
        if  pos > -1:
            return line[(pos+6):]
    return ""
        
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
    str = str + '<TR><TD href="' + full.replace("\\","/") + '">'
    str = str + getLastName(root)
    str = str + '</TD></TR> </TABLE>>'
    return str

###############################################################################
#label builder makes the table for the node label
def builderLabelInfo(root, full, info):
    str = '< <TABLE bgcolor="beige" cellspacing="0" border="0" cellborder="0">'
    str = str + '<TR><TD href="' + full.replace("\\","/") + '">'
    str = str + getLastName(root)   + '</TD></TR>' 
    str = str + '<TR><TD>' + info   + '</TD></TR> </TABLE>>'
    return str

###############################################################################
#directory: source directory
def buildGraphDirectory(que, token):
    ID = fatherID = 0
    while len(que) > 0: 
        top  = que.popleft()
        list = listdir_fullpath(top[0], token)

        if len(list[0]) > 0:
            tags = readTagsFromFile(list[1])
            node = DirectoryNode(top[0], str(fatherID), str(ID), tags)
            listNodes.append(node)
            fatherID = ID
            ID   = ID + 1

        for sons in list[0]:
            que.append( (sons, fatherID) )

#end buildgraphDirectory
######################################################################################
def initGraphDirectory(directory, token):
    global listNodes
    listNodes = [ ]
    que       = deque([ (directory, 0) ])
    buildGraphDirectory(que, token)

#end initGraphDirectory
######################################################################################
def buildDot(outDirectory):
    nodes = []
    edges = []
    for nodeD in listNodes:
        #lbl = builderLabel(getLastName(nodeD.name_), nodeD.name_)
        lbl = builderLabelInfo(getLastName(nodeD.name_), nodeD.name_, nodeD.tags_)
        nodes.append(
            (nodeD.id_, {'label': lbl})
        )
    listNroot = listNodes[1:]
    for nodeD in listNroot:
        edges.append(
            (nodeD.father_, nodeD.id_)
        )
    #creating the graph    
    graph   = functools.partial(gv.Graph, format='svg')
    out = add_edges(
        add_nodes(graph(),nodes),
        edges
    ) 
    #applying the style
    out = apply_styles(out, styles)
    out.render(outDirectory)

#endbuildDot
######################################################################################
if __name__ == "__main__":
    dir     = "z:\\DATASETS"
    outdir  = "s:/Documents/g3"
    token   = ".info"
    initGraphDirectory(dir, token)
    buildDot(outdir)


    