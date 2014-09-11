#!/usr/bin/env python
#
# Copyright 2013 Johannes Schauer <j.schauer at email.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

from math import sin, cos, pi, copysign
import re

wrap = lambda l: zip(l, l[1:]+l[:1])
sign = lambda x: copysign(1, x)


parts = [
        ("3005" , "Brick 1 x 1"),
        ("2453" , "Brick 1 x 1 x 5"),
        ("3004" , "Brick 1 x 2"),
        ("3245a", "Brick 1 x 2 x 2"),
        ("2454" , "Brick 1 x 2 x 5"),
        ("3622" , "Brick 1 x 3"),
        ("3755" , "Brick 1 x 3 x 5"),
        ("3010" , "Brick 1 x 4"),
        ("3009" , "Brick 1 x 6"),
        ("3754" , "Brick 1 x 6 x 5"),
        ("3008" , "Brick 1 x 8"),
        ("6111" , "Brick 1 x 10"),
        ("6112" , "Brick 1 x 12"),
        ("2465" , "Brick 1 x 16"),
        ("3003" , "Brick 2 x 2"),
        ("2357",  "Brick 2 x 2 Corner"),
        ("30145", "Brick 2 x 2 x 3"),
        ("3002" , "Brick 2 x 3"),
        ("3001" , "Brick 2 x 4"),
        ("30144", "Brick 2 x 4 x 3"),
        ("2456" , "Brick 2 x 6"),
        ("6213" , "Brick 2 x 6 x 3"),
        ("3007" , "Brick 2 x 8"),
        ("3006" , "Brick 2 x 10"),
        ("702",   "Brick 4 x 4 Corner"),
        ("2356" , "Brick 4 x 6"),
        ("6212" , "Brick 4 x 10"),
        ("4202" , "Brick 4 x 12"),
        ("30400", "Brick 4 x 18"),
        ("4201" , "Brick 8 x 8"),
        ("4204" , "Brick 8 x 16"),
        ("733"  , "Brick 10 x 10"),
        ("3024",  "Plate 1 x 1"),
        ("3023",  "Plate 1 x 2"),
        ("3623",  "Plate 1 x 3"),
        ("3710",  "Plate 1 x 4"),
        ("3666",  "Plate 1 x 6"),
        ("3460",  "Plate 1 x 8"),
        ("4477",  "Plate 1 x 10"),
        ("60479", "Plate 1 x 12"),
        ("3022",  "Plate 2 x 2"),
        ("2420",  "Plate 2 x 2 Corner"),
        ("3021",  "Plate 2 x 3"),
        ("3020",  "Plate 2 x 4"),
        ("3795",  "Plate 2 x 6"),
        ("3034",  "Plate 2 x 8"),
        ("3832",  "Plate 2 x 10"),
        ("2445",  "Plate 2 x 12"),
        ("91988", "Plate 2 x 14"),
        ("4282",  "Plate 2 x 16"),
        ("3031",  "Plate 4 x 4"),
        ("2639",  "Plate 4 x 4 Corner"),
        ("3032",  "Plate 4 x 6"),
        ("3035",  "Plate 4 x 8"),
        ("3030",  "Plate 4 x 10"),
        ("3029",  "Plate 4 x 12"),
        ("3958",  "Plate 6 x 6"),
        ("3036",  "Plate 6 x 8"),
        ("3033",  "Plate 6 x 10"),
        ("3028",  "Plate 6 x 12"),
        ("3456",  "Plate 6 x 14"),
        ("3027",  "Plate 6 x 16"),
        ("3026",  "Plate 6 x 24"),
        ("41539", "Plate 8 x 8"),
        ("728",   "Plate 8 x 11"),
        ("92438", "Plate 8 x 16"),
        ("60477", "Slope Brick 18 4 x 1"),
        ("30363", "Slope Brick 18 4 x 2"),
        ("54200", "Slope Brick 31 1 x 1 x 2/3"),
        ("85984", "Slope Brick 31 1 x 2 x 2/3"),
        ("3300",  "Slope Brick 33 2 x 2 Double"),
        ("3299",  "Slope Brick 33 2 x 4 Double"),
        ("4286",  "Slope Brick 33 3 x 1"),
        ("4287",  "Slope Brick 33 3 x 1 Inverted"),
        ("3298",  "Slope Brick 33 3 x 2"),
        ("3747a", "Slope Brick 33 3 x 2"),
        ("4161",  "Slope Brick 33 3 x 3"),
        ("99301", "Slope Brick 33 3 x 3 Double Concave"),
        ("3675",  "Slope Brick 33 3 x 3 Double Convex"),
        ("3297",  "Slope Brick 33 3 x 4"),
        ("3048",  "Slope Brick 45 1 x 2 Triple"),
        ("3040b", "Slope Brick 45 2 x 1"),
        ("3044b", "Slope Brick 45 2 x 1 Double"),
        ("3665",  "Slope Brick 45 2 x 1 Inverted"),
        ("3039",  "Slope Brick 45 2 x 2"),
        ("3043",  "Slope Brick 45 2 x 2 Double"),
        ("3046",  "Slope Brick 45 2 x 2 Double Concave"),
        ("962",   "Slope Brick 45 2 x 2 Double Concave / Double Convex"),
        ("3045",  "Slope Brick 45 2 x 2 Double Convex"),
        ("3660",  "Slope Brick 45 2 x 2 Inverted"),
        ("3676",  "Slope Brick 45 2 x 2 Inverted Double Convex"),
        ("3038",  "Slope Brick 45 2 x 3"),
        ("3042",  "Slope Brick 45 2 x 3 Double"),
        ("3037",  "Slope Brick 45 2 x 4"),
        ("3041",  "Slope Brick 45 2 x 4 Double"),
        ("4445",  "Slope Brick 45 2 x 8"),
        ("60481", "Slope Brick 65 2 x 1 x 2"),
        ("6678a", "Slope Brick 65 2 x 2 x 2"),
        ("4460",  "Slope Brick 75 2 x 1 x 3"),
        ("2449",  "Slope Brick 75 2 x 1 x 3 Inverted"),
        ("3684",  "Slope Brick 75 2 x 2 x 3"),
        ("3685",  "Slope Brick 75 2 x 2 x 3 Double Convex"),
        ("3070b", "Tile 1 x 1"),
        ("3069b", "Tile 1 x 2"),
        ("63864", "Tile 1 x 3"),
        ("2431",  "Tile 1 x 4"),
        ("6636",  "Tile 1 x 6"),
        ("4162",  "Tile 1 x 8"),
        ("3068b", "Tile 2 x 2"),
        ("87079", "Tile 2 x 4"),
        ("6934",  "Tile 3 x 6"),
        ("6881a", "Tile 6 x 6"),
        ("819",   "Baseplate 8 x 12"),
        ("3865",  "Baseplate 8 x 16"),
        ("3497",  "Baseplate 8 x 24"),
        ("4187",  "Baseplate 8 x 32"),
        ("397",   "Baseplate 10 x 16"),
        ("3867",  "Baseplate 16 x 16"),
        ("184",   "Baseplate 16 x 18"),
        ("210",   "Baseplate 16 x 22"),
        ("3334",  "Baseplate 16 x 24"),
        ("3857",  "Baseplate 16 x 32"),
        ("3645",  "Baseplate 24 x 40"),
        ("3811",  "Baseplate 32 x 32"),
        ("4186",  "Baseplate 48 x 48"),
        ("782",   "Baseplate 50 x 50"),
        ("3794a", "Plate 1 x 2 with Center Stud"),
        ("87580", "Plate 2 x 2 with Center Stud"),
    ]

