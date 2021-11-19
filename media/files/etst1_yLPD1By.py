a = lambda x, y: x*y
print(a(2, 5))

import copy 
list1=[1,3,[7,4],6]
list2=copy.copy(list1)
list2[2][0]=5
print(list1)