import cv2
import matplotlib.pyplot as plt

plt.style.use('seaborn')

image = cv2.imread("UI.jpeg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(8,8))
plt.imshow(image)
plt.axis("off")
plt.title("Original Image")
plt.show()

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.figure(figsize=(8,8))
plt.imshow(image_gray,cmap="gray")
plt.axis("off")
plt.title("Grayscale Image")
plt.show()

image_invert = cv2.bitwise_not(image_gray)
plt.figure(figsize=(8,8))
plt.imshow(image_invert,cmap="gray")
plt.axis("off")
plt.title("Grayscale Image")
plt.show()

image_smoothing = cv2.GaussianBlur(image_invert, (21, 21),sigmaX=0, sigmaY=0)
plt.figure(figsize=(8,8))
plt.imshow(image_smoothing,cmap="gray")
plt.axis("off")
plt.title("Smoothen Image")
plt.show()

final = cv2.divide(image_gray,255-image_smoothing,scale=255)
plt.figure(figsize=(8,8))
plt.imshow(final,cmap="gray")
plt.axis("off")
plt.title("Final Sketch Image")
plt.show()