def next_smallest_power_of_2(v):
    v |= v >> 1;
    v |= v >> 2;
    v |= v >> 4;
    v |= v >> 8;
    v |= v >> 16;
    v += 1
    v >>= 1
    return v

def is_power_of_2(v):
    return (v&(v-1)) == 0

def subdivide(rect):
    x,y,w,h = rect
    if w == h and is_power_of_2(w):
        return [(x,y,w)]
    if w > h:
        # get the largest power of 2 that fits
        k = next_smallest_power_of_2(h)
        # split width by it
        rect1 = (x,y,k,h)
        rect2 = (x+k,y,w-k,h)
        return subdivide(rect1) + subdivide(rect2)
    else:
        # get the largest power of 2 that fits
        k = next_smallest_power_of_2(w)
        # split width by it
        rect1 = (x,y,w,k)
        rect2 = (x,y+k,w,h-k)
        return subdivide(rect1) + subdivide(rect2)

def write_file(fname, comments, files, lines, triangles, quads):
    with open(fname, 'w') as outfile:
        for comment in comments:
            outfile.write("0 %s\n"%comment)
        for (x,y,z,a,b,c,d,e,f,g,h,i,fs) in files:
            x,y,z,a,b,c,d,e,f,g,h,i = [round(float(t),6)+0 for t in x,y,z,a,b,c,d,e,f,g,h,i]
            outfile.write("1 16 %s %s %s %s %s %s %s %s %s %s %s %s %s\n"%(x,y,z,a,b,c,d,e,f,g,h,i,fs))
        for (x1, y1, z1), (x2, y2, z2) in lines:
            x1,y1,z1,x2,y2,z2 = [round(t,6)+0 for t in x1,y1,z1,x2,y2,z2]
            outfile.write("2 24 %s %s %s %s %s %s\n"%(x1, y1, z1, x2, y2, z2))
        for (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) in triangles:
            x1,y1,z1,x2,y2,z2,x3,y3,z3 = [round(t,6)+0 for t in x1,y1,z1,x2,y2,z2,x3,y3,z3]
            outfile.write("3 16 %s %s %s %s %s %s %s %s %s\n"%(
                x1, y1, z1, x2, y2, z2, x3, y3, z3))
        for (x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4) in quads:
            x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4 = [round(t,6)+0 for t in x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4]
            outfile.write("4 16 %s %s %s %s %s %s %s %s %s %s %s %s\n"%(
                x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4))

