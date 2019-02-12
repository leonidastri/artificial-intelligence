#!/bin/sh
import heapq

class PriorityQueue:

    def  __init__(self):

        self.heap = []
        self.count = 0

    # Insert item in specific position in priority queue by considering
    # the priority given
    def push(self, item, priority):

        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    # Return the item popped from priority queue
    def pop(self):

        if( self.count > 0 ):

            priority, counter, item = heapq.heappop(self.heap)
            self.count -= 1
            return item

        else:

            return "Attention!Priority queue is empty.Cannot find item to pop."

    # Check if priority queue is empty by checking
    # the self.count variable
    def isEmpty(self):
        return True if self.count == 0 else False

    ''' If item found, update the first occurence of item if priority is higher than
        the new priority else do nothing. If item not found, just push the item in priority
        queue
    '''
    def update(self, item, priority):

        i = 0
        found_item = False


        if self.count > 0:

            while i < self.count:

                heap_item_priority, heap_item_counter, heap_item = self.heap[i]

                if item == heap_item:

                    found_item = True

                    if heap_item_priority > priority:

                        del self.heap[i]
                        self.heap.append((priority, heap_item_counter, item))
                        heapq.heapify(self.heap)

                    break

                i += 1

        if not found_item:

            self.push(item, priority)


# Takes a list of integers and by using a priority queue returns
# a list of sorted integers
def PQSort( list ):

    q = PriorityQueue()

    for item in list:
        q.push(item, item)

    return [q.pop() for i in range(len(list))]


if __name__ == '__main__':

    q = PriorityQueue()
