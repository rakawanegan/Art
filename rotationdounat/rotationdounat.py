# imitation of https://qiita.com/kurumaebi65/items/7e31b762fb529ad98739

import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()

div1 = 25
div2 = 25
R1 = 1
R2 = 2

def make_points(A,B):
    x = []
    y = []
    z = []

    sinA = math.sin(A)
    sinB = math.sin(B)
    cosA = math.cos(A)
    cosB = math.cos(B)
    for theta in [(2*math.pi*x)/div1 for x in range(div1)]:
        for phi in [(2*math.pi*x)/div2 for x in range(div2)]:
            cosphi = math.cos(phi)
            circlex = R2+R1*math.cos(theta)
            circley = R1*math.sin(theta)
            cordx = (circlex)*(cosB*cosphi+sinA*sinB*math.sin(phi))-circley*cosA*sinB
            cordy = (circlex)*(cosphi*sinB-cosB*sinA*math.sin(phi))+circley*cosA*cosB
            cordz = (cosA*(circlex)*math.sin(phi) + circley*sinA)

            x.append(cordx)
            y.append(cordy)
            z.append(cordz)

    return x,y,z

ax = fig.add_subplot(projection='3d')

A = 0
B = 0

def plot(data):
    ax.cla()
    ax.set_xlim(2,-2)
    ax.set_ylim(2,-2)
    ax.set_zlim(2,-2)
    global A
    global B
    A += 0.1
    B += 0.1
    x,y,z = make_points(A,B)
    ax.scatter(x, y, z, color='blue')



ani = animation.FuncAnimation(fig, plot, interval=100, frames=100)

ani.save("rotationdounat.gif")
plt.show()
