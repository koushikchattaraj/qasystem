ls=[i for i in range(100) if i%11==0]
print(len(ls))
print(ls)

def gen(n):
    for i in range(n):
     yield i

g=gen(10)
print(g.__next__())
print(g.__next__())
for i in g:
    print(i)