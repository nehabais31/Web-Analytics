import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread(r'E:\Neha\Course_Materials\Fall2020\Web Analytics\Assignment-4\image_3.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread(r'E:\Neha\Course_Materials\Fall2020\Web Analytics\Assignment-4\Bug.png',0)

height, width = template.shape[::]

res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF)
plt.imshow(res, cmap='gray')

min_val, max_val, min_locc, max_loc = cv2.minMaxLoc(res)

top_leftt = min_locc  #Change to max_loc for all except for TM_SQDIFF
bottom_right = (top_leftt[0] + width, top_leftt[1] + height)
cv2.rectangle(img_rgb, top_leftt, bottom_right, (255, 0, 0), 2) 

#cv2.imwrite(r'E:\Neha\Course_Materials\Fall2020\Web Analytics\Assignment-4\Bug_found3.png',img_rgb)
#cv2.waitKey()
#cv2.destroyAllWindows()    
#c