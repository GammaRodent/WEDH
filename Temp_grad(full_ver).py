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

time = np.linspace(0,1000,1000)
x_intensity = np.zeros(1000)
y_intensity = np.zeros(1000)
z_intensity = np.zeros(1000)

for t in range(720):
    x,y,z = sun_intensity(0,1000,t,1380,np.pi/6)
    x_intensity[t] = abs(x)
    y_intensity[t] = y
    z_intensity[t] = z

#Declare Variable
dl = 0.1
dt = 0.0001
c = 0.466
time = 1000
normal_temp = 150
x_size = 20
y_size = 20
z_size = 20
ambient =25
a = 1 #solar radiation absorptivity
h = 1 #convection,radiation heat transfer coefficient
temp_x_neg = 25
temp_y_neg = 25
temp_z_neg = 25

def define_gradient():
    temp_grad = [[[normal_temp for _ in range(x_size)] for _ in range(y_size)] for _ in range(z_size)]

    #XY-plane wall
    for i in range(y_size):
        for j in range(x_size):
            temp_grad[0][i][j] = ambient + a*z_intensity/h

    #XZ wall
    for i in range(z_size):
        for j in range(x_size):
            temp_grad[i][0][j] = ambient + a*y_intensity/h

    #YZ wall
    for i in range(z_size):
        for j in range(y_size):
            temp_grad[i][j][0] = ambient + a*x_intensity/h

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

    #setting the outer wall to temperature dependent of sun intensity
    #x-wall
    for i in range(y_size):
        for j in range(x_size):
            temp_grad[0][i][j] = ambient + a*x_intensity[t]/h
    #y-wall
    
    #z-wall
    
    
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