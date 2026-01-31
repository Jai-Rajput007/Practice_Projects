import random
import turtle

size = turtle.screensize(2000,2000,bg="black")
screen = turtle.Screen()
tutu = turtle.Turtle()
turtle.colormode(255)
tutu.shape(name="circle")
tutu.hideturtle()
tutu.pen(pensize=8)
tutu.speed(10)

def movement():
    if direction() == 0:
        tutu.left(90)
    else:
        tutu.right(90)
    tutu.forward(25)

def direction():
    return random.randint(0,1)

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

for _ in range(2001):
    tutu.color(random_color())
    movement()

turtle.done()