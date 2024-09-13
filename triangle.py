import matplotlib.pyplot as plt 
from random import randint, uniform
from math import sqrt, acos, pi, atan2
from datetime import datetime

########### Convex Hull calculation ################

def is_counter_clockwise_orientation(prev_point, point, next_point):
    '''Check if orientation is counter clockwise and return True if this is the case.'''
    result = (next_point[1] - point[1])*(point[0] - prev_point[0]) - (point[1] - prev_point[1])*(next_point[0] - point[0])

    if result > 0:
        return True
    
    return False


def get_convex_hull_points(points: list):
    # expected input is list of lists with coordinates ex. [[1,2],[4,5]] and response is either [] if there is no convex hull, or set with all points

    #1. sort by y coordinate 
    sorted_points = sorted(points, key=lambda point: point[1])
    
    min_point = sorted_points[0]
    remaining_points = points[1:]
    remaining_points_sorited = sorted(remaining_points, key=lambda point: atan2(point[1],point[0]))

    #print(sorted_points, "\nmin: ", min_point)    

    crnt_counter = 2
    convex_list = list()
    convex_list.append(min_point)
    convex_list.append(remaining_points_sorited[0])

    for crnt_point in remaining_points_sorited[1:]:
        if not is_counter_clockwise_orientation(convex_list[crnt_counter-2], convex_list[crnt_counter-1], crnt_point):
            return [] 
        else:
            convex_list.append(crnt_point)
            crnt_counter += 1
    
    return convex_list

#############################################################


#################### Main part ###################### 
def run(a,b,c):
    '''Run program: 
        1. Create triangle by the input points
        2. Generate random number of points inside triangle that form convex hull
        3. Draw the convex hull '''

    xmin, xmax, ymin, ymax = -5, 5, -5, 5

    ax = plt.subplot(1,1,1)
    colors = ['m', 'g', 'r']
    ax.scatter([a[0],b[0],c[0]], [a[1],b[1],c[1]], c=colors)

    ax.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')

    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

    arrow_fmt = dict(markersize=4, color='black', clip_on=False)
    ax.plot((1), (0), marker='>', transform=ax.get_yaxis_transform(), **arrow_fmt)
    ax.plot((0), (1), marker='^', transform=ax.get_xaxis_transform(), **arrow_fmt)

    # Debug strange triangles
    # t1 = [0.5023541122695032, 0.3914120681796405]
    # t2 = [1.1441142492497727, 1.0168469380221348]
    # t3 = [1.8269627838739504, 1.7872708867598366]
    # ax.scatter([t1[0],t2[0],t3[0]], [t1[1],t2[1],t3[1]], c=colors)
    # draw_triangle_by_three_points_and_plot(t1,t2,t3,ax)
    # ax.fill([t1[0],t2[0],t3[0]], [t1[1],t2[1],t3[1]])
    # plt.show()
    # return    

    # ax.plot([a[0], b[0]], [b[1],a[1]])
    # ax.plot([b[0], c[0]], [b[1],c[1]])
    # ax.plot([c[0], a[0]], [c[1],a[1]])
    draw_triangle_by_three_points_and_plot(a,b,c,ax)


    points = []
    points_x = []
    points_y = []

    points_count = randint(3,10)
    print('Total points: ', points_count)
    total_attempts = 0

    while True:
        total_attempts_exceeded = False 
        for i in range (0, points_count):
            found_point = False    
            while not found_point:
                np_x = uniform(min(a[0],b[0],c[0]),max(a[0],b[0],c[0]))
                np_y = uniform(min(a[1],b[1],c[1]),max(a[1],b[1],c[1]))
                total_attempts += 1

                if total_attempts > 100:
                   points = []
                   total_attempts = 0
                   total_attempts_exceeded = True
                   break
                
                if check_if_point_is_Inside_triangle(a,b,c,[np_x, np_y]):
                    found_point = True
                    points.append([np_x, np_y])
                
                    if i >= 2:
                        result = get_convex_hull_points(points=points)
                        if len(result) == 0:
                            points.pop(i)
                            found_point = False 
                        # else: 
                            # ax.scatter(np_x, np_y)

                    # else: 
                        # ax.scatter(np_x, np_y)

            if total_attempts_exceeded:
                break
        if not total_attempts_exceeded:
            break

    for point in result:
        points_x.append(point[0])
        points_y.append(point[1])
        ax.scatter(point[0], point[1])
        print('Final point: [', point[0], point[1], ']')

    ax.fill(points_x, points_y)
    plt.savefig('plot_' + str(datetime.now()) + '.jpg')
    plt.show()


