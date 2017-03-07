import sys
#
# Name: Sunny Yoo
# Date: 2017-01-11
#
# How to run: From a commend-line interface, run this application with an input file as an argument
#             and an output option. (default: print on the screen, f: output as a file with printing on the screen)
# Ex) Printing on the screen only : python processingHostValues.py [input].txt
# Ex) Printing on the screen & output as a text file(CodingDemoOutput.txt)
#                                 : python processingHostValues.py [input].txt f
#
# Node: a node containing host name, average, max value, min value, and next node
class Node:
    def __init__(self, host, avg, max, min, next = None):
        self.host = host
        self.avg = avg
        self.max = max
        self.min = min
        self.next = next

# HostList: a simple LinkedList class with Nodes from the Node class
class HostList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def add_node(self, host, avg, max, min):
        if self.head == None:
            self.head = Node(host, avg, max, min, None)
            self.tail = self.head
        elif self.head.avg <= avg:
            current = Node(host, avg, max, min, self.head)
            self.head = current
            top = self.head
            while top.next != None:
                top = top.next
            self.tail = top
        else:
            top = self.head
            while top.next != None:
                if top.avg >= avg and top.next.avg < avg :
                    temp = top.next
                    top.next = Node(host, avg, max, min, temp)
                    return
                top = top.next
            top.next = Node(host, avg, max, min, None)
            self.tail = Node(host, avg, max, min, None)

    def print_onScreen(self):
        top = self.head
        while top != None:
            print "%s: Average: %.1f Max: %.1f Min: %.1f" %(top.host, top.avg, top.max, top.min)
            top = top.next

    def print_toFile(self):
        text_file = open("CodingDemoOutput.txt","w")
        top = self.head
        while top != None:
            text_file.write("%s: Average: %.1f Max: %.1f Min: %.1f\n" %(top.host, top.avg, top.max, top.min))
            top = top.next
        text_file.close()

# ProcessInputFile: a class to read from input file, calculate values, create a list to store each row for each host, and print out the result
class ProcessInputfile:
    def __init__(self, input_file):
        # a list to contain processed data for each host
        self.sorted_list = HostList()
        self.filename = input_file
    
    def line_to_list(self):
        with open(self.filename, "r") as rows:
            for line in rows:
                delim = '|'
                info_or_value = line.split(delim)
                delim = ','
                host = info_or_value[0].split(delim)
                values = [float(x) for x in info_or_value[1].split(delim) if x.strip() and x.strip('None')]
                average, max, min = self.calculate_values(values)
                self.sorted_list.add_node(host[0],average,max,min)

    def calculate_values(self, values):
        average = sum(values)/float(len(values))
        return average, max(values), min(values)
    
    def printOutput(self, mode):
        self.sorted_list.print_onScreen()
        if mode=='f':
            self.sorted_list.print_toFile()

if __name__ == "__main__":
    sys.argv = sys.argv[1:]
    input_file = sys.argv[0]
    mode = None
    if sys.argv[1:] != None:
        mode = sys.argv[1:]
    if len(mode) != 0:
        mode = mode[0]
    output = ProcessInputfile(input_file)
    output.line_to_list()
    output.printOutput(mode)
