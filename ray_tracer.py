# module to implement ray tracing through sperical lenses (x-y plane)
# follow standard sign convention

import math
import sys

def trace(r1, r2, x_led, theta1):
    m1 = math.tan(math.radians(theta1)) #slope of input ray

    if x_led > 0:
        x_led = (-1)*x_led
    
    #assume lens place through origin and lens thickness as 2 mm
    th = 2 #correct the code in GUI part also
    x1 = r1 - (th/2)
    x2 = r2 + (th/2)
    print "***********************************************************"
    print "x1:", x1, "x2:", x2

    #calculation of intersection of ray and lens
    a = m1**2 + 1
    b = (-2)*(x_led*m1**2 + x1)
    c = x_led**2*m1**2 - r1**2 + x1**2

    if (b**2 - 4*a*c) < 0:
        print "**********************************************************\nRay doesnt intersect front surface!!"
        return -1, -1, -1, -1, -1, -1
        sys.exit()

    if r1 < 0:
        x_int = max(((-1)*b + math.sqrt(b**2 - 4*a*c))/(2*a), ((-1)*b - math.sqrt(b**2 - 4*a*c))/(2*a))
    else:
        x_int = min(((-1)*b + math.sqrt(b**2 - 4*a*c))/(2*a), ((-1)*b - math.sqrt(b**2 - 4*a*c))/(2*a))
 
    y_int = m1*(x_int - x_led)

    #calculation of slope of normal at 1st contact point
    m2 = (y_int - 0)/(x_int - x1)

    #for obtuse inclination
    if m2 < 0:
        err = math.pi
    else:
        err = 0
    print "slope of first normal:", (math.degrees(err + math.atan(m2)))

    #Refraction at first surface
    if r1 > 0:
        theta2 =  theta1 + math.fabs(math.degrees(math.atan(m2)))#angle of input ray with normal
    else:
        if x1 < x_led:
            theta2 = theta1 - math.degrees(err + math.atan(m2))
        else:
            theta2 = math.degrees(err + math.atan(m2)) - theta1

    print "Theta2:", theta2
    theta3 = math.degrees(math.asin((1/1.585)*math.sin(math.radians(theta2)))) #angle of refraction
    print "Theta3:", theta3

    #path of refracted ray
    if r1 > 0:
        m3 = math.tan(math.radians(theta3) - math.fabs(math.atan(m2)))
    if r1 < 0:
        if x_led < x1:
            m3 = math.tan(math.atan(m2) - math.radians(theta3))
        else:
            m3 = math.tan(math.atan(m2) + math.radians(theta3))
    print "slope of refracted ray:", (math.degrees(math.atan(m3)))

    #intersection of refracted ray and rear lens surface
    a = m3**2 + 1
    b = (2)*(y_int*m3 - m3**2*x_int - x2)
    c = y_int**2 + x2**2 - 2*y_int*m3*x_int + m3**2*x_int**2 - r2**2

    if (b**2 - 4*a*c) < 0:
        print "**********************************************************\nRay doesnt intersect rear surface!!"
        return x_int, y_int, -1, -1, m3, -1
        sys.exit()
    
    if r2 > 0:
        x_int2 = min(((-1)*b + math.sqrt(b**2 - 4*a*c))/(2*a), ((-1)*b - math.sqrt(b**2 - 4*a*c))/(2*a))
    else:
        x_int2 = max(((-1)*b + math.sqrt(b**2 - 4*a*c))/(2*a), ((-1)*b - math.sqrt(b**2 - 4*a*c))/(2*a))

    y_int2 = y_int + m3*(x_int2 - x_int)

    #slope of normal at second surface
    m4 = (y_int2 - 0)/(x_int2 - x2)

    if m4 > 0: #case of negative meniscus (only for displaying purpose)
        err = math.pi
    
    print "slope of second normal:", (math.degrees(math.pi - err + math.atan(m4)))

    #refraction at second surface
    if r2 > 0:
        theta4 = math.degrees(math.fabs(math.atan(m4)) + math.atan(m3))
    else:
        theta4 = math.fabs(math.degrees(math.atan(m3) - math.atan(m4)))
            
    print "Theta4: ", theta4
    
    try:
        theta5 = math.degrees(math.asin((1.585/1)*math.sin(math.radians(theta4))))
        print "Theta5: ", theta5
    except ValueError as e:
        print e
        print "************************************************************\nTIR occured"
        return x_int, y_int, x_int2, y_int2, m3, -1
        sys.exit()

    #viewing angle
    if r2 < 0:
        if math.fabs(m3) > math.fabs(m4):
            theta6 = theta5 + math.degrees(math.atan(m4))
            case = "divergence"
            m5 = math.tan(math.radians(theta6))
            #print "1"
        elif math.fabs(m3) < math.fabs(m4) and theta5 > math.degrees(math.atan(m4)):
            theta6 = theta5 - math.degrees(math.atan(m4))
            case = "convergence"
            m5 = math.tan(math.radians(180 - theta6))
            #print "2"
        elif math.fabs(m3) < math.fabs(m4) and theta5 < math.degrees(math.atan(m4)):
            theta6 = math.degrees(math.atan(m4)) - theta5
            case = "divergence"
            m5 = math.tan(math.radians(theta6))
            #print "3"

    else:
        #print "Inside else;", math.degrees(math.atan(m4))
        theta6 = theta5 - math.fabs(math.degrees(math.atan(m4)))
        case = "divergence"
        m5 = math.tan(math.radians(theta6))

    case = "(" + case + ")"
    print "Viewing angle:", theta6, case
    print "***********************************************************"
    print y_int2, y_int

    return x_int, y_int, x_int2, y_int2, m3, m5
