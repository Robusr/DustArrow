import re
r = r"X(.+)Y(.+)GX(.+)GY(.+)GZ(.+)"
m = re.findall(r,"X5.9Y-1.2GX-0.20GY1.75GZ1.74")
for i in m:
    Gyrox = i[0]
    Gyroy = i[1]
    Gx = i[2]
    Gy = i[3]
    Gz = i[4]
print(Gz)
