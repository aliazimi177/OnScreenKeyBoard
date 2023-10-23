from anytree.importer import JsonImporter
from anytree import RenderTree
from anytree.search import findall

f = open("sortedWords.Json", "r")

json = f.read()

importer = JsonImporter()

root = importer.import_(data=json)

#for pre, fill, node in RenderTree(root):
    #print("%s%s" % (pre, node.name))

def suggest(q):
    #res = findall(root, lambda node: q in node.name)
    res = findall(root, lambda node: node.name.startswith(q))
    return res[:8]
