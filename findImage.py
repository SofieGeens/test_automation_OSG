from python_imagesearch.imagesearch import imagesearch

def findImage(img):
    x,y = imagesearch(img,precision = 0.7)
    if x != -1:
        return True
    else:
        return False