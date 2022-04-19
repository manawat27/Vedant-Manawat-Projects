# Name: Vedant Manawat
# VNum: V00904582
# CSC 305 Assignment 3

import sys
import array
import numpy as np
import math


""" Defining some global variables to help keep track of information to use later. """
near,left,right,bottom,top = 0,0,0,0,0
ambient,back,res = (),[],[]
sphere,light = [],[]

ray_origin = np.array([0,0,0])
colors = []
recur = 0

"""
    This function will read the input .txt file and seprate the data into the lists/tuples/integer variables so that we have 
    the respective data to render the scene. 
"""
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

""" A simple function used to normalize a vector (I wrote this in hopes to cut down the time it takes to run the file). """
def normalize(ray):
    sum = 0
    for item in ray:
        sum += math.pow(item,2)
    
    norm = math.sqrt(sum)
    normed_ray = ray/norm

    return normed_ray

"""
    A function to solve the quadratic equan with the given ray origin and direction to find whether or not there is an 
    intersection and to find what the hit point is which is be used later. 
"""
def solve_quad(S,C):

    a = np.dot(C,C)
    b = 2*np.dot(S,C)
    c = (np.dot(S,S)) - 1
    dis = (math.pow(b,2)) - (4*a*c)

    if (dis >= 0):
        t1 = -(b/a) + ((math.sqrt(dis))/a)
        th = -(b/a) - ((math.sqrt(dis))/a)
        min_t = min(t1,th)

        if(min_t > 0.00001):
            hit = 1
            return min_t,hit
        else:
            return None,None

    return None,None

"""
    Function to compute the diffused color of that pixel based on the intersection of the ray created from intersection point
    to the light source. This function returns the individual component of a pixel (for example only either R,G or B based on
    what is passed into the function when it is called). 
"""
def get_diffuse_color(Kd,intensity,normal,L,obj_color):

    dot_product = np.dot(normal,L)
    if (dot_product < 0):
        intensity = 0

    diffuse_color = Kd*intensity*dot_product*obj_color
    
    return diffuse_color


"""
    Function to compute the specular color of that pixel based on the intersection of the ray created from the intersection point
    to the light source. This function returns the specular value that is to be added onto the final color of the pixel. 
"""
def get_spec(Ks,intensity,normal,L,v,n):
    r_temp = 2 * (np.dot(normal,L)) * normal - L
    r = normalize(r_temp)

    v_temp = v[:3]
    v_new = normalize(v_temp)
    r_dot_v = math.pow(np.dot(r,v_new),n)

    if (r_dot_v < 0):
        r_dot_v = 0
    elif (r_dot_v > 1):
        r_dot_v = 1

    spec_color = Ks * (intensity*255) * r_dot_v

    return spec_color

"""
    Function to calculate all the local illumination of the pixel. 
    This function calls the two functions in order to compute the ambient, diffused and specular effect on the object. 
    It will call the function for each and every light source in the scene as diffuse and specular are an addition 
    of all light sources. Before calling the functions it will find the ray from the intersection point to the light source.

    This function returns the color of the pixel after the three effects have been applied to it. 
"""
def illuminate(color,object,normal,intersecting_point,eye):
    diffuse_r,spec_r = 0,0
    diffuse_g,spec_g = 0,0
    diffuse_b,spec_b = 0,0

    new_eye = np.concatenate([eye,[1]])
    v = new_eye - intersecting_point

    for i in range(len(light)):
        Light = np.concatenate([light[i][1:4],[1]])
        l_point = Light - intersecting_point
        l_point_prev = l_point[:3]
        L_point = normalize(l_point_prev)

        diffuse_r += get_diffuse_color(sphere[object][11],light[i][4],normal,L_point,color[0])
        spec_r += get_spec(sphere[object][12],light[i][4],normal,L_point,v,sphere[object][14])
        diffuse_g += get_diffuse_color(sphere[object][11],light[i][5],normal,L_point,color[1])
        spec_g += get_spec(sphere[object][12],light[i][5],normal,L_point,v,sphere[object][14])
        diffuse_b += get_diffuse_color(sphere[object][11],light[i][6],normal,L_point,color[2])
        spec_b += get_spec(sphere[object][12],light[i][6],normal,L_point,v,sphere[object][14])

    new_color_r = color[0]*sphere[object][10]*ambient[0] + diffuse_r + spec_r
    new_color_g = color[1]*sphere[object][10]*ambient[1] + diffuse_g + spec_g
    new_color_b = color[2]*sphere[object][10]*ambient[2] + diffuse_b + spec_b
    color = (new_color_r,new_color_g,new_color_b)
    
    new_color = list(color)
    for item in new_color:
        if (item > 255):
            index = new_color.index(item)
            clamped = 255
            new_color[index] = clamped

    color = tuple(new_color)
    return color


"""
    This is the main function where the "Ray Tracing" happens, in this function the transformation matrix is applied and is 
    applied to the "ray" variable which is essentially the ray passing through an object in the scene. This function handles
    the normalizing of vectors using the normalize function and deals with homogenous/cartesian coordinates for vectors and 
    other points in the image plane. This function will returen the color of the object (with diffuse and specular) if and only
    if there is an intersection between the ray and the object. If there is no such intersection then the background color will
    be returned. 

    This function also recursively calls itself (3 times) to perform the reflection between the reflected ray and the transformed
    object. 

    This function calls the following functions:
        - slove_quad(): to find the closest intersection. 
        - normalize(): to normalize the passed in vector. 
        - illuminate(): to apply ambient, diffusion and speculuar to the object color. 
"""
def trace(ray,object,eye):
    global recur 
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

        point_of_intersection = new_ray_origin + new_ray*th
        point_of_intersection_mag = np.linalg.norm(point_of_intersection)
        eye_mag = np.linalg.norm(eye)
        
        if (point_of_intersection_mag < eye_mag):
            return back
        else:
            difference = point_of_intersection[:3] - sphere[object][1:4]
            difference = np.concatenate([difference,[1]])
            temp = np.matmul(M_inv,difference)
            normal_temp = np.matmul(M_inv_tran,temp)
            normal = normal_temp[:3]
            normal = normalize(normal)

            color_cr = (sphere[object][7]*255,sphere[object][8]*255,sphere[object][9]*255)
            color = illuminate(color_cr,object,normal,point_of_intersection,eye)

            ray_re_dir = -2 * np.dot(normal,ray) * normal + ray

            if recur < 3:
                color_re = trace(ray_re_dir,object,eye)
                color_ref = (sphere[object][13]*color_re[0],sphere[object][13]*color_re[1],sphere[object][13]*color_re[2])
                recur = recur + 1
                return (color[0]+color_ref[0],color[1]+color_ref[1],color[2]+color_ref[2])
            else:
                return color
    return back

"""
    This is essentially the "main()" function. It sets up the initial vectors and the width and height of the ppm file. 
    Initially the image will be the background color and will change after we calculate the intersection and the pixel color. 
    This function will write to the ppm from left to right, bottom to top as and when it recieves a color from the trace function. 
"""
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
            ray = eye + P_cr_worldCoord
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


"""
    A main function needed by python, but this function will call the functions:
        - parse_files()
        - write_to_ppm()
"""
def main():
    outfile = parse_files()
    write_to_ppm(outfile)

if __name__ == "__main__":
    main()
