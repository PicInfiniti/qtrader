class Robot:
    
    def __init__(self, name):
        self.name = name
        
    def say_hi(self):
        print("Hi, I am " + self.name)
        
class PhysicianRobot(Robot):
    pass
    
x = Robot("Marvin")
y = PhysicianRobot("James")
print(x, type(x))
print(y, type(y))
y.say_hi()
