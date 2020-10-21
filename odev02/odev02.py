

try:
    fileAirlines=open("airlines.txt", "r")
except:
    print("There is no file as such.")
 
myDict = {}
    
if fileAirlines is not None:
    for line in fileAirlines:
        splittedLine = line.strip().split(",")
        myDict[splittedLine[0]] = splittedLine[1:]
    


def find_all_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if node not in path:
                newpaths = find_all_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths
    
  
    
a = input("Enter the source airline: \n")
b = input("Enter the destination airline: \n")

if a not in myDict:
    print("There is no airline by the name of", a, ". Try again.\n")
elif b not in myDict:
    print("There is no airline by the name of", b, ". Try again.\n")
else:
    paths = find_all_paths(myDict, a,b)
    s=min(paths, key=len)
    l=max(paths, key=len)
    shortestPath = ' -> '.join([str(elem) for elem in s])
    longestPath = ' -> '.join([str(elem) for elem in l])
    if paths is not None:
        print("\n The shortest path from" ,a ,"to", b, "is: \n", shortestPath)
        print("\n The longest path from" ,a ,"to", b, "is: \n", longestPath)
    else:
        print("There is no path from" ,a, "to", b)
    
