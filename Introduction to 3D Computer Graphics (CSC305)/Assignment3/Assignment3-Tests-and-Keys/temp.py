# Name: Vedant Manawat
# VNum: V00904582
# CSC 305 Assignment 3

import sys
import array
import numpy as np
import math

from numpy.lib.function_base import diff
from numpy.ma.core import dot

near,left,right,bottom,top = 0,0,0,0,0
ambient,back,res = (),[],[]
sphere,light = [],[]

ray_origin = np.array([0,0,0])
colors = []

def parse_files():
    filename = sys.argv[1]
    f = open(filename,"r")

    lines = f.read().splitlines()
    lines = list(filter(lambda x: x != "",lines))

    for item in lines:
        if "NEAR" in item:
            val = item.split()
            global near 
            near = float(val[1])
        elif "LEFT" in item:
            val = item.split()
            global left 
            left = float(val[1])
        elif "RIGHT" in item:
            val = item.split()
            global right 
            right = float(val[1])
        elif "BOTTOM" in item:
            val = item.split()
            global bottom 
            bottom = float(val[1])
        elif "TOP" in item:
            val = item.split()
            global top 
            top = float(val[1])
        elif "OUTPUT" in item:
            val = item.split()
            outfile = val[1]
        elif "AMBIENT" in item:
            val = item.split()
            global ambient 
            ambient = (float(val[1]),float(val[2]),float(val[3]))
        elif "BACK" in item:
            val = item.split()
            global back 
            back = ((int(val[1])*255),(int(val[2])*255),(int(val[3])*255))
        elif "RES" in item:
            val = item.split()
            global res 
            res.append(val[1])
            res.append(val[2])
        elif "SPHERE" in item:
            val = item.split()
            n = int(val[-1])
            float_list = tuple(map(float,val[2:-1]))
            tup = (val[1],) + float_list + (n,)
            sphere.append(tup)
        elif "LIGHT" in item:
            val = item.split()
            pos = tuple(map(float,val[2:5]))
            inten = tuple(map(float,val[5:]))
            tup = (val[1],) + pos + inten
            light.append(tup)
    
    f.close()

    return outfile

def normalize(ray):
    sum = 0
    for item in ray:
        sum += math.pow(item,2)
    
    norm = math.sqrt(sum)
    normed_ray = ray/norm

    return normed_ray

def solve_quad(S,C):
    a = np.dot(C,C)
    b = 2*np.dot(S,C)
    c = (np.dot(S,S)) - 1
    dis = (math.pow(b,2)) - (4*a*c)

    if (dis >= 0):
        t1 = -(b/a) + ((math.sqrt(dis))/a)
        th = -(b/a) - ((math.sqrt(dis))/a)
        hit = 1
        return min(t1,th),hit

    return 0,None

def get_diffuse(Kd,intensity,color,N,L):
    dot_pro = np.dot(N,L)
    if (dot_pro < 0):
        intensity = 0
    diff_color = Kd * intensity * dot_pro * color

    return diff_color

def get_spec(Ks,intensity,normal,L,v,n):
    r_temp1 = 2*(np.dot(normal,L))
    r_temp2 = r_temp1 * n
    r_temp = r_temp2 - L
    dot_rv = np.dot(r_temp,v)
    dot_pro = math.pow(dot_rv,n)
    spec_color = Ks * intensity * dot_pro

    return spec_color

