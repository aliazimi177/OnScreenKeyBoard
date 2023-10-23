from anytree import Node, AnyNode, RenderTree, find
from anytree.exporter import JsonExporter
import pandas as pd

root = Node("root")
words = pd.read_json('words.json')[0]


def create_tree():
    index = 0
    for word in words:
        create_node(word)
        index += 1
        print(index)

def node_exists(name):
    result = find(root, lambda node: node.name == name)
    return result != None

def find_node(name):
    return find(root, lambda node: node.name == name)

def create_node(word):
    for index in range(len(word)+1):
        if node_exists(word[:index]) == False:
            if len(word[:index]) == 1:
                Node(word[:index], parent=root)
            else:
                Node(word[:index], parent=find_node(word[:(index-1)]))

create_tree()

exporter = JsonExporter(indent=2, sort_keys=True)
json = exporter.export(root)
f = open("sortedWords.Json", "x")
f.writelines(json)


for pre, fill, node in RenderTree(root):
    print("%s%s" % (pre, node.name))
