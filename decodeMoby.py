import numpy as np
import matplotlib.pylab as plt
from PIL import Image

f = open('mobydick.txt','r')
blah = f.read()


codes = []

conv = {8301:5,8298:2,8302:6,8300:4,8299:3,8204:1,8203:0,8303:7,8206:8}

i = 1
tempstr = ''
while i < 50000000:
    try: 
        tempstr += str(conv[ord(unicode(blah[i:i+3],'utf-8'))])
        i += 3
    except UnicodeDecodeError:
        i +=1
        codes.append(int(tempstr))
        tempstr = ''
    except TypeError:
        break

def hex_to_rgb(value):
    value = value.lstrip('0x')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def num_there(s):
    return any(i=='8' for i in s)

def oct_to_deci(value):
    lv = len(value)
    temp = 0
    for i in range(0,lv):
        temp += int(value[i]) * 8 ** (lv-i-1)
    return temp

# Convert saved array of octal code to hex to RGB
img2b = np.zeros((2448,3264,3))
#notes to fix code:
''' every time encounter length 15 stretch, skip them and start a new line. read out x's first (so need to switch i and j) why are there zeros everywhere'''

k = 0 
for i in range(0,1264):
    for j in range(0,1224): #len(codes)):
        if not num_there(str(codes[k])):
            if len(str(codes[k])) == 16:
                rgb1 = hex_to_rgb(hex(oct_to_deci(str(codes[k])[0:8])))
                rgb2 = hex_to_rgb(hex(oct_to_deci(str(codes[k])[8:16])))
                img2b[2*j,i] = rgb1
                img2b[2*j+1,i] = rgb2
            else:
                print k
        k+=1


# Take array and make an RGB picture
img = Image.fromarray(img2b, 'RGB')
img.save('decodeMoby.png')

