import turtle 
import random

tutu = turtle.Turtle()
screen =  turtle.Screen()

def angle_provider(sides):
    return 360/sides

def create_shape(sides,angle):
    for _ in range(sides):
        tutu.forward(100)
        tutu.right(angle)
        

def create_final():
    for i in range(3,11):
        angle = angle_provider(i)
        create_shape(i,angle)


create_final()
turtle.done()
