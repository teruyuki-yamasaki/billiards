import os 
import numpy as np 
from PIL import Image

color_list = ['yellow', 'blue', 'red', 'pink', 'orange', 'green', 'brown', 'black']

color_dict = {
    'yellow': [1, 1, 0, 1],
    'blue': [0, 0, 0.8, 1], 
    'red': [1, 0, 0, 1], 
    'pink': [1, 0.75, 0.79, 1], 
    'orange': [0.97, 0.58, 0.02, 1],
    'green': [0.25, 0.76, 0.50, 1], 
    'brown': [0.63, 0.32, 0.18, 1], 
    'black': [0, 0, 0, 1]
}

digit_dict = {
    0: [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
    1: [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
    2: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
    3: [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    4: [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
    5: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
    6: [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    7: [[1, 1, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1]],
    8: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
    9: [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]
}

H = 256
W = 256

h = 5 
w = 5

Mh = 10
Mw = 6 

dtype = np.uint8

black = np.array([0, 0, 0, 1], dtype=dtype)*255
white = np.array([1, 1, 1, 1], dtype=dtype)*255

def get_digit(num):
    array = np.ones((h, w, 4), dtype=dtype)*255

    digit = np.array(digit_dict[int(num)%10], dtype=dtype)

    if num < 10:
        for i in range(h):
            for j in range(3):
                array[i][j+1][:] = black if digit[i][j]==1 else white
    
    if num >= 10:
        for i in range(h):
            array[i][0][:] = black
            for j in range(3):
                array[i][j+2][:] = black if digit[i][j]==1 else white

    return array

def enlarge(digit, Mh, Mw):
    array = np.ones((len(digit)*Mh, len(digit[0])*Mw, 4), dtype=dtype)*255

    for i in range(len(digit)):
        for j in range(len(digit[0])):

            for I in range(i*Mh, (i+1)*Mh):
                for J in range(j*Mw, (j+1)*Mw):
                    array[I][J][:] = digit[i][j][:]

    return array 

def put_digit(num, array):    
    # white base 
    for i in range(-1*Mh, (h+1)*Mh):
        for j in range(-1*Mw, (w+1)*Mw):
            array[int(H/2)-int(Mh*h/2)+i][int(W/2)-int(Mw*w/2)+j][:] = white 

    # digit 
    digit = get_digit(num)
    digit = enlarge(digit, Mh, Mw)
    for i in range(h*Mh):
        for j in range(w*Mw):
            array[int(H/2)-int(Mh*h/2)+i][int(W/2)-int(Mw*w/2)+j][:] = digit[i][j][:]
    
    return array 

def get_solid(color_name): 
    color = np.array([int(_*255) for _ in color_dict[color_name]], dtype=dtype)

    array = np.ones((H, W, 4), dtype=dtype)*255

    for i in range(H):
        for j in range(W):
            array[i][j][:] = color

    return array 

def get_stripe(color_name):
    color = np.array([int(_*255) for _ in color_dict[color_name]], dtype=dtype)

    array = np.ones((H, W, 4), dtype=dtype)*255
    
    for i in range(int(2*H/7), int(5*H/7)):
        for j in range(W):
            array[i][j][:] = color

    return array 

def main():
    for i in range(15):
        if i <= 7:
            array = get_solid(color_list[i])
        else:
            array = get_stripe(color_list[i%8]) 

        array = put_digit(i+1, array) 

        img = Image.fromarray(array, 'RGBA') 

        img_name = 'color_{}.png'.format(str(i+1))
        img.save('./assets/'+img_name)

if __name__=='__main__':
    main() 