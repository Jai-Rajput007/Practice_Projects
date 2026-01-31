import turtle

tutu = turtle.Turtle()
screen = turtle.Screen()
tutu.shape(name="square")


def snake():
    tutu.resizemode(rmode="user")
    tutu.shapesize(stretch_len=3)

snake()
turtle.done()