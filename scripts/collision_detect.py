"""
    collision detect
    input: obstacles' vertex coordinates, list vertex_list[]
"""

def collision_detect(vertexs, point1, point2):
    positive_flag = 0
    negative_flag = 0
    step_b = False
    # line function
    line = lambda x1, y1, x2, y2, x, y: (y2-y1)*x + (x1-x2)*y + (x2*y1 - x1*y2)
    for vertex in vertexs:
        if line(point1[0], point1[1],point2[0], point2[1], vertex[0], vertex[1]) == 0:
            step_b = True
            break
        elif line(point1[0], point1[1],point2[0], point2[1], vertex[0], vertex[1]) < 0:
            negative_flag += 1
        else:
            positive_flag += 1
    if step_b or (not step_b and (positive_flag * negative_flag) != 0):
        max_x = 0.0
        max_y = 0.0
        min_x = 100.0 
        min_y = 100.0
        for vertex in vertexs:
            max_x = max(max_x, vertex[0])
            min_x = min(min_x, vertex[0])
            max_y = max(max_y, vertex[1])
            min_y = min(min_y, vertex[1])
        if (point1[0] > max_x and point2[0] > max_x) or \
            (point1[0] < min_x and point2[0] < min_x) or \
            (point1[1] > max_y and point2[1] > max_y) or \
            (point1[1] < min_y and point2[1] < min_y):
            return False
        else:
            return True
    else:
        return False