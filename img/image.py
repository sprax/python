'''image processing with PIL'''
# ArrayAlgo.py from ArrayAlgo.java       Author: Sprax LInes   2011.11

import numpy as np
import scipy as sp
import matplotlib.pyplot as mpp
# import Image as im

from PIL import Image as pm

#px = Image.open('image/tt.jpg')
# from PIL import Image
#print(Image.dir())
imt = pm.open("TaranakiA.jpg")
#im.rotate(45).show()
img = imt.convert('L')      # convert to grayscale
ima = np.asarray(img)
imb = np.fft.rfft2(ima)
imc = np.fft.irfft2(imb)
imd = pm.fromarray(imc.astype(np.uint8))
#imd.show("inverse")

imba = np.real(imb)

ime = pm.fromarray(imba.astype(np.uint8))
ime.show("forward")


a = np.arange(100)
b = np.arange(100)
c = a + b
for j in range(20):
    print(j, "\t", c[j])

a = np.zeros(1000)
a[:100] = 1
b = sp.fft(a)
mpp.plot(a)