def drawstud():
    lines = list()
    triangles = list()
    quads = list()
    # each stud is 4 LDU high and studs are 20 LDU apart
    center = (0, -4, 0)
    # each stud has a radius of 6 LDU
    studsides = 16
    circle = [(center[0] + sin((side*2*pi)/studsides)*6,
        center[2] + cos((side*2*pi)/studsides)*6)
        for side in range(studsides)]
    # now for each slice of the cake...
    for p1, p2 in wrap(circle):
        # write the top plate
        triangles.append(((center[0], center[1], center[2]),
            (p1[0], -4, p1[1]),
            (p2[0], -4, p2[1])))
        # write the side
        quads.append(((p1[0], -4, p1[1]), (p2[0], -4, p2[1]),
            (p2[0],  0, p2[1]), (p1[0],  0, p1[1])))
        # write the lines top and bottom
        lines.append(((p1[0], -4, p1[1]), (p2[0], -4, p2[1])))
        lines.append(((p1[0], 0, p1[1]), (p2[0], 0, p2[1])))
    return lines, triangles, quads

def drawbox():
    lines = list()
    triangles = list()
    quads = list()
    outertopcoords = [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]
    outerbottomcoords = [(x, 1, z) for x,_,z in outertopcoords]
    # write outer top plate and lines
    quads.append(outertopcoords)
    for p1, p2 in wrap(outertopcoords):
        lines.append((p1, p2))
    # outer sides and lines
    for (p1, p2), (p3, p4) in zip(wrap(outertopcoords), wrap(outerbottomcoords)):
        quads.append((p1,p2,p4,p3))
        lines.append((p1,p3))
    # write outer bottom plate and lines
    quads.append(outerbottomcoords)
    for p1, p2 in wrap(outerbottomcoords):
        lines.append((p1, p2))
    return lines, triangles, quads

def drawopenbox():
    lines = list()
    triangles = list()
    quads = list()
    outertopcoords = [(0,0,0),(1,0,0),(1,0,1),(0,0,1)]
    outerbottomcoords = [(x, 1, z) for x,_,z in outertopcoords]
    # write outer top plate and lines
    quads.append(outertopcoords)
    for p1, p2 in wrap(outertopcoords):
        lines.append((p1, p2))
    # outer sides and lines
    for (p1, p2), (p3, p4) in zip(wrap(outertopcoords), wrap(outerbottomcoords)):
        quads.append((p1,p2,p4,p3))
        lines.append((p1,p3))
    for p1, p2 in wrap(outerbottomcoords):
        lines.append((p1, p2))
    return lines, triangles, quads

