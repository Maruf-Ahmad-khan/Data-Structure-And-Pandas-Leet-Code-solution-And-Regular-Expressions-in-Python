#!/usr/bin/env python
"""
An alternative graphical text pager.  It allows you to quickly find clusters
of words.  To search for words, just click on them or type them in at the
entry bar at the top and press enter.

Todo pieces have been extracted to the TODO file.
"""

from __future__ import nested_scopes, division
import sys, os
from Tkinter import *
from zooming import Zooming
import color
import warnings

__version__ = "$Id: skim.py,v 1.4 2005/10/09 10:01:55 drewp Exp $"

# optional module import
if 0: # wordnet support jammed off for now, until we write it
    try: 
        if not os.environ.get('WNHOME'):
            os.environ["WNHOME"] = "/usr/local/WordNet-1.7.1"

        # from stdwn import impl
        # import wntools
        have_wordnet = 1
    except:
        print "Please install pywn from pywn.sourceforge.net (you'll also need to download the wordnet database and set WNHOME to its location"
        have_wordnet = 0

try:
    from shellwords import shellwords
    have_shellwords = 1
except:
    warnings.warn("If you want to search for search terms with spaces, you should install shellwords (http://www.crazy-compilers.com/py-lib/shellwords.html). If you have ez_setup, easy_install http://www.crazy-compilers.com/py-lib/python-shellwords-0.2.tar.gz",
                  stacklevel=2)
    have_shellwords = 0

def allsynonyms(word):
    syns=[]
    for synset in impl.lookupSynsetsByForm(word):
        for syn in synset.synonyms:
            form = syn.form.replace("_"," ")
            if form not in syns:
                syns.append(form)
    return syns

class Dummy:
    """This is the temporary Birdseye or Searchterms until those are set."""
    def dummy(self,*k,**kw):
        return
    def __getattr__(self,attr):
        print >>sys.stderr,"warning: requested %s on Dummy class" % attr
        return self.dummy

class Textview(Text):
    def __init__(self,*k,**kw):
        Text.__init__(self,*k,**kw)
        self.colortags={} # color:tagname
        self.serial=0

        self.birdseye=Dummy()
        self.st=Dummy()

        # This should be all the events that can cause a viewport change:
        self.bind("<Motion>",self.viewportchange)
        self.bind("<ButtonPress-1>",self.button1down)
        self.bind("<B1-ButtonRelease>",self.button1up)
        # Normally, double clicking would remove the term from the
        # search terms.  We presume the user was double clicking so they
        # could copy to the clipboard
        self.bind("<Double-1>",self.button1up) 

        self.bind("<4>",self.viewportchange)
        self.bind("<5>",self.viewportchange)
    def button1down(self,ev):
        self.b1downidx=self.index("@%i,%i" % (ev.x,ev.y))

    def button1up(self,ev):
        upidx=self.index("@%i,%i" % (ev.x,ev.y))
        if upidx==self.b1downidx:
            newterm=self.get("%s wordstart" % upidx,"%s wordend" % upidx)
        else:
            newterm=self.get(self.b1downidx,upidx)

        if newterm in self.st:
            self.st.deleteterm(newterm)
        else:
            self.st.addterm(newterm)
        
    def setsearchterms(self,st):
        self.st=st
        
    def viewportchange(self,*args):
        lastline=self.indextopos("end")[0]
        (f1,f2)=self.yview()
        self.birdseye.moveviewport(f1*lastline+1,f2*lastline+1)

    def movetop(self,topline):
        lastline=self.indextopos("end")[0]
        f=1.0*topline/lastline
        self.yview_moveto(f)
        self.viewportchange()
            
    def setbirdseye(self,be):
        "this text widget will send commands to a slave birdseye object"
        self.birdseye=be
        be.settextview(self)

    def fillwidget(self,lines):
        self.configure(state='normal')
        for l in lines:
            self.insert("end",l)
        self.configure(state='disabled')
        self.birdseye.wait_visibility()
        self.birdseye.setnumlines(len(lines))
        self.viewportchange()
            
    def tagforcolor(self,color):
        """returns a tagname that will tint the background color of text"""
        tagname=self.colortags.setdefault(color,self.serial)
        self.serial+=1
        
        self.tag_configure(tagname,background=color)
        return tagname

    def indextopos(self,ind):
        # normalize to line.char
        x=self.index(ind)
        i=x.find(".")
        # return (line,char) (line is still 1-based)
        return (int(x[:i]),int(x[i+1:]))
        
    def highlighttext(self, word, color="red"):
        """in textwidget tw, sets the background color of all matching words.
        always case-insens."""

        tag = self.tagforcolor(color)
        ind = "0.0"
        while 1:
            ind = self.search(word, "%s + 1 chars" % ind, "end")
            if ind == "":
                break
            indend = "%s + %i chars" % (ind,len(word))
            self.birdseye.addhighlight(self.indextopos(ind),
                                       self.indextopos(indend),color)
            self.tag_add(tag,ind,indend)
            
    def clearallhighlight(self):
        for tag in self.colortags.values():
            self.tag_remove(tag,"0.0","end")
        self.birdseye.clearallhighlight()


