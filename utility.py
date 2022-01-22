import cv2

def show_image(img, resize=None):
    if resize is not None:
        img = cv2.resize(img, (round(img.shape[1] / resize), round(img.shape[0] / resize)))
    cv2.imshow('image', img)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()
