file = open("data\\relations.txt", "r")
text = file.read()
relations = text.splitlines()

graph = {}

for relation in relations:
    nodes = relation.split('->')
    if not nodes[0] in graph.keys() :
        graph[nodes[0]] = [nodes[1]]
    else:
        lis = graph[nodes[0]]
        lis.append(nodes[1])
        
question_file = open("data\\question.txt", "r")
question_text = question_file.read()
question = question_text.splitlines()
start_tasks = question[0].split(':')[1].strip()
ending_task = question[1].split(':')[1].strip()
    
def find_opt_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not start in graph.keys():
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_opt_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

min_path =[]
path = []
start_tasks_list = start_tasks.split(',')

for stask in start_tasks_list:
    cur_path = find_opt_path(graph , stask , ending_task,path)
    if len(min_path) == 0 or len(min_path) > len(cur_path):
        min_path = cur_path

print('The minimun path is ',min_path)