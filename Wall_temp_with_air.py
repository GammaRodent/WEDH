#5680 x 2000 x3320


import numpy as np
import matplotlib.pyplot as plt
import math

#Sun Intensity
def sun_intensity(start_time,end_time,current_time,intensity,tilt_angle=0):
    total_time = end_time-start_time
    angle_of_sun = (current_time/total_time)*np.pi
    ind_var = (math.sin(angle_of_sun)*math.cos(tilt_angle))
    if ind_var == 0:
        ind_var = 0.00001
    intensity = intensity*1.4*0.7**(ind_var**-0.678)
    x_intensity = int(intensity*math.cos(angle_of_sun))
    y_intensity = int(intensity*math.sin(angle_of_sun)*math.cos(tilt_angle))
    z_intensity = int(intensity*math.sin(angle_of_sun)*math.sin(tilt_angle))
    return (x_intensity,y_intensity,z_intensity)

time = np.linspace(0,1500,1500)
x_intensity = np.zeros(1500)
y_intensity = np.zeros(1500)
z_intensity = np.zeros(1500)

for t in range(720):
    x,y,z = sun_intensity(0,720,t,500)
    x_intensity[t] = x
    y_intensity[t] = y
    z_intensity[t] = z

#Declare Variable
thickness = 0.1
dl = 0.01
dt = 0.0001
c_wall = 0.466
c_air = 0.1
time = 720
normal_temp = 30
outside_temp = 40
a = 0.5 #solar radiation absorptivity
h = 20 #convection,radiation heat transfer coefficient

#Parameter of the room
x_size = 57
y_size = 17
z_size = 33

## XY wall is the roof (0)
## YZ1 and YZ2 are the wall on the east and west (1,2)
## XZ1 and XZ2 are the wall on the north and south (3,4)

def setup_gradient_wall():
    temp_wall = [[normal_temp for _ in range(int(thickness/dl))] for _ in range(5)]
    for i in range(5):
        temp_wall[i][0] = outside_temp
    temp_wall[0][-1] = temp1[z_size//2][y_size-2][x_size//2]
    temp_wall[1][-1] = temp1[z_size//2][y_size//2][0]
    temp_wall[2][-1] = temp1[z_size//2][y_size//2][x_size-2]
    temp_wall[3][-1] = temp1[0][y_size//2][x_size//2]
    temp_wall[4][-1] = temp1[z_size-2][y_size//2][x_size//2]
    return temp_wall

def setup_gradient_air():
    temp_grad = [[[normal_temp for _ in range(x_size)] for _ in range(y_size)] for _ in range(z_size)]
    #X-axis wall
    for i in range(y_size):
        for j in range(x_size):
            temp_grad[0][i][j] = wall_temp1[3][-2]
            temp_grad[z_size-1][i][j] = wall_temp1[4][-2]

    #Y-axis wall
    for i in range(z_size):
        for j in range(x_size):
            temp_grad[i][0][j] = 30
            temp_grad[i][y_size-1][j] = wall_temp1[0][-2]

    #Z-axis wall
    for i in range(z_size):
        for j in range(y_size):
            temp_grad[i][j][0] = wall_temp1[1][-2]
            temp_grad[i][j][x_size-1] = wall_temp1[2][-2]
    return temp_grad

temp1 = [[[normal_temp for _ in range(x_size)] for _ in range(y_size)] for _ in range(z_size)]

wall_temp1 = setup_gradient_wall()
temp1 = setup_gradient_air()

fig1, axis1 = plt.subplots(nrows = 5)
fig2, axis2 = plt.subplots()

wall1 = axis1[0].pcolormesh([wall_temp1[0]], cmap = plt.cm.jet, vmin = 0, vmax = 45)
wall2 = axis1[1].pcolormesh([wall_temp1[1]], cmap = plt.cm.jet, vmin = 0, vmax = 45)
wall3 = axis1[2].pcolormesh([wall_temp1[2]], cmap = plt.cm.jet, vmin = 0, vmax = 45)
wall4 = axis1[3].pcolormesh([wall_temp1[3]], cmap = plt.cm.jet, vmin = 0, vmax = 45)
wall5 = axis1[4].pcolormesh([wall_temp1[4]], cmap = plt.cm.jet, vmin = 0, vmax = 45)
room = axis2.pcolormesh(temp1[17], cmap = plt.cm.jet, vmin = 0, vmax = 45)
plt.colorbar(wall1, ax=axis1)
plt.colorbar(room, ax=axis2)

for t in range(time):
    #Wall
    wall_temp2 = setup_gradient_wall()
    wall_temp1[0][1] += int(a*y_intensity[t]/h)
    if x_intensity[t] > 0:
        wall_temp1[1][1] += int(a*x_intensity[t]/h)
    else:
        wall_temp1[2][1] += int(a*-1*x_intensity[t]/h)
    if z_intensity[t] > 0:
        wall_temp1[3][1] += int(a*z_intensity[t]/h)
    else:
        wall_temp1[4][1] += int(a*-1*z_intensity[t]/h)
    
    for i in range(5):
        for j in range(1,int(thickness/dl-1)):
            dd_temp = wall_temp1[i][j+1]+wall_temp1[i][j-1]-2*wall_temp1[i][j]
            wall_temp2[i][j] = c_wall * dt/(dl**2) * (dd_temp) + wall_temp1[i][j]
    wall_temp1 = np.copy(wall_temp2)

    #Air
    temp2 = setup_gradient_air()

    power_of_cooling = 20
    for i in range(5,17):
        for j in range(10,22):
            temp1[j][i][0] -= power_of_cooling

    for z in range(1,z_size-1):
        for y in range(1,y_size-1):
            for x in range(1,x_size-1):
                dd_temp_y = (temp1[z][y+1][x])+(temp1[z][y-1][x])-2*(temp1[z][y][x])
                dd_temp_z = (temp1[z+1][y][x])+(temp1[z-1][y][x])-2*(temp1[z][y][x])
                if 5 <= y <= 16:
                    dd_temp_x = int(0.2*(temp1[z][y][x+1])+1.8*(temp1[z][y][x-1])-2*(temp1[z][y][x]))
                    temp2[z][y][x] = c_air * dt/(dl**2) * (3*dd_temp_x+dd_temp_y+dd_temp_z) + temp1[z][y][x]
                else:
                    dd_temp_x = (temp1[z][y][x+1])+(temp1[z][y][x-1])-2*(temp1[z][y][x])
                    temp2[z][y][x] = c_air * dt/(dl**2) * (dd_temp_x+dd_temp_y+dd_temp_z) + temp1[z][y][x]

    temp1 = temp2.copy()

    wall1.set_array([wall_temp1[0]])
    wall2.set_array([wall_temp1[1]])
    wall3.set_array([wall_temp1[2]])
    wall4.set_array([wall_temp1[3]])
    wall5.set_array([wall_temp1[4]])
    room.set_array(temp1[17])
    axis2.set_title(f"t = {t}")
    plt.pause(0.0001)
plt.show()