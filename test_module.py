class Student:
    # Magic or Constructor Method
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    # instance method
    def info(self):
        return f"Name {self.name}, Email {self.email}"