def draw_triangle_by_three_points_and_plot(point1, point2, point3, plotter):
    plotter.plot([point1[0], point2[0]], [point2[1],point1[1]])
    plotter.plot([point2[0], point3[0]], [point2[1],point3[1]])
    plotter.plot([point3[0], point1[0]], [point3[1],point1[1]])




def calc_triangle_area(a, b, c):
    area = abs((a[0]*(b[1] - c[1]) + b[0]*(c[1] - a[1]) + c[0]*(a[1] - b[1]))/2.0)

    return area


def check_if_point_is_Inside_triangle(a,b,c,p):
    tolerance = 0.0001 
    main_tr_area = calc_triangle_area(a,b,c)
    pab_tr_area = calc_triangle_area(p,a,b)
    pbc_tr_area = calc_triangle_area(p,b,c)
    pac_tr_area = calc_triangle_area(p,a,c)

    #print(main_tr_area, pab_tr_area + pbc_tr_area + pac_tr_area,  main_tr_area == pab_tr_area + pbc_tr_area + pac_tr_area)

    if main_tr_area > pab_tr_area + pbc_tr_area + pac_tr_area - tolerance and main_tr_area < pab_tr_area + pbc_tr_area + pac_tr_area + tolerance:
        return True
    return False


if __name__ == '__main__':
    angle_a = eval(input('enter first angle '))
    angle_b = eval(input('enter second angle '))
    angle_c = eval(input('enter third angle '))

# angle_a = [0,0]
# angle_b = [6,0]
# angle_c = [3,5.19]

    run(angle_a, angle_b, angle_c)


###################### Not used ##############################
#def check_all_angles_in_figure_below_180(points:list, verbose=False) -> bool:
#     stored_angles = {}
#     for point in points:
#         for another_point in points: 
#             if point == another_point:
#                 continue
#             for third_point in points:

#                 if third_point == point or third_point == another_point: 
#                     continue

#                 combo = []
#                 combo.append(frozenset(point))
#                 combo.append(frozenset(another_point))
#                 combo.append(frozenset(third_point))
#                 combo.sort()
#                 combination_tuple = tuple(combo)
#                 #print(combination_tuple,type(combination_tuple))

#                 if combination_tuple in stored_angles:
#                     continue

#                 current_angle = get_angle_between_points(point, another_point, third_point)
#                 if  current_angle >= 180 or current_angle <= 0:
#                     return False
                
#                 stored_angles[combination_tuple] = current_angle
#     if verbose: 
#         print('Result: ', True, '\nDetails: ', stored_angles)
#     return True


# def get_random_point(a, b, c):
#     np_x = random(min(a[0],b[0],c[0]),max(a[0],b[0],c[0]))
#     np_y = random(min(a[1],b[1],c[1]),max(a[1],b[1],c[1]))

#     print(np_x, np_y, check_if_point_is_Inside_triangle(a,b,c, [np_x, np_y]))


# def get_angle_between_points(a,b,c):
#     ab_len = sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
#     ac_len = sqrt((a[0] - c[0])**2 + (a[1] - c[1])**2)
#     bc_len = sqrt((b[0] - c[0])**2 + (b[1] - c[1])**2)

#     #print('arcos', (ab_len**2 + ac_len**2 - bc_len**2)/(2*ab_len*ac_len))
#     # if acos((ab_len**2 + ac_len**2 - bc_len**2)/(2*ab_len*ac_len)) < 0:
#     #     return 360
#     angle = acos((ab_len**2 + ac_len**2 - bc_len**2)/(2*ab_len*ac_len)) * (180 / pi)
#     return angle

#######################################################################

# test points:
# Final point: [ 0.5023541122695032 0.3914120681796405 ]
# Final point: [ 1.1441142492497727 1.0168469380221348 ]
# Final point: [ 1.8269627838739504 1.7872708867598366 ]
# Final point: [ 3.1637905118307543 3.303461011674295 ]
# Final point: [ 3.677000200175391 3.9304988990079615 ]
# Final point: [ 2.2708778052815815 2.6756678197157653 ]