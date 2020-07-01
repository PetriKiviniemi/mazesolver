class PQ(object):

    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    def isEmpty(self):
        return len(self.queue) == 0

    def heapify(self):
        #TODO:: Implement heapify method for unordered binary trees (Not the case with mazes)
        return

    def insert(self, value):
        self.queue.append(value)

    def pop(self):
        #If the queue contains tuples, compare the tuple's Y values (depth) and return the min elem found
        if len(self.queue) > 0 and type(self.queue[0]) == tuple:
            try: 
                indexOfMin = 0
                for i in range(len(self.queue)):
                    if self.queue[i][1] < self.queue[indexOfMin][1]:
                        indexOfMin = i
                item = self.queue[indexOfMin]
                del self.queue[indexOfMin]
                return item
            except IndexError:
                print()
                exit()
        #This part is suitable for node objects
        try:
            indexOfMin = 0
            for i in range(len(self.queue)):
                if self.queue[i] < self.queue[indexOfMin]:
                    indexOfMin = i 
            item = self.queue[indexOfMin]
            del self.queue[indexOfMin]
            return item
        except IndexError:
            print()
            exit()
