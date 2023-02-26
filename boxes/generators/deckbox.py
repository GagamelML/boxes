#!/usr/bin/env python3
# Copyright (C) 2013-2014 Florian Festi
# Copyright (C) 2018 jens persson <jens@persson.cx>
# Copyright (C) 2023 Manuel Lohoff
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import edges, Boxes


class InsetEdgeSettings(edges.Settings):
    """Settings for InsetEdge"""
    absolute_params = {
        "thickness": 0,
    }


class InsetEdge(edges.BaseEdge):
    """An edge with space to slide in a lid"""
    def __call__(self, length, **kw):
        t = self.settings.thickness
        self.corner(90)
        self.edge(t, tabs=2)
        self.corner(-90)
        self.edge(length, tabs=2)
        self.corner(-90)
        self.edge(t, tabs=2)
        self.corner(90)


class FingerHoleEdgeSettings(edges.Settings):
    """Settings for FingerHoleEdge"""
    absolute_params = {
        "wallheight": 0,
    }


class FingerHoleEdge(edges.BaseEdge):
    """An edge with room to get your fingers around cards"""
    def __call__(self, length, **kw):
        depth = self.settings.wallheight/5
        self.edge(length/2-10, tabs=2)
        self.corner(90)
        self.edge(depth, tabs=2)
        self.corner(-180, 10)
        self.edge(depth, tabs=2)
        self.corner(90)
        self.edge(length/2-10, tabs=2)


class DeckBox(Boxes):
    """Box for storage of playing card Decks, e.g. MTG or any other trading card game"""
    ui_group = "Box"

    description = """
#### Building instructions

Place inner walls on floor first (if any). Then add the outer walls. Glue the two walls without finger joins to the inside of the side walls. Make sure there is no squeeze out on top, as this is going to form the rail for the lid.

Add the top of the rails to the sides and the grip rail to the lid.

Details of the lid and rails

![Details](static/samples/CardBox-detail.jpg)

Whole box (early version still missing grip rail on the lid):
"""

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.argparser.add_argument(
            "--deckheight",  action="store", type=float, default=65,
            help="Hight of one stack of cards")
        self.argparser.add_argument(
            "--cardwidth",  action="store", type=float, default=68,
            help="Width of one card")
        self.argparser.add_argument(
            "--cardheight", action="store", type=float, default=92,
            help="Hight of one card")
        self.argparser.add_argument(
            "--num",  action="store", type=int, default=3,
            help="number of compartments")

    @property
    def boxwidth(self):
        return self.num * (self.deckheight + self.thickness) + self.thickness

    @property
    def boxdepth(self):
        return self.cardwidth + 2 * self.thickness

    @property
    def h(self):
        return self.cardheight

    def divider_bottom(self):
        t = self.thickness
        c = self.deckheight
        y = self.boxdepth

        for i in range(1, self.num):
            self.fingerHolesAt(0.5*t + (c+t)*i, 0, y, 90)

    def divider_back_and_front(self):
        t = self.thickness
        c = self.deckheight
        y = self.cardheight
        for i in range(1, self.num):
            self.fingerHolesAt(0.5*t + (c+t)*i, 0, y, 90)

    def render(self):
        h = self.h
        t = self.thickness

        x = self.boxwidth
        y = self.boxdepth
        c = self.deckheight

        s = InsetEdgeSettings(thickness=t)
        p = InsetEdge(self, s)
        p.char = "a"
        self.addPart(p)

        s = FingerHoleEdgeSettings(thickness=t, wallheight=h)
        p = FingerHoleEdge(self, s)
        p.char = "A"
        self.addPart(p)

        with self.saved_context():
            self.rectangularWall(x, y-t*.2, "eFee", move="right", label="Lid")
            self.rectangularWall(x, y, "ffff", callback=[self.divider_bottom],
                                 move="right", label="Bottom")
        self.rectangularWall(x, y, "eEEE", move="up only")
        self.rectangularWall(x, t, "feee", move="up", label="Lip Front")
        self.rectangularWall(x, t, "eefe", move="up", label="Lip Back")

        with self.saved_context():
            self.rectangularWall(x, h+t, "FfFf",
                                 callback=[self.divider_back_and_front],
                                 move="right",
                                 label="Back")
            self.rectangularWall(x, h+t, "FfFf",
                                 callback=[self.divider_back_and_front],
                                 move="right", 
                                 label="Front")
        self.rectangularWall(x, h+t, "EEEE", move="up only")


        with self.saved_context():
            self.rectangularWall(y, h+t, "FFEF", move="right", label="Outer Side Left")
            self.rectangularWall(y, h+t, "FFaF", move="right", label="Outer Side Right")
        self.rectangularWall(y, h+t, "fFfF", move="up only")

        with self.saved_context():
            self.rectangularWall(y, h, "Aeee", move="right", label="Inner Side Left")
            self.rectangularWall(y, h, "Aeee", move="right", label="Inner Side Right")
        self.rectangularWall(y, h, "eAee", move="up only")

        with self.saved_context():
            self.rectangularWall(y-t*.2, t, "fEeE", move="right", label="Lid Lip")
        self.rectangularWall(y, t*2, "efee", move="up only")

        for i in range(self.num - 1):
            self.rectangularWall(h, y, "fAff", move="right", label="Divider")

        for i in range(self.num):
            self.rectangularWall(c, h, "eeee", move="right", label="Front inlay")
            self.rectangularWall(c, h, "eeee", move="right", label="Back inlay")

        self.rectangularWall(x, y - 2*t, "eeee", move="right", label="Lid topper")