def render_part(part):
    partid, parttext = part[:2]
    ###################################################
    # parse part text into usable information         #
    ###################################################
    m = re.match(r"(?P<type>[A-Za-z0-9 ]+?) (?P<studsz>\d+)"+
            r" x (?P<studsx>\d+)(?: x (?P<height>\d+(?:/\d+)?))?"+
            r"(?: (?P<corner>Corner)| "+
            r"(?P<slope>(?:Double|Triple|Inverted|Concave|Convex| |/)+)| "+
            r"(?P<centerstud>with Center Stud))?",
            parttext)
    ###################################################
    # sanity checks                                   #
    ###################################################
    if m.group('type') not in ['Brick', 'Plate', 'Slope Brick 18',
            'Slope Brick 31', 'Slope Brick 33', 'Slope Brick 45',
            'Slope Brick 65', 'Slope Brick 75', 'Tile', 'Baseplate']:
        print "not supported part type: %s"%m.group('type')
        exit(1)
    if m.group('type') == 'Plate' and m.group('height'):
        print "plates can't have a height"
        exit(1)
    if m.group('height') and m.group('corner'):
        print "corners can't have a height"
        exit(1)
    if m.group('corner') and (m.group('studsx') != m.group('studsz')):
        print "corners must be squares"
        exit(1)
    ###################################################
    # set up data structures                          #
    ###################################################
    files = list()
    lines = list()
    triangles = list()
    quads = list()
    studsz = int(m.group('studsz'))
    studsx = int(m.group('studsx'))
    if m.group('type') in ['Brick', 'Slope Brick 18', 'Slope Brick 31',
            'Slope Brick 33', 'Slope Brick 45', 'Slope Brick 65',
            'Slope Brick 75']:
        if m.group('height'):
            if m.group('height') == '2/3':
                height = 2
            else:
                height = int(m.group('height'))*3
        else:
            height = 3
    else:
        height = 1
    # convert plate height to LDraw units
    height *= 8
    ###################################################
    # handle bricks, plates and slope brick 31        #
    ###################################################
    if m.group('type') == 'Baseplate':
        rects = subdivide((-studsx/2.0,-studsz/2.0,studsx,studsz))
        for x,z,s in rects:
            files.append(((x+s/2.0)*20, 0, (z+s/2.0)*20,1,0,0,0,1,0,0,0,1,"stud%d.dat"%s))
        files.append((-studsx*10,0,-studsz*10,studsx*20,0,0,0,4,0,0,0,studsz*20,"box.dat"))
    elif m.group('type') in ['Brick', 'Plate'] and m.group('corner'):
        for z in [0,1]:
            for x in [0,1]:
                if z == 0 and x == 0:
                    continue
                files.append((-x*studsx*10+studsx*5, 0, -studsz*z*10+studsz*5,1,0,0,0,1,0,0,0,1,"stud%d.dat"%(studsz/2)))
        # create top, bottom, inner and outer rectangles
        # draw an L
        coords = [(0,0),(1,0),(1,-1),(-1,-1),(-1,1),(0,1)]
        # walls are 4 LDU thick, use sign() in case x or y are zero
        outertopcoords = [(studsx*10*x, 0, studsz*10*z) for x,z in coords]
        innertopcoords = [(studsx*10*x-sign(x)*4, 4, studsz*10*z-sign(z)*4) for x,z in coords]
        outerbottomcoords = [(x, height, z) for x,y,z in outertopcoords]
        innerbottomcoords = [(x, height, z) for x,y,z in innertopcoords]
        # write outer top plate and lines
        # draw two trapezoids
        quads.append(outertopcoords[:4])
        quads.append(outertopcoords[3:]+outertopcoords[:1])
        for p1, p2 in wrap(outertopcoords):
            lines.append((p1, p2))
        # outer sides and lines
        for (p1, p2), (p3, p4) in zip(wrap(outertopcoords), wrap(outerbottomcoords)):
            quads.append((p1,p2,p4,p3))
            lines.append((p1,p3))
        # write inner top plate and lines
        # draw two trapezoids
        quads.append(innertopcoords[:4])
        quads.append(innertopcoords[3:]+innertopcoords[:1])
        for p1, p2 in wrap(innertopcoords):
            lines.append((p1, p2))
        # inner sides and lines
        for (p1, p2), (p3, p4) in zip(wrap(innertopcoords), wrap(innerbottomcoords)):
            quads.append((p1,p2,p4,p3))
            lines.append((p1,p3))
        # write out bottom with trapezoids and lines
        for (p1, p2), (p3, p4) in zip(wrap(innerbottomcoords), wrap(outerbottomcoords)):
            quads.append((p1, p2, p4, p3))
            lines.append((p1, p2))
            lines.append((p3, p4))
    elif m.group('type') in ['Brick', 'Plate', 'Tile']:
        # draw studs
        if m.group('centerstud'):
            files.append((0,0,0,1,0,0,0,1,0,0,0,1,"stud1.dat"))
        elif m.group('type') not in ['Slope Brick 31', 'Tile']:
            rects = subdivide((-studsx/2.0,-studsz/2.0,studsx,studsz))
            for x,z,s in rects:
                files.append(((x+s/2.0)*20, 0, (z+s/2.0)*20,1,0,0,0,1,0,0,0,1,"stud%d.dat"%s))
        # outer box
        files.append((-studsx*10,0,-studsz*10,studsx*20,0,0,0,height,0,0,0,studsz*20,"openbox.dat"))
        # inner box
        files.append((-studsx*10+4,4,-studsz*10+4,studsx*20-8,0,0,0,height-4,0,0,0,studsz*20-8,"openbox.dat"))
        # write out bottom with trapezoids
        coords = [(1,1),(1,-1),(-1,-1),(-1,1)]
        outerbottomcoords = [(studsx*10*x, height, studsz*10*z) for x,z in coords]
        innerbottomcoords = [(studsx*10*x-sign(x)*4, height, studsz*10*z-sign(z)*4) for x,z in coords]
        for (p1, p2), (p3, p4) in zip(wrap(innerbottomcoords), wrap(outerbottomcoords)):
            quads.append((p1, p2, p4, p3))
    elif m.group('type') == 'Slope Brick 31':
        # create top, bottom, inner and outer rectangles
        # draw a square
        coords = [(1,1),(1,-1),(-1,-1),(-1,1)]
        # walls are 4 LDU thick, use sign() in case x or y are zero
        outertopcoords = [(studsx*10*x, 0 if z == 1 else height-4, studsz*10*z) for x,z in coords]
        innertopcoords = [(studsx*10*x-sign(x)*4, height-4, studsz*10*z-sign(z)*4) for x,z in coords]
        outerbottomcoords = [(x, height, z) for x,y,z in outertopcoords]
        innerbottomcoords = [(x, height, z) for x,y,z in innertopcoords]
        # write outer top plate and lines
        # draw a rectangle
        quads.append(outertopcoords)
        for p1, p2 in wrap(outertopcoords):
            lines.append((p1, p2))
        # outer sides and lines
        for (p1, p2), (p3, p4) in zip(wrap(outertopcoords), wrap(outerbottomcoords)):
            quads.append((p1,p2,p4,p3))
            lines.append((p1,p3))
        # write inner top plate and lines
        # draw a rectangle
        quads.append(innertopcoords)
        for p1, p2 in wrap(innertopcoords):
            lines.append((p1, p2))
        # inner sides and lines
        for (p1, p2), (p3, p4) in zip(wrap(innertopcoords), wrap(innerbottomcoords)):
            quads.append((p1,p2,p4,p3))
            lines.append((p1,p3))
        # write out bottom with trapezoids and lines
        for (p1, p2), (p3, p4) in zip(wrap(innerbottomcoords), wrap(outerbottomcoords)):
            quads.append((p1, p2, p4, p3))
            lines.append((p1, p2))
            lines.append((p3, p4))
    ###################################################
    # handle slopes                                   #
    ###################################################
    elif m.group('type') in ['Slope Brick 18', 'Slope Brick 33',
            'Slope Brick 45', 'Slope Brick 65', 'Slope Brick 75']:
        # draw studs (draw an L if double concave)
        coordsL = [(0,0),(0,-1),(-1,-1),(-1,1),(1,1),(1,0)]
        coords = [(-1,-1),(-1,1),(1,1),(1,-1)]
        ###################################################
        # handle double, triple slopes                    #
        ###################################################
        if m.group('slope') in ['Double', 'Triple', 'Double Concave / Double Convex']:
            coords = [(1,1),(1,-1),(-1,-1),(-1,1)]
            # create top, bottom, inner and outer rectangles
            outertopcoords = [(studsx*10*x, 24-4, studsz*10*z) for x,z in coords]
            outerbottomcoords = [(x, 24, z) for x,y,z in outertopcoords]
            # walls are 4 LDU thick, use sign() in case x or y are zero
            innertopcoords = [(studsx*10*x-sign(x)*4, 24-4, studsz*10*z-sign(z)*4) for x,z in coords]
            innerbottomcoords = [(x, 24, z) for x,y,z in innertopcoords]
            # outer sides and lines
            for (p1, p2), (p3, p4) in zip(wrap(outertopcoords), wrap(outerbottomcoords)):
                quads.append((p1,p2,p4,p3))
                lines.append((p1,p3))
            # write inner top plate and lines
            quads.append(innertopcoords)
            for p1, p2 in wrap(innertopcoords):
                lines.append((p1, p2))
            # inner sides and lines
            for (p1, p2), (p3, p4) in zip(wrap(innertopcoords), wrap(innerbottomcoords)):
                quads.append((p1,p2,p4,p3))
                lines.append((p1,p3))
            # write out bottom with trapezoids and lines
            for (p1, p2), (p3, p4) in zip(wrap(innerbottomcoords), wrap(outerbottomcoords)):
                quads.append((p1, p2, p4, p3))
                lines.append((p1, p2))
                lines.append((p3, p4))
            ###################################################
            # handle triple slopes                            #
            ###################################################
            if 'Triple' == m.group('slope'):
                tip = (0,0,studsz*10)
                # write outer top lines
                for p1, p2 in wrap(outertopcoords)[:-1]:
                    lines.append((p1, p2))
                # write out slopes and lines
                for p1, p2 in wrap(outertopcoords):
                    triangles.append([p1,p2,tip])
                    lines.append((p1,tip))
            ###################################################
            # handle double slopes                            #
            ###################################################
            elif 'Double' == m.group('slope'):
                if m.group('type') == 'Slope Brick 45':
                    ridge = [(studsx*10,0,0),(-studsx*10,0,0)]
                elif m.group('type') == 'Slope Brick 33':
                    ridge = [(studsx*10,24-14,0),(-studsx*10,24-14,0)]
                else:
                    print "unsupported slope type for double"
                    exit(1)
                # write outer top lines
                lines.append(outertopcoords[1:3])
                lines.append(outertopcoords[:1]+outertopcoords[-1:])
                # draw gables
                triangles.append(ridge[:1]+outertopcoords[:2])
                triangles.append(ridge[-1:]+outertopcoords[2:])
                # draw slopes
                quads.append(ridge+outertopcoords[1:3])
                quads.append(ridge+outertopcoords[-1:]+outertopcoords[:1])
                # draw lines for ridge and rakes
                lines.append(ridge)
                lines.append(ridge[:1]+outertopcoords[:1])
                lines.append(ridge[:1]+outertopcoords[1:2])
                lines.append(ridge[-1:]+outertopcoords[-1:])
                lines.append(ridge[-1:]+outertopcoords[2:3])
            ###################################################
            # handle double concave / double convex slopes    #
            ###################################################
            elif 'Double Concave / Double Convex' == m.group('slope'):
                if m.group('type') != 'Slope Brick 45':
                    print "unsupported slope type for double concave / double convex"
                    exit(1)
                ridge1 = [(0,0,0),(-studsx*10,0,0)]
                ridge2 = [(0,0,studsz*10),(0,0,0)]
                # write outer top lines (eaves)
                lines.append(outertopcoords[1:3])
                lines.append(outertopcoords[:2])
                # draw gables
                triangles.append(ridge1[-1:]+outertopcoords[2:])
                triangles.append(ridge2[:1]+outertopcoords[:1]+outertopcoords[-1:])
                # draw slopes
                quads.append(ridge1+outertopcoords[1:3])
                quads.append(ridge2+outertopcoords[:2])
                triangles.append(ridge1+outertopcoords[-1:])
                triangles.append(ridge2+outertopcoords[-1:])
                # draw ridges
                lines.append(ridge1)
                lines.append(ridge2)
                # draw rakes
                lines.append(ridge1[-1:]+outertopcoords[2:3])
                lines.append(ridge1[-1:]+outertopcoords[-1:])
                lines.append(ridge2[:1]+outertopcoords[:1])
                lines.append(ridge2[:1]+outertopcoords[-1:])
                # draw valley and hip
                lines.append(((0,0,0),outertopcoords[-1]))
                lines.append(((0,0,0),outertopcoords[1]))
        ###################################################
        # handle all other slopes                         #
        ###################################################
        else:
            if m.group('slope') in ['Inverted', 'Inverted Double Convex']:
                rects = subdivide((-studsx/2.0,-studsz/2.0,studsx,studsz))
                for x,z,s in rects:
                    files.append(((x+s/2.0)*20, 0, (z+s/2.0)*20,1,0,0,0,1,0,0,0,1,"stud%d.dat"%s))
            elif m.group('slope') == 'Double Convex':
                files.append((-10*(studsx-1), 0, 10*(studsz-1),1,0,0,0,1,0,0,0,1,"stud1.dat"))
            elif m.group('slope') == 'Double Concave':
                for z in range(studsz):
                    for x in range(studsx):
                        if z == 0 or x == studsx-1:
                            files.append(((studsx/2.0 - x)*20 - 10, 0, (studsz/2.0 - z)*20 - 10,1,0,0,0,1,0,0,0,1,"stud1.dat"))
            else:
                for x in range(studsx):
                    files.append(((studsx/2.0 - x)*20 - 10, 0, 10*(studsz-1),1,0,0,0,1,0,0,0,1,"stud1.dat"))
            ###################################################
            # create top, bottom, inner and outer rectangles  #
            ###################################################
            if m.group('slope') in ['Double Convex', 'Inverted Double Convex']:
                outertopcoords = [((x-studsx+1)*10, 0, (z+studsz-1)*10) for x,z in coords]
                outerbottomcoords = [(studsx*10*x, height, studsz*10*z) for x,z in coords] # big
                helpercoords = [((x-studsx+1)*10, height, (z+studsz-1)*10) for x,z in coords] # small
                innerbottomcoords = [(studsx*10*x-sign(x)*4, height, studsz*10*z-sign(z)*4) for x,z in coords]
                innertopcoords = [(6*x-(studsx-1)*10, 4, z*6+(studsz-1)*10) for x,z in coords]
                nosedown1 = outerbottomcoords[:1]+outerbottomcoords[-1:]
                noseup1 = [(x,height-4,z) for x,y,z in nosedown1]
                nosedown2 = outerbottomcoords[-2:-1]+outerbottomcoords[-1:]
                noseup2 = [(x,height-4,z) for x,y,z in nosedown2]
                # if an inverted piece is requested, switch coordinates around
                if m.group('slope') == 'Inverted Double Convex':
                    outerbottomcoords, helpercoords, outertopcoords = (
                            [(x,0,z) for x,y,z in outerbottomcoords],
                            [(x,0,z) for x,y,z in helpercoords],
                            [(x,height,z) for x,y,z in outertopcoords])
                    innertopcoords, innerbottomcoords = (
                            [(x,4,z) for x,y,z in innertopcoords],
                            [(x,height,z) for x,y,z in innertopcoords])
                    noseup1, nosedown1 = [(x,0,z) for x,y,z in nosedown1], [(x,4,z) for x,y,z in noseup1]
                    noseup2, nosedown2 = [(x,0,z) for x,y,z in nosedown2], [(x,4,z) for x,y,z in noseup2]
            elif m.group('slope') == 'Double Concave':
                outertopcoords = [(studsx*10*x+(abs(x)-1)*(10*studsx-20), 0, studsz*10*z+(1-abs(z))*(10*studsz-20)) for x,z in coordsL]
                outerbottomcoords = [(studsx*10*x, height, studsz*10*z) for x,z in coords] # big
                helpercoords = [(studsx*10*x+(abs(x)-1)*(10*studsx-20), height, studsz*10*z+(1-abs(z))*(10*studsz-20)) for x,z in coordsL] # small
                innertopcoords = [((studsx*10-4)*x+(abs(x)-1)*(10*studsx-20), 4, (studsz*10-4)*z+(1-abs(z))*(10*studsz-20)) for x,z in coordsL]
                innerbottomcoords = [((studsx*10-4)*x, height, (studsz*10-4)*z) for x,z in coords]
                tip = [(studsx*10,height,-studsz*10), (studsx*10,height-4,-studsz*10)]
                # there is somehow no inverted double concave piece
            else:
                outertopcoords = [(studsx*10*x, 0, (z+studsz-1)*10) for x,z in coords]
                helpercoords = [(studsx*10*x, height, (z+studsz-1)*10) for x,z in coords] # small
                outerbottomcoords = [(studsx*10*x, height, studsz*10*z) for x,z in coords] # big
                innertopcoords = [((studsx*10-4)*x, 4, z*6+(studsz-1)*10) for x,z in coords]
                innerbottomcoords = [(studsx*10*x-sign(x)*4, height, studsz*10*z-sign(z)*4) for x,z in coords]
                nosedown = outerbottomcoords[:1]+outerbottomcoords[-1:]
                noseup = [(x,height-4,z) for x,y,z in nosedown]
                # if an inverted piece is requested, switch coordinates around
                if m.group('slope') == 'Inverted':
                    outerbottomcoords, helpercoords, outertopcoords = (
                            [(x,0,z) for x,y,z in outerbottomcoords],
                            [(x,0,z) for x,y,z in helpercoords],
                            [(x,height,z) for x,y,z in outertopcoords])
                    innertopcoords, innerbottomcoords = (
                            [(x,4,z) for x,y,z in innertopcoords],
                            [(x,height,z) for x,y,z in innertopcoords])
                    noseup, nosedown = [(x,0,z) for x,y,z in nosedown], [(x,4,z) for x,y,z in noseup]
            ###################################################
            # create outer sides and lines                    #
            ###################################################
            if m.group('slope') in ['Double Convex', 'Inverted Double Convex']:
                for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[:2], wrap(helpercoords)[:2]):
                    quads.append((p1,p2,p4,p3))
                for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[1:2], wrap(helpercoords)[1:2]):
                    lines.append((p1,p3))
            elif m.group('slope') == 'Double Concave':
                for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[1:5], wrap(helpercoords)[1:5]):
                    quads.append((p1,p2,p4,p3))
                for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[2:5], wrap(helpercoords)[2:5]):
                    lines.append((p1,p3))
            else:
                for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[:3], wrap(helpercoords)[:3]):
                    quads.append((p1,p2,p4,p3))
                for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[1:3], wrap(helpercoords)[1:3]):
                    lines.append((p1,p3))
            ###################################################
            # draw nose                                       #
            ###################################################
            if m.group('slope') in ['Inverted Double Convex', 'Double Convex']:
                quads.append(noseup1+[nosedown1[1]]+[nosedown1[0]])
                quads.append(noseup2+[nosedown2[1]]+[nosedown2[0]])
            elif m.group('slope') != 'Double Concave':
                quads.append(noseup+[nosedown[1]]+[nosedown[0]])
            ###################################################
            # draw sides and lines to the nose                #
            ###################################################
            if m.group('slope') in ['Double Convex', 'Inverted Double Convex']:
                quads.append(outertopcoords[-2:-1]+helpercoords[-2:-1]+noseup2[:1]+nosedown2[:1])
                quads.append(outertopcoords[:1]+helpercoords[:1]+noseup1[:1]+nosedown1[:1])
            elif m.group('slope') == 'Double Concave':
                quads.append(outertopcoords[-1:]+helpercoords[-1:]+tip)
                quads.append(outertopcoords[1:2]+helpercoords[1:2]+tip)
            else:
                quads.append(outertopcoords[-1:]+helpercoords[-1:]+nosedown[-1:]+noseup[-1:])
                quads.append(outertopcoords[:1]+helpercoords[:1]+nosedown[:1]+noseup[:1])
            if m.group('slope') in ['Inverted Double Convex', 'Double Convex']:
                lines.append(noseup1[:1]+nosedown1[:1])
                lines.append(noseup1[-1:]+nosedown1[-1:])
                lines.append(noseup2[:1]+nosedown2[:1])
                lines.append(noseup2[-1:]+nosedown2[-1:])
            elif m.group('slope') == 'Double Concave':
                lines.append(tip)
            else:
                lines.append(noseup[:1]+nosedown[:1])
                lines.append(noseup[-1:]+nosedown[-1:])
            ###################################################
            # write inner top plate and lines                 #
            ###################################################
            if m.group('slope') == 'Double Concave':
                quads.append(innertopcoords[:4])
                quads.append(innertopcoords[3:]+innertopcoords[:1])
            else:
                quads.append(innertopcoords)
            for p1, p2 in wrap(innertopcoords):
                lines.append((p1, p2))
            ###################################################
            # inner sides and lines                           #
            ###################################################
            if m.group('slope') == 'Double Concave':
                # the quadrilateral sides
                for (p1, p2), (p3, p4) in zip(wrap(innertopcoords)[1:5],
                        wrap(innerbottomcoords)[-1:]+wrap(innerbottomcoords)[:4]):
                    quads.append((p1,p2,p4,p3))
                for (p1, p2), (p3, p4) in zip(wrap(innertopcoords)[2:5], wrap(innerbottomcoords)[:4]):
                    lines.append((p1,p3))
                # the slopes
                triangles.append(innertopcoords[-1:]+innertopcoords[:1]+innerbottomcoords[-1:])
                triangles.append(innertopcoords[:1]+innertopcoords[1:2]+innerbottomcoords[-1:])
                lines.append(innertopcoords[-1:]+innerbottomcoords[-1:])
                lines.append(innertopcoords[:1]+innerbottomcoords[-1:])
                lines.append(innertopcoords[1:2]+innerbottomcoords[-1:])
            else:
                for (p1, p2), (p3, p4) in zip(wrap(innertopcoords), wrap(innerbottomcoords)):
                    quads.append((p1,p2,p4,p3))
                    lines.append((p1,p3))
            ###################################################
            # draw slope and lines around it                  #
            ###################################################
            if m.group('slope') in ['Double Convex', 'Inverted Double Convex']:
                if m.group('slope') == 'Inverted Double Convex':
                    noseup1, nosedown1, noseup2, nosedown2 = nosedown1, noseup1, nosedown2, noseup2
                quads.append(outertopcoords[-1:]+outertopcoords[:1]+[noseup1[1]]+[noseup1[0]])
                quads.append(outertopcoords[2:3]+outertopcoords[3:4]+[noseup2[1]]+[noseup2[0]])
                lines.append(noseup1[:1]+outertopcoords[:1])
                lines.append(noseup1[-1:]+outertopcoords[-1:])
                lines.append(noseup2[-2:-1]+outertopcoords[-2:-1])
                lines.append(noseup1[:1]+noseup1[-1:])
                lines.append(noseup2[:1]+noseup2[-1:])
            elif m.group('slope') == 'Double Concave':
                triangles.append(outertopcoords[-1:]+outertopcoords[:1]+[tip[1]])
                triangles.append(outertopcoords[:1]+outertopcoords[1:2]+[tip[1]])
                lines.append(outertopcoords[-1:]+[tip[1]])
                lines.append(outertopcoords[:1]+[tip[1]])
                lines.append(outertopcoords[1:2]+[tip[1]])
            else:
                if m.group('slope') == 'Inverted':
                    noseup, nosedown = nosedown, noseup
                quads.append(outertopcoords[-1:]+outertopcoords[:1]+[noseup[1]]+[noseup[0]])
                lines.append(noseup[:1]+outertopcoords[:1])
                lines.append(noseup[-1:]+outertopcoords[-1:])
                lines.append(noseup[:1]+noseup[-1:])
            ###################################################
            # for drawing top/bottom, switch the coords       #
            ###################################################
            if m.group('slope') in ['Inverted Double Convex', 'Inverted']:
                outertopcoords, outerbottomcoords = outerbottomcoords, outertopcoords
            ###################################################
            # write out bottom with trapezoids and lines      #
            ###################################################
            for (p1, p2), (p3, p4) in zip(wrap(innerbottomcoords), wrap(outerbottomcoords)):
                quads.append((p1, p2, p4, p3))
                lines.append((p1, p2))
                lines.append((p3, p4))
            ###################################################
            # write outer top plate and lines                 #
            ###################################################
            if m.group('slope') == 'Double Concave':
                quads.append(outertopcoords[:4])
                quads.append(outertopcoords[3:]+outertopcoords[:1])
            else:
                quads.append(outertopcoords)
            for p1, p2 in wrap(outertopcoords):
                lines.append((p1, p2))
    else:
        print "not supported part type: %s"%m.group('type')
        exit(1)
    ###################################################
    # write data to file                              #
    ###################################################
    write_file("parts/%s.dat"%partid, [parttext], files, lines, triangles, quads)

