#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import sys

from anytree import Node, RenderTree
from shutil import copyfile
from anytree.exporter import JsonExporter
import fileinput
import re
import pkg_resources


def tree2graph(data):
    """
    Convert a JSON to a graph.

    Parameters
    ----------
    json_filepath : str
        Path to a JSON file

    Examples
    --------
    >>> s ={"Harry":{"//comments":"IDuniquedudocument","//type":"keyword","//card":"1.1","Bill":{"Jane":[{"Diane":"Mary"},{"Louise":"Mark"}]}}}
    >>> tree2graph(s)
    ([('Harry', 'Bill'), ('Bill', 'Jane'), ('Jane', 'Diane'), ('Diane', 'Mary'), ('Jane', 'Louise'), ('Louise', 'Mark')], Node('/root'))
    """
    # Extract tree edges from the dict
    edges = []
    root = Node("root")
    properties = ['current', '//comments', '//card', '//type','transformation type','transformation copyTo','transformation enabled']
   
    def getNodeName(node, parent):
        if node is None:
            return 'root'
        elif str(node) == 'data':
            return str(node) + '.' + str(parent)
        elif any(str(node) in s for s in properties):
            return None                   
        return node

    def addNode(nodeToAdd, tree, parent, root):
        edges.append((parent, nodeToAdd))
        if isinstance(root, dict):
            nComments=None
            if('//comments' in root):
                nComments=root['//comments']
            nCard=None
            if('//card' in root):
                nCard=root['//card']
            nType=None
            if('//type' in root):
                nType=root['//type']
            newNode = Node(nodeToAdd, parent=tree, comment=nComments,card=nCard, type=nType)
        else:
            newNode = Node(nodeToAdd, parent=tree)
        return newNode

    def get_edges(root, tree, parent, gdParent):
        parentName = str(parent)
        if getNodeName(parent, gdParent) is None:
            return
        if isinstance(root, dict):
            for name, item in root.items():
                if parent is not None and getNodeName(name, gdParent) is not None:
                    t = addNode(getNodeName(name, parent), tree, getNodeName(parent, gdParent), item  )
                    get_edges(item, t, name, parent)
                else:
                    get_edges(item, tree, name, parent)
        elif isinstance(root, list):
            for el in root:
                if parent is not None and not isinstance(el, dict) and getNodeName(el, parent) is not None:
                    t = addNode(getNodeName(el, parent), tree, getNodeName(parent, gdParent), el)
                get_edges(el, tree, parent, gdParent)
        elif isinstance(root, str) and getNodeName(root, parent) is not None:
            addNode(getNodeName(root, parent), tree, getNodeName(parent, gdParent), root)

    get_edges(data, root, None, None)

    return edges, root
   


def main(json_filepath, out_dot_path, htmlTitle):
  
    """IO."""
    # Read JSON
    with open(json_filepath) as data_file:
        data = json.load(data_file)

    # Get edges
    edges, root = tree2graph(data)
   
    exporter = JsonExporter(indent=1, sort_keys=True)

    tempFile= out_dot_path+'.tmp'
    f = open(tempFile, 'w')
    print(exporter.export(root), file=f)
    f.close()
 
    find = "'"
    replace = " "
    jsonTreeString=''
    for line in fileinput.input(files=tempFile):
        line = re.sub(find,replace, line.rstrip())
        jsonTreeString= jsonTreeString+line
        #print(line)

    body='<body onload="onLoadDocument();">'
    body=body+'<h1>'+htmlTitle+'</h1>'
    body=body+' <input id="vdspdata" type="hidden" value=\''+jsonTreeString+'\' />'
    body=body+'</body>'

    src='treeViewer.html'
    filepath = pkg_resources.resource_filename(__name__, src)
    dst=out_dot_path
    copyfile(filepath, dst)
    with open(dst, "a") as myfile:
        myfile.write(body)

def get_parser():

    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("-i", "--input",
                        dest="json_filepath",
                        help="JSON FILE to read",
                        metavar="FILE",
                        required=False)
                        
    parser.add_argument("-o", "--output",
                        dest="out_dot_path",
                        help="html output file",
                        metavar="FILE",
                        required=True)
 
    parser.add_argument("-t", "--title",
                        dest="htmlTitle",
                        help="Title of the generated html",
                        required=True)                        
    return parser

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    args = get_parser().parse_args()
    main(  json_filepath =args.json_filepath, out_dot_path= args.out_dot_path, htmlTitle= args.htmlTitle)
