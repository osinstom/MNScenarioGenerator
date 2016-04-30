from topo_parser import generate

arg = []
arg.append("-f")
arg.append("topologies/zoo-dataset/Agis.graphml") # Path to graphML file
arg.append("-o")
arg.append("gen_test.py") # Output file name
arg.append("-h")
arg.append("3")
generate(arg)


