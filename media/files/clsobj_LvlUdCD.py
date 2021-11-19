
class math:

    def __init__(self):
        

        self.input()

    def input(self):
        self.a=int(input('Enter a number '))
        self.b=int(input('Enter a number '))
        x = input("What u want??")
        if x == "add" or x == "+":
            self.add()

        elif x == "sub" or x == "-":
            self.sub()

        else:
            print("Please")
        

    def add(self):
        c=self.a + self.b
        print(c)

    def sub(self):
        c=self.a-self.b
        print(c)
        

    
        




obj=math()