import cv2

image = cv2.imread("variant-10.jpg")

if image is None:
    print("Error: Image not found")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold filtering (threshold=150)
_, thresholded = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

cv2.imshow("Threshold Filtering (150)", thresholded)
cv2.waitKey(0)
cv2.destroyAllWindows()
