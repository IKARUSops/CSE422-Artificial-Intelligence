import heapq
fileLocation = input('Enter path of txt file: ')
inp = open(fileLocation, 'r')
inp1 =inp.read()
inp1 = ''.join([i.upper() for i in inp1])
inp2 = inp1.split('\n')
inp3 = [inp2[i] for i in range(len(inp2))]
inp4 = [i.split() for i in inp3]
print('Your locations: ',[i[0] for i in inp4])
h = {i[0]:int(i[1]) for i in inp4}

graph = {}
for i in inp4:
  graph[i[0]] = (i[2::2],[int(j) for j in i[3::2]])


class PriorityQueue:
    def __init__(self):
        self.queue = []
    
    def push(self, node, cost, heuristic, parent):
        heapq.heappush(self.queue, (cost + heuristic, cost, node, parent))
    
    def pop(self):
        return heapq.heappop(self.queue)
    
    def isEmpty(self):
        return len(self.queue) == 0

def aStar(start, destination):
    global h, graph
    pq = PriorityQueue()
    pq.push(start, 0, h[start], None)
    
    checked = set()
    parentList = {}
    costRoute = {start: 0}  
    
    while not pq.isEmpty():
        _, actCost, currentNode, parent = pq.pop()
        
        if currentNode in checked:
            continue
        
        checked.add(currentNode)
        parentList[currentNode] = parent
        
        if currentNode == destination:
            path = []
            parentNode = currentNode
            while parentNode:
                path.append(parentNode)
                parentNode = parentList[parentNode]
            return path[::-1], actCost  
        
        edge = graph[currentNode][0]
        distances = [int(d) for d in graph[currentNode][1]]
        
        for i in range(len(edge)):
            if edge[i] not in checked:
                newCost = actCost + distances[i]
                if edge[i] not in costRoute or newCost < costRoute[edge[i]]:
                    costRoute[edge[i]] = newCost
                    pq.push(edge[i], newCost, h[edge[i]], currentNode)
    
    return None, float('inf')  # Return None and infinity if no path is found

start = input('Enter the start node: ').upper()
while start not in h:
    print("Invalid start node. Please enter a valid node.")
    start = input('Enter the start node: ').upper()

destination = input('Enter the destination node: ').upper()
while destination not in h:
    print("Invalid destination node. Please enter a valid node.")
    destination = input('Enter the destination node: ').upper()


try:
    path, distance = aStar(start, destination)
    if path is None:
        print("No path found.")
    else:
        print("Path found:", path)
        print("Total distance:", distance)
except KeyError as e:
    print(f"Error: Missing node data for {e}")
except Exception as e:
    print(f"Unexpected error: {e}")