# coordinates are normalized with six significant digits after the comma
# because of the following distribution of the official ldraw files:
# egrep -ho '\.[^ e]+' /usr/share/ldraw-parts/p/* /usr/share/ldraw-parts/parts/* | awk '{ print length-1 }' | sort -n | uniq -c
# 1175688 1
# 2548068 2
# 3076127 3
# 1170125 4
#  209386 5
#   33254 6
#    2274 7
#     107 8
#     109 9
#      15 10
#      54 14
#       1 17
#       1 18
#       2 28


if __name__ == "__main__":
    lines, triangles, quads = drawstud()
    write_file("parts/stud1.dat", [], [], lines, triangles, quads)
    for s in [2,4,8,16,32]:
        files = list()
        for z in range(2):
            for x in range(2):
                files.append((s*(5 - x*10), 0, s*(5 - z*10),1,0,0,0,1,0,0,0,1,"stud%d.dat"%(s/2)))
        write_file("parts/stud%d.dat"%s, [], files, [], [], [])
    lines, triangles, quads = drawbox()
    write_file("parts/box.dat", [], [], lines, triangles, quads)
    lines, triangles, quads = drawopenbox()
    write_file("parts/openbox.dat", [], [], lines, triangles, quads)
    for part in parts:
        render_part(part)
