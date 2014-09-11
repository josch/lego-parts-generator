#!/usr/bin/env python

from __future__ import print_function

import sys
import os
import itertools
from functools import cmp_to_key

def transform(u,v,w,tm):
    x,y,z,a,b,c,d,e,f,g,h,i = tm
    return (a*u + b*v + c*w + x),(d*u + e*v + f*w + y),(g*u + h*v + i*w + z)

def handle_file(fname,lines,triangles,quads):
    with open(fname) as f:
        for line in f:
            t = line.split()
            if t[0] == '0':
                continue
            elif t[0] == '1':
                c = int(t[1])
                if c != 16:
                    print("no support for sub-files with other colors than 16", file=sys.stderr)
                    exit(1)
                tm = [float(x) for x in t[2:-1]]
                dn = os.path.dirname(fname)
                fname2 = os.path.join(dn,t[-1])
                lines2 = list()
                triangles2 = list()
                quads2 = list()
                handle_file(fname2,lines2,triangles2,quads2)
                # now apply the give transformation to the new lines, triangles and quads
                for c,x1,y1,z1,x2,y2,z2 in lines2:
                    x1,y1,z1 = transform(x1,y1,z1,tm)
                    x2,y2,z2 = transform(x2,y2,z2,tm)
                    lines.append((c,x1,y1,z1,x2,y2,z2))
                for c,x1,y1,z1,x2,y2,z2,x3,y3,z3 in triangles2:
                    x1,y1,z1 = transform(x1,y1,z1,tm)
                    x2,y2,z2 = transform(x2,y2,z2,tm)
                    x3,y3,z3 = transform(x3,y3,z3,tm)
                    triangles.append((c,x1,y1,z1,x2,y2,z2,x3,y3,z3))
                for c,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4 in quads2:
                    x1,y1,z1 = transform(x1,y1,z1,tm)
                    x2,y2,z2 = transform(x2,y2,z2,tm)
                    x3,y3,z3 = transform(x3,y3,z3,tm)
                    x4,y4,z4 = transform(x4,y4,z4,tm)
                    quads.append((c,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4))
            elif t[0] == '2':
                c = int(t[1])
                x1,y1,z1,x2,y2,z2 = [float(x) for x in t[2:]]
                lines.append((c,x1,y1,z1,x2,y2,z2))
            elif t[0] == '3':
                c = int(t[1])
                x1,y1,z1,x2,y2,z2,x3,y3,z3 = [float(x) for x in t[2:]]
                triangles.append((c,x1,y1,z1,x2,y2,z2,x3,y3,z3))
            elif t[0] == '4':
                c = int(t[1])
                x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4 = [float(x) for x in t[2:]]
                quads.append((c,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4))
            else:
                print("unknown line type: %s"%t[0], file=sys.stderr)
                exit(1)

def normalize_l(c,x1,y1,z1,x2,y2,z2):
    if (x1,y1,z1) < (x2,y2,z2):
        return (c,x1,y1,z1,x2,y2,z2)
    else:
        return (c,x2,y2,z2,x1,y1,z1)

def normalize_t(c,x1,y1,z1,x2,y2,z2,x3,y3,z3):
    # since winding order does not matter, we just sort
    pts = sorted([(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)])
    x1,y1,z1,x2,y2,z2,x3,y3,z3 = itertools.chain.from_iterable(pts)
    return (c,x1,y1,z1,x2,y2,z2,x3,y3,z3)

def rotate(cycle):
    tcmp = lambda a,b: cmp(a[1],b[1])
    smallest_idx = min(enumerate(cycle), key=cmp_to_key(tcmp))[0]
    return cycle[smallest_idx:]+cycle[:smallest_idx]

def normalize_q(c,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4):
    # rotate the smallest coordinate to the front
    pts = rotate([(x1,y1,z1),(x2,y2,z2),(x3,y3,z3),(x4,y4,z4)])
    # winding order does not matter, so deciding whether or not the next point
    # is the second or last, we pick the smallest
    if pts[1] > pts[3]:
        pts = [pts[0],pts[3],pts[2],pts[1]]
    x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4 = itertools.chain.from_iterable(pts)
    return (c,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4)

if __name__ == '__main__':
    lines = list()
    triangles = list()
    quads = list()
    handle_file(sys.argv[1],lines,triangles,quads)
    # now normalize the lines, triangles and quads
    lines = [ normalize_l(*x) for x in lines]
    triangles = [ normalize_t(*x) for x in triangles]
    quads = [ normalize_q(*x) for x in quads]
    # now output the normalized values
    with open(os.path.join(sys.argv[2],os.path.basename(sys.argv[1])), "w") as outfile:
        # we round to six digits and add zero to avoid printing a negative zero
        for c,x1,y1,z1,x2,y2,z2 in sorted(lines):
            x1,y1,z1,x2,y2,z2 = [round(t,6)+0 for t in x1,y1,z1,x2,y2,z2]
            outfile.write("2 %d %s %s %s %s %s %s\n"%(c,x1,y1,z1,x2,y2,z2))
        for c,x1,y1,z1,x2,y2,z2,x3,y3,z3 in sorted(triangles):
            x1,y1,z1,x2,y2,z2,x3,y3,z3 = [round(t,6)+0 for t in x1,y1,z1,x2,y2,z2,x3,y3,z3]
            outfile.write("3 %d %s %s %s %s %s %s %s %s %s\n"%(c,x1,y1,z1,x2,y2,z2,x3,y3,z3))
        for c,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4 in sorted(quads):
            x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4 = [round(t,6)+0 for t in x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4]
            outfile.write("4 %d %s %s %s %s %s %s %s %s %s %s %s %s\n"%(c,x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4))
