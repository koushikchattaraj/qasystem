

class system:

    def __init__(self):
        self.database={}
        
        self.register()

    def register(self):
        print("Welcome to Register Page")
        username = input("HI Enter Your name")
        password = input("Enter Your password")
        self.database[username]=password
        print("Register Sucessfully")
        self.login()

    def login(self):
        print("Welcome to Login Page")
        login = input("Enter Your name")
        password = input("Enter Your password")
        
        if login in self.database and self.database[login] == password:
            print("Hi "+ login +" Lets Play The game")
            
            



        else:
            print("Sorry Please Go To Register Page")
            self.register()


        




obj=system()