class Birdseye(Zooming):
    """
    the coordinate systems:
      pos    - (line,char) from the tcl index format, but as a tuple. 
               lines start with 1
      world  - the master coordinates of the zooming canvas
      canvas - the tk coordinates on the zooming canvas 
               (used in canvas methods, events, etc)
    """
    
    def __init__(self,*k,**kw):
        Zooming.__init__(self,bg="gray20",*k,**kw)
        self.create_rectangle(0,0,0,0,width=3,outline="green",tags="viewport")

        self.columnwidth=100 # width of a text column in pixels
        # (pos1,pos2,color) for each of the active highlights (they might 
        # not be drawn)
        self.highlights=[] 
        self.visiblelines=(0,0) # start,end line numbers

        self.draggingvp=0 # is the user currently dragging the viewport

        self.textview=Dummy() # link back to the master textview class

        # how many world units per greeked text line (which is always a 
        # 1pix-tall line)
        self.linespacing=2

        self.setupviewportscrolling()
        self.panbindings()
        self.zoombindings()
        self.addconstraint("left",">",0)
        self.addconstraint("right","<",self.columnwidth)
        self.addconstraint("top",">",0)
        self.addconstraint("sclx","==",1)
        self.addconstraint("scly","<",1.5)
        self.bind("<Configure>",self.updateconstraints)
        self.numlines=2

        # scrolling really should be moved to a generic place,
        # where one function receives Tk events, then handles
        # then in a consistent fashion: Modifiers should change
        # how scrolling works
        self.bind("<4>", self.scroll)
        self.bind("<5>", self.scroll)

    def scroll(self, ev):
        if ev.keycode == 5:
            self.textview.yview(SCROLL, 4, UNITS)
        elif ev.keycode == 4:
            self.textview.yview(SCROLL, -4, UNITS)
        self.textview.viewportchange()

    def settextview(self,tv):
        self.textview = tv
            
    def setupviewportscrolling(self):
        def b1press(self,ev):
            # all canvas coords
            vpcoords=self.coords("viewport")
            if (ev.x>vpcoords[0] and ev.x<vpcoords[2] and
                ev.y>vpcoords[1] and ev.y<vpcoords[3]):

                # remember how far into the vp the click was
                self.vpyoffset=ev.y-vpcoords[1] 
            else:
                self.vpyoffset=0
            self.draggingvp=1
            # update the viewport box right away, before any mousemove
            b1motion(self,ev)

        def b1motion(self,ev):
            if self.draggingvp:
                # user wants the top of the view to show this line:
                line = self.world2pos(self.canvas2world(ev.x,
                                      ev.y-self.vpyoffset))[0]
                self.textview.movetop(line)

        def b1release(self,ev):
            self.draggingvp=0

        self.bind("<ButtonPress-1>",lambda ev:b1press(self,ev))
        self.bind("<B1-Motion>",lambda ev:b1motion(self,ev))
        self.bind("<B1-ButtonRelease>",lambda ev:b1release(self,ev))

    def pos2world(self,pos):
        """converts (line,char) to world (x,y). This uses 1-based
        line numbers"""
        return (pos[1],(pos[0]-1)*self.linespacing)
    
    def world2pos(self,coord):
        """converts world (x,y) to (line,char). (1-based line numbers)"""
        return (coord[1]/self.linespacing+1, coord[0])

    def setnumlines(self,numlines):
        self.numlines=numlines
        self.updateconstraints()
        
    def updateconstraints(self,*args):
        # leave an attractive (i hope) space at the bottom
        fakenumlines = self.numlines
        
        self.delconstraint("bottom","<")
        self.addconstraint("bottom","<",self.pos2world((fakenumlines,0))[1])

        self.delconstraint("scly",">")
        if self.numlines>1 or 1:
            wbot = self.pos2world((fakenumlines,0))
            self.addconstraint("scly", ">", (self.winfo_height()+5) / wbot[1])

    def createposline(self,startpos,endpos,**kw):
        "creates a line in pos coordinates"
        c1=self.world2canvas(*self.pos2world(startpos))
        c2=self.world2canvas(*self.pos2world(endpos))
        return self.create_line(c1[0],c1[1],c2[0],c2[1],**kw)

    def addhighlight(self,pos1,pos2,color):
        self.highlights.append((pos1,pos2,color))
        if 1 or self.linevisible(pos1[0]):
            self.drawhighlight(pos1,pos2,color)
    
    def drawhighlight(self,pos1,pos2,color):
        self.createposline(pos1,pos2,fill=color,tag="highlight")

    def moveviewport(self,linestart,lineend):
        # (1-based lines)
        # find world coordinates of those lines
        (x,y1)=self.pos2world((linestart,0))
        (x,y2)=self.pos2world((lineend,0))
        # convert to canvas coords with the proper x values
        cc1=self.world2canvas(0+1,y1+2)
        cc2=self.world2canvas(self.columnwidth-2,y2-2)
        # adjust viewport canvas item
        self.coords(*(("viewport",) + cc1 + cc2))
    
    def greeked(self,lines):
        "draws greeked version of text in a canvas widget"
        skip=1
	maxlines=3000 # never draw more than this many lines
        if len(lines)>maxlines:
            skip = int(len(lines)/maxlines)
        for l,y in zip(lines,range(1,len(lines)+1)):
            if y%skip!=0:
                continue

            right=1+len(l)
            left=right-len(l.lstrip())
            self.createposline((y,left),(y,right),fill="gray40",tag="greek")
        self.tkraise("viewport","greek")
        self.setscale(0,0,1,1.0/skip)
    def clearallhighlight(self):
        self.delete("highlight")
        