def illuminate(color,object,normal,intersection,eye):
    diffuse_r,diffuse_g,diffuse_b,specular_r,specular_g,specular_b = 0,0,0,0,0,0
    intermediate_intersection = np.delete(intersection,-1)
    v = eye - intermediate_intersection
    for i in range(len(light)):
        Light = np.concatenate([light[i][1:4],[1]])
        l_point = Light - intersection 
        l_point = np.delete(l_point,-1)
        L_point = normalize(l_point)

        cart_intersection = np.delete(intersection,-1)
        th,hit = solve_quad(cart_intersection,L_point)

        diffuse_r += get_diffuse(sphere[object][11],light[i][4],color[0],normal,L_point)
        specular_r += get_spec(sphere[object][12],light[i][4],normal,L_point,v,sphere[object][14])
        diffuse_g += get_diffuse(sphere[object][11],light[i][5],color[1],normal,L_point)
        specular_g += get_spec(sphere[object][12],light[i][5],normal,L_point,v,sphere[object][14])
        diffuse_b += get_diffuse(sphere[object][11],light[i][6],color[2],normal,L_point)
        specular_b += get_spec(sphere[object][12],light[i][6],normal,L_point,v,sphere[object][14])
   
    new_color_r = color[0]*sphere[object][10]*ambient[0] + diffuse_r + specular_r
    new_color_g = color[1]*sphere[object][10]*ambient[1] + diffuse_g + specular_g
    new_color_b = color[2]*sphere[object][10]*ambient[2] + diffuse_b + specular_b

    color = (new_color_r,new_color_g,new_color_b)
    new_color = list(color)

    for i in range(len(new_color)):
        if new_color[i] > 255:
            clamped = 255
            new_color[i] = clamped
    
    color = tuple(new_color)
    
    return color

def trace(ray,object,eye):
    new_ray_origin = np.concatenate([ray_origin,[1]])
    new_ray = np.concatenate([ray,[0]])

    translation = np.array([[1,0,0,sphere[object][1]],[0,1,0,sphere[object][2]],[0,0,1,sphere[object][3]],[0,0,0,1]])
    scale = np.array([[sphere[object][4],0,0,0],[0,sphere[object][5],0,0],[0,0,sphere[object][6],0],[0,0,0,1]])
    
    Mat = np.matmul(translation,scale)
    M_inv = np.linalg.inv(Mat)
    M_inv_tran = np.transpose(M_inv)

    S_double_prime = np.matmul(M_inv,new_ray_origin)
    c_double_prime = np.matmul(M_inv,new_ray)

    s_prime = np.delete(S_double_prime,-1)
    c_prime = np.delete(c_double_prime,-1)

    th,intersection = solve_quad(s_prime,c_prime)
    
    if (intersection and not None):

        point_of_intersection = s_prime + c_prime*th
        point_of_intersection = np.concatenate([point_of_intersection,[1]])

        temp = np.matmul(M_inv_tran,M_inv)
        normal_temp = np.matmul(temp,point_of_intersection)
        normal_temp = np.delete(normal_temp,-1)
        normal = normalize(normal_temp)

        color_cr = (sphere[object][7]*255,sphere[object][8]*255,sphere[object][9]*255)
        color = illuminate(color_cr,object,normal,point_of_intersection,eye)
        return color
    
    return back

def write_to_ppm(outfile):

    u = np.array([1,0,0])
    v = np.array([0,1,0])
    n = np.array([0,0,1])
    eye = np.array([0,0,0])
    width = int(int(res[0]))
    height = int(int(res[1]))

    f = open(outfile,"wb")
    header = 'P6 ' + str(width) + ' ' + str(height) + ' ' + str(255) + '\n'
    image = array.array('B', back * width * height)

    k=0
    for row in range(width):
        for col in range(height):
            P_cr_worldCoord = (-near*n) + left*((2*col/width)-1)*u + top*((2*row/height)-1)*v
            ray = P_cr_worldCoord - eye
            normalized_ray = normalize(ray)
            for object in range(len(sphere)):
                color_cr = trace(normalized_ray,object,eye)
                if (image[-k] == back[0] and image[-k+1] == back[0] and image[-k+1] == back[0]):
                    image[-k] = (int(color_cr[0]))
                    image[-k + 1] = (int(color_cr[1]))
                    image[-k + 2] = (int(color_cr[2]))
            k = k + 3

    with open(outfile, 'wb') as f:
        f.write(bytearray(header, 'ascii'))
        image.tofile(f)
    f.close()
        
def main():
    outfile = parse_files()
    write_to_ppm(outfile)

if __name__ == "__main__":
    main()
