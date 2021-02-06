import numpy as np
import math
import cv2
EPS = 1e-10


# 逆时针旋转
# 弧度
def rotate_poly(poly: np.array, rad):
    N, d = poly.shape
    if N < 3 or d != 2:
        raise ValueError

    # center_point = np.asarray([0., 0.])
    # matrix = np.asarray([[math.cos(rad), math.sin(rad)],
    #                      [-math.sin(rad), math.cos(rad)]])
    # new_poly = np.dot((poly - center_point), matrix) + center_point

    matrix = np.asarray([[math.cos(rad), math.sin(rad)],
                         [-math.sin(rad), math.cos(rad)]])
    new_poly = np.dot((poly), matrix)
    return new_poly


# shape of min_rect: [4, 2]
def min_rect(poly: np.array):
    x_min, y_min = np.min(poly, axis=0)
    x_max, y_max = np.max(poly, axis=0)
    min_rect = np.asarray([[x_min, y_min],
                           [x_max, y_min],
                           [x_max, y_max],
                           [x_min, y_max]])
    area = (x_max - x_min) * (y_max - y_min)
    return min_rect, area


def get_rad(poly: np.array):
    N, d = poly.shape
    if N < 3 or d != 2:
        raise ValueError

    rad = []
    for i in range(N):
        vector = poly[i-1] - poly[i]
        rad.append(math.atan(vector[1] / (vector[0]+EPS)))
    return rad


# shape of rect_min: [4, 2]
def min_rotate_rect(poly: np.array):
    rect_min, area_min = min_rect(poly)
    rad_min = 0.
    rad = get_rad(poly)
    for r in rad:
        new_poly = rotate_poly(poly, -r)
        rect, area = min_rect(new_poly)
        if area < area_min:
            rect_min, area_min, rad_min = rect, area, r
    min_rect_r = rotate_poly(rect_min, rad_min)
    return min_rect_r, area_min
    #return rect_min, area_min

def get_pic(poly, index):
    #print(poly)

    min_rect_r, area_min = min_rotate_rect(poly)
    print(index, area_min)

def read_file():
    f = open("d:\\code\\data.txt")
    line = f.readline()
    data = {}
    lastArea = ""
    index = 0
    poly = []
    while line:
        line = line.replace("\n", "").replace("\t", " ")
        splits = line.split(" ")
        area = splits[0]
        index = int(splits[1])
        if data.__contains__(area) == False:
            if lastArea != "":
                #print(data[lastArea])
                polyData = np.array(data[lastArea], np.float64)
                get_pic(polyData, (index - 1))
            data[area] = []
            lastArea = area
        
        x = float(splits[2])
        y = float(splits[3])
        data[area].append([x, y])
        line = f.readline()
    #print("area:", lastArea, ", index: ", index)
    polyData = np.array(data[lastArea], np.float64)
    get_pic(polyData, index)
    #print(data)
    f.close()
            

if __name__ == "__main__":
    #在这里输入多边形顶点坐标
    #poly = np.array([[37436420.3209, 37436420.3209], [37436419.5221, 37436419.5221], 
    #[37436433.4053, 37436433.4053], [37436434.9173, 37436434.9173], [37436431.9823, 37436431.9823],
    #[37436420.4579,37436420.4579],[37436420.3209,37436420.3209]], np.int32)
    #get_pic(poly)
    read_file()
