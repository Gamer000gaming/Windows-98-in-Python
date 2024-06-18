#-------------------------------------------------------------------------------
# Name:        Demineur Tk Spm v1.5
# Purpose:     Education Game
#
# Author:      Serge Smeesters, alias Spaceeman
#
# Created:     2023-02-18
# Copyright:   (c) Serge Smeesters 2023
# Licence:     GPL3
#-------------------------------------------------------------------------------

import tkinter as Tk
import re
import random as R


class Case :
    size = 0
    def __init__( self, li, ci, bombe=False, connu=False, nba=0, drapeau=0 ) :
        (self.li, self.ci) = (li, ci)
        self.bombe = bombe
        self.connu = connu
        self.nba = nba
        self.drapeau = drapeau
        self.ditems = list()

    def __del__(self) :
        if self.ditems : cv.delete( *self.ditems )

    def explorer1( self ) :
        if self.connu or (0 < self.drapeau) : return
        self.connu = True
        self.draw()
        if self.bombe or (0 < self.nba) : return
        for dl in (-1, 0, 1) :
            for dc in (-1, 0, 1) :
                c = case(self.li+dl, self.ci+dc)
                if c : c.explorer()

    def explorer( self ) :
        toexp = set([(self.li,self.ci)])
        while toexp :
            li,ci = toexp.pop()
            c = case(li,ci)
            if c.connu or (0 < c.drapeau) : continue
            c.connu = True
            c.draw()
            if c.bombe or (0 < c.nba) : continue
            for dl in (-1, 0, 1) :
                for dc in (-1, 0, 1) :
                    c = case( li+dl, ci+dc )
                    if c : toexp.add( (c.li, c.ci ) )


    def placer_drapeau( self ) :
        if not self.connu :
            self.drapeau +=1
            if 2 < self.drapeau : self.drapeau = 0
            self.draw()

    def draw(self) :
        size = Case.size
        x, y = self.ci*size, self.li*size
        (txtcouleur, txt) = ("black", "")

        if self.connu and self.bombe :
            (couleur, txtcouleur, txt) = ("#F88", "#F00", "✹")
        elif self.connu and self.nba < 1 :
            (couleur, txtcouleur, txt) = ("#EEE", "#000", " ")
        elif self.connu and self.nba > 0 :
            gb = int(238 - 68 * self.nba / 8)
            (couleur, txtcouleur, txt) = (
                "#FF%02X%02X"%(gb,gb), "#000", str( self.nba )[0] )
        elif not self.connu and self.drapeau == 0 :
            (couleur, txtcouleur, txt) = ("#AAA", "#888", "░")
        elif not self.connu and self.drapeau == 1 :
            (couleur, txtcouleur, txt) = ("#FAA", "#F00", "✘")
        elif not self.connu and self.drapeau == 2 :
            (couleur, txtcouleur, txt) = ("#AAF", "#D00", "?")
        if self.ditems : cv.delete( *self.ditems )
        self.ditems.append(
            cv.create_rectangle( x, y, x+size, y+size, fill=couleur) )
        self.ditems.append(
            cv.create_text( x + (size/2), y + (size/2),
                text=txt, font=('DejaVu Sans', int(size/2), 'bold'),
                fill=txtcouleur ) )

def initialise( l, h, nb ) :
    global largeur, hauteur, nbombes, nbcases, cases, entry
    largeur = min( 96, max( 4, l ) )
    hauteur = min( 64, max( 4, h ) )
    nbcases = largeur * hauteur
    nbombes = min( nbcases -1, max( 1, nb ) )
    entry.delete(0,Tk.END)
    entry.insert(0, "%ix%i+%i"%(largeur, hauteur, nbombes) )

    cases = list()
    (ncr,nbr) = (nbcases, nbombes)
    for li in range( hauteur ) :
        ligne_de_cases = list()
        for ci in range( largeur ) :
            if R.randrange( ncr ) < nbr :
                bombe = True
                nbr -= 1
            else :
                bombe = False
            ligne_de_cases.append( Case( li, ci, bombe ) )
            ncr -= 1
        cases.append( ligne_de_cases )
    calculer_alentours()
    draw_cases()
    title_info()


def case( li, ci ) :
    if li < 0 or ci < 0 or largeur <= ci or hauteur <= li :
        return False
    return cases[li][ci]


def calculer_alentours() :
    for li in range( hauteur ) :
        for ci in range( largeur ) :
            nba = 0
            for dl in range(-1,2) :
                for dc in range(-1,2) :
                    if (dl != 0) or (dc != 0) :
                        c = case( li+dl, ci+dc )
                        if c and c.bombe : nba += 1
            cases[li][ci].nba = nba


def draw_cases() :
    vals = re.split("[x,+]", cv.winfo_geometry() )
    (cw,ch) = ( int( vals[0] ), int( vals[1] ) )
    Case.size = min( cw / largeur, ch / hauteur )
    for li in range( hauteur ) :
        for ci in range( largeur ) :
            cases[li][ci].draw()


def title_info() :
    nbd = 0
    for li in range( hauteur ) :
        for ci in range( largeur ) :
            c = cases[li][ci]
            if c.drapeau == 1 or (c.connu and c.bombe) : nbd += 1
    rb = nbombes - nbd
    root.title( "Demineur, encore %i à trouver sur les %i"%(rb, nbombes) )


def input_config_visible( visible=True ) :
    global entry, entry_cv_id, lastw
    if visible and not entry_cv_id :
        entry_cv_id = cv.create_window(lastw/2, 32, window=entry)
    elif not visible and entry_cv_id :
        cv.delete( entry_cv_id )
        entry_cv_id = None


def input_config_valid( event ) :
    global entry, entry_cv_id
    if not entry_cv_id : return
    try :
        vals = re.split("[x,+]", entry.get() )
        (cw,ch,nb) = ( int( vals[0] ), int( vals[1] ), int( vals[2] ) )
    except :
        (cw,ch,nb) = (32, 16, 99)
    initialise( cw, ch, nb )
    input_config_visible( False )


def click(event) :
    if event.num == 2 and not entry_cv_id :
        input_config_visible( True )
    else :
        input_config_visible( False )
        (x, y, size) = ( event.x, event.y, Case.size )
        c = case( int( y / size ), int( x / size ) )
        if c :
            if event.num == 1 : c.explorer()
            elif event.num == 3 : c.placer_drapeau()
            title_info()


(lastw, lasth) = (0, 0)
def reconf(event) :
    global lastw, lasth
    gstr = cv.winfo_geometry()
    vals = re.split("[x,+]", gstr)
    (cw,ch) = ( int( vals[0] ), int( vals[1] ) )
    if (cw, ch) == (lastw, lasth) : return
    lastw, lasth = cw, ch
    draw_cases()

def main(root):
    root.columnconfigure( 0, weight=1 )
    root.rowconfigure( 0, weight=1 )
    cv = Tk.Canvas( root )
    cv.grid( column=0, row=0, sticky=(Tk.N, Tk.W, Tk.E, Tk.S) )

    entry = Tk.Entry( root )
    entry.bind("<KP_Enter>", input_config_valid)
    entry.bind("<Return>", input_config_valid)
    entry.bind("<Escape>", click )
    entry.focus()
    entry_cv_id=None

    cv.bind("<Button-1>", click)
    cv.bind("<Button-2>", click)
    cv.bind("<Button-3>", click)
    root.bind("<Configure>", reconf)

    initialise(10, 10, 20)
    root.mainloop()

root = Tk.Tk()
main(root)
