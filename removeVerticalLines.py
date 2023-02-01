import cv2
import numpy as np

def removeLines(img):
	w=img.shape[0]
	h=img.shape[1]
	for i in range(w):
		for j in range(h):
			(b,g,r) = img[i][j]
			if (b,r,g) == (128,128,128):
				img[i][j] = (255,255,255)
	return img
img=cv2.imread("./images/sinus.png")
image=removeLines(img)
cv2.imwrite("./images/sinus.png",image)