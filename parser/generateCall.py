from sys import argv
from GraphMLTopotoMininetNetworkGeneratorFunction import generate

## Przyklad uzycia
arg = []
arg.append("-f")
arg.append("topologies/Abilene.graphml") # Path to graphML file
arg.append("-o")
arg.append("topologies/Abilene-generated.py") # Output file name
#etc

generate(arg)

## Lub rownowaznie mozna odkomentowac ponizej i z linii komend: python generateCall.py -f GML_File_Path.graphml
#generate(argv)
