import numpy as np
import matplotlib.pyplot as plt
import math

#Declare Variable
dl = 0.1
dt = 0.0001
c = 0.466
time = 1000
normal_temp = 150
x_size = 20
y_size = 20
z_size = 20
temp_x_pos = 200
temp_y_pos = 200
temp_z_pos = 50
temp_x_neg = 100
temp_y_neg = 100
temp_z_neg = 100

def define_gradient():
    temp_grad = [[[normal_temp for _ in range(x_size)] for _ in range(y_size)] for _ in range(z_size)]

    #X-axis wall
    for i in range(y_size):
        for j in range(x_size):
            temp_grad[0][i][j] = temp_x_pos
            temp_grad[z_size-1][i][j] = temp_x_neg

    #Y-axis wall
    for i in range(z_size):
        for j in range(x_size):
            temp_grad[i][0][j] = temp_y_pos
            temp_grad[i][y_size-1][j] = temp_y_neg

    #Z-axis wall
    for i in range(z_size):
        for j in range(y_size):
            temp_grad[i][j][0] = temp_z_pos
            temp_grad[i][j][x_size-1] = temp_z_neg

    return temp_grad

temp1 = define_gradient()
# for i in range(10):
#     print('')
#     for j in range(10):
#         print(temp1[i][j])

fig, axis = plt.subplots()

pcm = axis.pcolormesh(temp1[5], cmap = plt.cm.jet, vmin = 0, vmax = 200)
plt.colorbar(pcm, ax=axis)

for t in range(time):
    temp2 = define_gradient()
    for z in range(1,z_size-1):
        for y in range(1,y_size-1):
            for x in range(1,x_size-1):
                dd_temp_x = (temp1[z][y][x+1])+(temp1[z][y][x-1])-2*(temp1[z][y][x])
                dd_temp_y = (temp1[z][y+1][x])+(temp1[z][y-1][x])-2*(temp1[z][y][x])
                dd_temp_z = (temp1[z+1][y][x])+(temp1[z-1][y][x])-2*(temp1[z][y][x])
                temp2[z][y][x] = c * dt/(dl**2) * (dd_temp_x+dd_temp_y+dd_temp_z) + temp1[z][y][x]
    temp1 = temp2.copy()
# for i in range(10):
#     print('')
#     for j in range(10):
#         print(temp1[i][j])
    pcm.set_array(temp1[5])
    plt.pause(0.01)

plt.show()