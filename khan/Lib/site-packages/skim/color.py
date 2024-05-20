def generatecolors(numcols):
     """returns numcols saturated colors. returned colors are #000000 
     format"""
     hueoffset=.2 

     cols=[]
     for i in range(numcols):
         cols.append(rgbtohex(*hsv2rgb(hueoffset+1.0*i/
                                                   numcols,1,1)))
     return cols

def hsv2rgb(h,s,v):
    """Takes floats from 0..1 for each channel, returns r,g,b as
    0..255 ints.  (algorithm ported from
    http://aspn.activestate.com/ASPN/Cookbook/Tcl/Recipe/133527)"""
    if s<=0:
        return 255*v,255*v,255*v

    h=6.0*(h%1.0)
    f=h-int(h)
    p=int(255*v*(1.0-s))
    q=int(255*v*(1.0-(s*f)))
    t=int(255*v*(1.0-(s*(1.0-f))))
    v=int(255*v)

    return ((v,t,p),
            (q,v,p),
            (p,v,t),
            (p,q,v),
            (t,p,v),
            (v,p,q))[int(h)]

def desat(color,amt):
    """Returns desaturated color. amt=0 is no change, amt=1 is
    gray. all color values are 0..255"""
    c=hextorgb(color) # take apart color string if necessary
    v=1.0*(c[0]+c[1]+c[2])/3 # v is the brightness of the target gray
    b=1.0-amt # precalc the
    x=v*amt   # constants
    return rgbtohex(r=c[0]*b+x, # weighted average between
                          g=c[1]*b+x, # original color and the gray of 
                          b=c[2]*b+x) # matching brightness

def boost(color,amt):
    """amt=0 no effect, amt=1 raise to white"""
    c=hextorgb(color)
    return rgbtohex([max(0,min(255,c[i]+(255-c[i])*amt)) for i in range(3)])

def rgbtohex(*args):
    """(255,255,255)->#ffffff"""
    if len(args)==3:
        r,g,b=args
    elif len(args)==1:
        r,g,b=args[0]
    else:
        raise RuntimeError("rgbtohex takes r,g,b or (r,g,b)")

    return "#%02X%02X%02X" % (r,g,b)

def hextorgb(hexed):
    """#ffffff -> (255,255,255). non strings are passed through"""
    if isinstance(hexed,str):
        return int(hexed[1:3],16),int(hexed[3:5],16),int(hexed[5:7],16)
    else:
        return hexed

def safe(color):
    """returns the color (255,255,255) after possible brightening"""
    r,g,b=[x/255 for x in hextorgb(color)]
    val= 0.30*r + 0.59*g + 0.11*b # perceived brightness
    if val>.5:
        return [255*x for x in (r,g,b)]
    else:
        # disgusting brightness boost for colors that are too dark
        factor=.5-val
        newcolor=[255*(min(1,x+factor)) for x in r,g,b]
        return newcolor

     
