from visual import *

floor = box (pos=(0,0,0), length=4, height=0.5, width=4, color=color.blue)
ball = sphere (pos=(0,4,0), radius=1, color=color.red)
ball.velocity = vector(0,-1,0)
dt = 0.01

while 1:
    sleep(0.01)
    ball.pos = ball.pos + ball.velocity*dt
    if ball.y < ball.radius:
        ball.velocity.y = -ball.velocity.y
    else:
        ball.velocity.y = ball.velocity.y - 9.8*dt