class textfile:
    def __init__(self,filename):
        f=open(filename,"r")
        self.lines=f.readlines()


class Searchterms(Text):
    def __init__(self,*k,**kw):
        Text.__init__(self,height=1,*k,**kw)
        self.configure(font="arial 12")
        
        self.bind("<Return>",lambda x: self.update(readtext=1))
        
        self.lastknown=""
        self.terms=[] # list of current search terms
        self.changed = 0 # whether we have work to do

        self.textview=Dummy() # link to the Textview

    def settextview(self,tv):
        self.textview=tv

        bindings = {
            # some emacs bindings
            '<Control-n>' : ('yview', (SCROLL, 2, UNITS)),
            '<Control-p>' : ('yview', (SCROLL, -2, UNITS)),
            '<Control-v>' : ('yview', (SCROLL, 1, PAGES)),
            '<Alt-v>' :     ('yview', (SCROLL, -1, PAGES)),

            '<Up>' :        ('yview', (SCROLL, -2, UNITS)),
            '<Down>' :      ('yview', (SCROLL, 2, UNITS)),
            '<Alt-Left>' :  ('xview', (SCROLL, -2, UNITS)), # problems with this
            '<Alt-Right>' : ('xview', (SCROLL, 2, UNITS)), # this too

            '<Next>' :      ('yview', (SCROLL, 1, PAGES)),
            '<Prior>' :     ('yview', (SCROLL, -1, PAGES)),

            '<Home>' :      ('yview', (MOVETO, 0)),
            '<End>' :       ('yview', (MOVETO, 1)),

            # some vi/less-like bindings.  These are pretty silly and could
            # be replaced with more useful ones, should the keys be needed
            '<Control-j>' : ('yview', (SCROLL, 2, UNITS)),
            '<Control-k>' : ('yview', (SCROLL, -2, UNITS)),
            '<Control-d>' : ('yview', (SCROLL, 1, PAGES)),
            '<Control-u>' : ('yview', (SCROLL, -1, PAGES)),
            '<Control-l>' : ('xview', (SCROLL, 2, UNITS)),
            '<Control-h>' : ('xview', (SCROLL, -2, UNITS)),
            '<Control-H>' : ('yview', (MOVETO, 0)),
            '<Control-M>' : ('yview', (MOVETO, 0.5)),
            '<Control-L>' : ('yview', (MOVETO, 1)),
        }

        for k, cb in bindings.items():
            self.bind(k, lambda evt, cb=cb: self.scroll(*cb))

        self.bind('<Control-c>', lambda evt: root.destroy())
        self.bind('<Control-q>', lambda evt: root.destroy())
        self.bind('<Control-A>', self.zoom_all) # is this binding okay?
        
    def zoom_all(self, evt):
        self.textview.birdseye.zoom_all()
        
    def scroll(self, fn, args=None, kw=None):
        if not args: args = ()
        if not kw: kw = {}
        fns = {
            'xview' : self.textview.xview,
            'yview' : self.textview.yview,
        }
        apply(fns[fn], args, kw)
        self.textview.viewportchange()

        if fn == 'yview':
            if args == ('moveto', 1):
                self.textview.birdseye.move(0, -1e10)
            elif args == ('moveto', 0):
                self.textview.birdseye.move(0, 1e10)

    def update(self, readtext=0):
        """gets search terms, picks colors, and applies highlights to
        all the views"""
        if readtext:
            currenttext=self.get("0.0","end")
            if have_shellwords:
                currenttext = currenttext.strip().replace('"', '\"')
                newterms = shellwords(currenttext)
            else:
                newterms = currenttext.split()
            # we could send just the new/deleted terms to the
            # highlighter, but the text could get inconsistent if one
            # term is a substring of another
            self.terms = newterms
            self.changed = 1
        if self.changed:
            self.delete("0.0", "end")

            # insert still better color algorithm here
            numcols=len(self.terms)
            colors = []
            # min numcols, list of boosts to repeat through the sequence
            boostlevels=((0,[.2]), 
                         (5,[.4,.1]),
                         (10,[.5,-.1,.2]),
                         )
            # find the appropriate boost pattern
            for mincols,pattern in boostlevels:
                if numcols>=mincols:
                    boosts=pattern
                else:
                    break
                
            for col,boost in zip(color.generatecolors(numcols),
                                 boosts*int(numcols/len(boosts)+1)):
                colors.append(color.rgbtohex(color.safe(color.boost(col,boost))))

            self.textview.clearallhighlight()
            for term, col in zip(self.terms, colors):
                self.textview.highlighttext(term,col)

                if have_shellwords and ' ' in term:
                    quoted = 1
                else:
                    quoted = 0

                self.tag_configure(term, background=col)

                if quoted:
                    self.insert(END, '"')
                self.insert(END, term, (term,))
                if quoted:
                    self.insert(END, '"')
                self.insert(END, ' ')

            self.changed = 0
        
        # don't actually process the return key
        return "break"
    def addterm(self, newterm):
        # no empty terms and no multiline searches
        if not newterm.strip() or '\n' in newterm: return
        if newterm not in self:
            self.terms.append(newterm)
            self.changed = 1
            self.update()
    def deleteterm(self, newterm):
        if not newterm.strip(): return
        if newterm in self:
            self.terms.remove(newterm)
            self.changed = 1
            self.update()
    def __contains__(self, term):
        return term in self.terms

def cli():
    """Run from command line interface"""
    root=Tk()

    root.wm_geometry("700x850")

    birdseye = Birdseye(root,width=100)
    textview = Textview(root, wrap="none") # wrap="word" is good too
    searchterms = Searchterms(root)

    searchterms.pack(side=TOP, fill=X, expand=0)
    birdseye.pack(side=LEFT, fill=Y, expand=0)
    textview.pack(side=LEFT, fill=BOTH, expand=1)

    textview.setbirdseye(birdseye)
    textview.setsearchterms(searchterms)
    searchterms.settextview(textview)
    searchterms.focus()

    try:
        tf = textfile(sys.argv[1])
        root.wm_title("skim: %s" % sys.argv[1])
    except:
        root.wm_title("skim: %s" % "<stdin>")
        print >>sys.stderr, "skim: reading file from stdin"
        class stdinread:
            pass
        tf=stdinread
        tf.lines=sys.stdin.readlines()

    textview.fillwidget(tf.lines)
    birdseye.greeked(tf.lines)
    birdseye.zoom_all()

    root.mainloop()

if __name__ == '__main__':
    cli()
