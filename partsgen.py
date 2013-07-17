from math import sin, cos, pi, copysign
import re

wrap = lambda l: zip(l, l[1:]+l[:1])
sign = lambda x: copysign(1, x)

studsides = 16

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
        ("3048",  "Slope Brick 45 2 x 1 Triple"),
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
    ]

def drawstud(studsx, studsz, x, z, lines, triangles, quads):
    # each stud is 4 LDU high and studs are 20 LDU apart
    center = ((studsx/2.0 - x)*20 - 10, -4, (studsz/2.0 - z)*20 - 10)
    # each stud has a radius of 6 LDU
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

def render():
    for part in parts:
        partid, parttext = part[:2]
        m = re.match(r"(?P<type>[A-Za-z0-9 ]+?) (?P<studsz>\d+)"+
                r" x (?P<studsx>\d+)(?: x (?P<height>\d+(?:/\d+)?))?"+
                r"(?: (?P<corner>Corner)| "+
                r"(?P<slope>(?:Double|Triple|Inverted|Concave|Convex| |/)+))?",
                parttext)
        # sanity checks
        if m.group('type') not in ['Brick', 'Plate', 'Slope Brick 18',
                'Slope Brick 31', 'Slope Brick 33', 'Slope Brick 45',
                'Slope Brick 65', 'Slope Brick 75']:
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
        if m.group('type') in ['Brick', 'Plate']:
            # draw studs
            for z in range(studsz):
                for x in range(studsx):
                    if not m.group('corner') or z >= studsz/2 or x >= studsx/2:
                        drawstud(studsx, studsz, x, z, lines, triangles, quads)
            # create top, bottom, inner and outer rectangles
            # in case of a corner, draw an L otherwise draw a square
            if m.group('corner'):
                coords = [(0,0),(1,0),(1,-1),(-1,-1),(-1,1),(0,1)]
            else:
                coords = [(1,1),(1,-1),(-1,-1),(-1,1)]
            outertopcoords = [(studsx*10*x, 0, studsz*10*z) for x,z in coords]
            outerbottomcoords = [(x, height*8, z) for x,y,z in outertopcoords]
            # walls are 4 LDU thick, use sign() in case x or y are zero
            innertopcoords = [(studsx*10*x-sign(x)*4, 4, studsz*10*z-sign(z)*4) for x,z in coords]
            innerbottomcoords = [(x, height*8, z) for x,y,z in innertopcoords]
            # write outer top plate and lines
            # in case of a corner draw two trapezoids, otherwise draw a rectangle
            if m.group('corner'):
                quads.append(outertopcoords[:4])
                quads.append(outertopcoords[3:]+outertopcoords[:1])
            else:
                quads.append(outertopcoords)
            for p1, p2 in wrap(outertopcoords):
                lines.append((p1, p2))
            # outer sides and lines
            for (p1, p2), (p3, p4) in zip(wrap(outertopcoords), wrap(outerbottomcoords)):
                quads.append((p1,p2,p4,p3))
                lines.append((p1,p3))
            # write inner top plate and lines
            # in case of a corner draw two trapezoids, otherwise draw a rectangle
            if m.group('corner'):
                quads.append(innertopcoords[:4])
                quads.append(innertopcoords[3:]+innertopcoords[:1])
            else:
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
        elif m.group('type') in ['Slope Brick 18', 'Slope Brick 31',
                'Slope Brick 33', 'Slope Brick 45', 'Slope Brick 65',
                'Slope Brick 75']:
            # draw studs (draw an L if double concave)
            coordsL = [(0,0),(0,-1),(-1,-1),(-1,1),(1,1),(1,0)]
            coords = [(-1,-1),(-1,1),(1,1),(1,-1)]
            if m.group('type') != 'Slope Brick 31' \
                    and 'Double' != m.group('slope') \
                    and 'Triple' != m.group('slope') \
                    and 'Double Concave / Double Convex' != m.group('slope'):
                if m.group('slope') in ['Inverted', 'Inverted Double Convex']:
                    for z in range(studsz):
                        for x in range(studsx):
                            drawstud(studsx, studsz, x, z, lines, triangles, quads)
                elif m.group('slope') == 'Double Convex':
                    drawstud(studsx, studsz, studsx-1, 0, lines, triangles, quads)
                elif m.group('slope') == 'Double Concave':
                    for z in range(studsz):
                        for x in range(studsx):
                            if z == 0 or x == studsx-1:
                                drawstud(studsx, studsz, x, z, lines, triangles, quads)
                else:
                    for x in range(studsx):
                        drawstud(studsx, studsz, x, 0, lines, triangles, quads)
                # create top, bottom, inner and outer rectangles
                if m.group('slope') == 'Inverted Double Convex':
                    outertopcoords = [(studsx*10*x, 0, studsz*10*z) for x,z in coords]
                    outertopcoords2 = [((x-studsx+1)*10, 0, (z+studsz-1)*10) for x,z in coords] # small
                    outerbottomcoords = [((x-studsx+1)*10, height*8, (z+studsz-1)*10) for x,z in coords]
                    innertopcoords = [(6*x-(studsx-1)*10, 4, z*6+(studsz-1)*10) for x,z in coords]
                    innerbottomcoords = [(6*x-(studsx-1)*10, height*8, z*6+(studsz-1)*10) for x,z in coords]
                    noseup1 = outertopcoords[:1]+outertopcoords[-1:]
                    nosedown1 = [(x,4,z) for x,y,z in noseup1]
                    noseup2 = outertopcoords[-2:-1]+outertopcoords[-1:]
                    nosedown2 = [(x,4,z) for x,y,z in noseup2]
                elif m.group('slope') == 'Double Convex':
                    outertopcoords = [((x-studsx+1)*10, 0, (z+studsz-1)*10) for x,z in coords]
                    outerbottomcoords = [(studsx*10*x, height*8, studsz*10*z) for x,z in coords] # big
                    outerbottomcoords2 = [((x-studsx+1)*10, height*8, (z+studsz-1)*10) for x,z in coords] # small
                    innerbottomcoords = [(studsx*10*x-sign(x)*4, height*8, studsz*10*z-sign(z)*4) for x,z in coords]
                    innertopcoords = [(6*x-(studsx-1)*10, 4, z*6+(studsz-1)*10) for x,z in coords]
                    nosedown1 = outerbottomcoords[:1]+outerbottomcoords[-1:]
                    noseup1 = [(x,height*8-4,z) for x,y,z in nosedown1]
                    nosedown2 = outerbottomcoords[-2:-1]+outerbottomcoords[-1:]
                    noseup2 = [(x,height*8-4,z) for x,y,z in nosedown2]
                elif m.group('slope') == 'Double Concave':
                    outertopcoords = [(studsx*10*x+(abs(x)-1)*(10*studsx-20), 0, studsz*10*z+(1-abs(z))*(10*studsz-20)) for x,z in coordsL]
                    outerbottomcoords = [(studsx*10*x, height*8, studsz*10*z) for x,z in coords] # big
                    outerbottomcoords2 = [(studsx*10*x+(abs(x)-1)*(10*studsx-20), height*8, studsz*10*z+(1-abs(z))*(10*studsz-20)) for x,z in coordsL] # small
                    innertopcoords = [((studsx*10-4)*x+(abs(x)-1)*(10*studsx-20), 4, (studsz*10-4)*z+(1-abs(z))*(10*studsz-20)) for x,z in coordsL]
                    innerbottomcoords = [((studsx*10-4)*x, height*8, (studsz*10-4)*z) for x,z in coords]
                    tip = [(studsx*10,height*8,-studsz*10), (studsx*10,height*8-4,-studsz*10)]
                else:
                    outertopcoords = [(studsx*10*x, 0, (z+studsz-1)*10) for x,z in coords]
                    outerbottomcoords2 = [(studsx*10*x, height*8, (z+studsz-1)*10) for x,z in coords] # small
                    outerbottomcoords = [(studsx*10*x, height*8, studsz*10*z) for x,z in coords] # big
                    innertopcoords = [((studsx*10-4)*x, 4, z*6+(studsz-1)*10) for x,z in coords]
                    innerbottomcoords = [(studsx*10*x-sign(x)*4, height*8, studsz*10*z-sign(z)*4) for x,z in coords]
                    nosedown = outerbottomcoords[:1]+outerbottomcoords[-1:]
                    noseup = [(x,height*8-4,z) for x,y,z in nosedown]
                    # invert all the coordinates along the y axis
                    if m.group('slope') == 'Inverted':
                        outertopcoords, outertopcoords2, outerbottomcoords = (
                                [(x,0,z) for x,y,z in outerbottomcoords],
                                [(x,0,z) for x,y,z in outerbottomcoords2],
                                [(x,height*8,z) for x,y,z in outertopcoords])
                        innertopcoords, innerbottomcoords = (
                                [(x,4,z) for x,y,z in innertopcoords],
                                [(x,height*8,z) for x,y,z in innertopcoords])
                        noseup = outertopcoords[:1]+outertopcoords[-1:]
                        nosedown = [(x,4,z) for x,y,z in noseup]
                # write outer top plate and lines
                if m.group('slope') == 'Double Concave':
                    quads.append(outertopcoords[:4])
                    quads.append(outertopcoords[3:]+outertopcoords[:1])
                else:
                    quads.append(outertopcoords)
                for p1, p2 in wrap(outertopcoords):
                    lines.append((p1, p2))
                # outer sides and lines
                if m.group('slope') == 'Inverted Double Convex':
                    for (p1, p2), (p3, p4) in zip(wrap(outerbottomcoords)[:2], wrap(outertopcoords2)[:2]):
                        quads.append((p1,p2,p4,p3))
                    for (p1, p2), (p3, p4) in zip(wrap(outerbottomcoords)[1:2], wrap(outertopcoords2)[1:2]):
                        lines.append((p1,p3))
                elif m.group('slope') == 'Double Convex':
                    for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[:2], wrap(outerbottomcoords2)[:2]):
                        quads.append((p1,p2,p4,p3))
                    for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[1:2], wrap(outerbottomcoords2)[1:2]):
                        lines.append((p1,p3))
                elif m.group('slope') == 'Double Concave':
                    for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[1:5], wrap(outerbottomcoords2)[1:5]):
                        quads.append((p1,p2,p4,p3))
                    for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[2:5], wrap(outerbottomcoords2)[2:5]):
                        lines.append((p1,p3))
                else:
                    for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[:3], wrap(outerbottomcoords2)[:3]):
                        quads.append((p1,p2,p4,p3))
                    for (p1, p2), (p3, p4) in zip(wrap(outertopcoords)[1:3], wrap(outerbottomcoords2)[1:3]):
                        lines.append((p1,p3))
                # draw nose
                if m.group('slope') in ['Inverted Double Convex', 'Double Convex']:
                    quads.append(noseup1+[nosedown1[1]]+[nosedown1[0]])
                    quads.append(noseup2+[nosedown2[1]]+[nosedown2[0]])
                elif m.group('slope') != 'Double Concave':
                    quads.append(noseup+[nosedown[1]]+[nosedown[0]])
                # draw sides and lines to the nose
                if m.group('slope') == 'Inverted Double Convex':
                    quads.append(outerbottomcoords[-2:-1]+outertopcoords2[-2:-1]+nosedown2[:1]+noseup2[:1])
                    quads.append(outerbottomcoords[:1]+outertopcoords2[:1]+nosedown1[:1]+noseup1[:1])
                elif m.group('slope') == 'Double Convex':
                    quads.append(outertopcoords[-2:-1]+outerbottomcoords2[-2:-1]+noseup2[:1]+nosedown2[:1])
                    quads.append(outertopcoords[:1]+outerbottomcoords2[:1]+noseup1[:1]+nosedown1[:1])
                elif m.group('slope') == 'Double Concave':
                    quads.append(outertopcoords[-1:]+outerbottomcoords2[-1:]+tip)
                    quads.append(outertopcoords[1:2]+outerbottomcoords2[1:2]+tip)
                else:
                    quads.append(outertopcoords[-1:]+outerbottomcoords2[-1:]+nosedown[-1:]+noseup[-1:])
                    quads.append(outertopcoords[:1]+outerbottomcoords2[:1]+nosedown[:1]+noseup[:1])
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
                # draw slope and lines around it
                if m.group('slope') == 'Inverted':
                    quads.append(outerbottomcoords[-1:]+outerbottomcoords[:1]+[nosedown[1]]+[nosedown[0]])
                    lines.append(nosedown[:1]+outerbottomcoords[:1])
                    lines.append(nosedown[-1:]+outerbottomcoords[-1:])
                    lines.append(nosedown[:1]+nosedown[-1:])
                elif m.group('slope') == 'Inverted Double Convex':
                    quads.append(outerbottomcoords[-1:]+outerbottomcoords[:1]+[nosedown1[1]]+[nosedown1[0]])
                    quads.append(outerbottomcoords[2:3]+outerbottomcoords[3:4]+[nosedown2[1]]+[nosedown2[0]])
                    lines.append(nosedown1[:1]+outerbottomcoords[:1])
                    lines.append(nosedown1[-1:]+outerbottomcoords[-1:])
                    lines.append(nosedown2[-2:-1]+outerbottomcoords[-2:-1])
                    lines.append(nosedown1[:1]+nosedown1[-1:])
                    lines.append(nosedown2[:1]+nosedown2[-1:])
                elif m.group('slope') == 'Double Convex':
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
                    quads.append(outertopcoords[-1:]+outertopcoords[:1]+[noseup[1]]+[noseup[0]])
                    lines.append(noseup[:1]+outertopcoords[:1])
                    lines.append(noseup[-1:]+outertopcoords[-1:])
                    lines.append(noseup[:1]+noseup[-1:])
                # write inner top plate and lines
                if m.group('slope') == 'Double Concave':
                    quads.append(innertopcoords[:4])
                    quads.append(innertopcoords[3:]+innertopcoords[:1])
                else:
                    quads.append(innertopcoords)
                for p1, p2 in wrap(innertopcoords):
                    lines.append((p1, p2))
                # inner sides and lines
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
                # write out bottom with trapezoids and lines
                for (p1, p2), (p3, p4) in zip(wrap(innerbottomcoords), wrap(outerbottomcoords)):
                    quads.append((p1, p2, p4, p3))
                    lines.append((p1, p2))
                    lines.append((p3, p4))
        else:
            print "not supported part type: %s"%m.group('type')
            exit(1)
        outfile = open("parts/%s.dat"%partid, 'w')
        outfile.write("0 %s\n"%parttext)
        for (x1, y1, z1), (x2, y2, z2) in lines:
            outfile.write("2 24 %f %f %f %f %f %f\n"%(x1, y1, z1, x2, y2, z2))
        for (x1, y1, z1), (x2, y2, z2), (x3, y3, z3) in triangles:
            outfile.write("3 16 %f %f %f %f %f %f %f %f %f\n"%(
                x1, y1, z1, x2, y2, z2, x3, y3, z3))
        for (x1, y1, z1), (x2, y2, z2), (x3, y3, z3), (x4, y4, z4) in quads:
            outfile.write("4 16 %f %f %f %f %f %f %f %f %f %f %f %f\n"%(
                x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4))
        outfile.close()

if __name__ == "__main__":
    render()
