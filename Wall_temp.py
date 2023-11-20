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

for t in range(1000):
    x,y,z = sun_intensity(0,1000,t,1380,np.pi/6)
    x_intensity[t] = abs(x)
    y_intensity[t] = y
    z_intensity[t] = z

#Declare Variable
thickness = 0.1
dl = 0.01
dt = 0.0001
c = 0.466
time = 1000
normal_temp = 25
a = 0.5 #solar radiation absorptivity
h = 5 #convection,radiation heat transfer coefficient
temp_x_neg = normal_temp
temp_y_neg = normal_temp
temp_z_neg = normal_temp

#Parameter of the room
x_size = 20
y_size = 20
z_size = 20

## XY wall is the roof (0)
## YZ1 and YZ2 are the wall on the east and west (1,2)
## XZ1 and XZ2 are the wall on the north and south (3,4)

def setup_gradient_wall():
    temp_wall = [[normal_temp for _ in range(int(thickness/dl))] for _ in range(5)]
    return temp_wall
    
def setup_gradient_air():
    temp = [[[normal_temp for _ in range(x_size)] for _ in range(y_size)] for _ in range(z_size)]
    return temp

outside_temp = 30

temp1 = setup_gradient_wall()
temp1[0][0] = outside_temp
temp1[1][0] = outside_temp
temp1[2][0] = outside_temp
temp1[3][0] = outside_temp
temp1[4][0] = outside_temp

fig, axis = plt.subplots()

pcm = axis.pcolormesh([temp1[0]], cmap = plt.cm.jet, vmin = 0, vmax = 45)
plt.colorbar(pcm, ax=axis)

for t in range(time):
    temp2 = setup_gradient_wall()
    temp2[0][0] = 40
    temp2[1][0] = 40
    temp2[2][0] = 40
    temp2[3][0] = 40
    temp2[4][0] = 40

    temp1[0][1] = temp1[0][1] + 0.15*int(a*y_intensity[t]/h)
    temp1[1][1] = temp1[1][1] + 0.15*int(a*max(0,x_intensity[t])/h)
    temp1[2][1] = temp1[2][1] + 0.15*int(a*max(0,-1*x_intensity[t])/h)
    temp1[3][1] = temp1[3][1] + 0.15*int(a*max(0,z_intensity[t])/h)
    temp1[4][1] = temp1[4][1] + 0.15*int(a*max(0,z_intensity[t])/h)
    
    for i in range(5):
        for j in range(1,int(thickness/dl-1)):
            dd_temp = temp1[i][j+1]+temp1[i][j-1]-2*temp1[i][j]
            temp2[i][j] = c * dt/(dl**2) * (dd_temp) + temp1[i][j]
    temp1 = np.copy(temp2)
    print(temp1[0])
    pcm.set_array([temp1[0]])
    axis.set_title(f"t = {t}")
    plt.pause(0.01)
plt.show()