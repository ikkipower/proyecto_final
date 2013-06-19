#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rssReader.py
#       
#  Copyright 2013 Sergio Morlans <https://github.com/ikkipower/proyecto_final>
#       
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#       
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#       
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

from gi.repository import Gtk, GdkPixbuf, Gdk

import os, sys

sys.path.append('./rssReader')
from dbclass import Dbclass

import MySQLdb 
import types

class RSS_GUI:
	
    def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file("./glade/rss.glade")
		self.handlers = {"onDeleteWindow": Gtk.main_quit,
		                 "onAboutDialog": self.onAboutDialog,
		                 "onCloseAbout": self.onCloseAbout,
		                 "onDBUpdate": self.onDBUpdate,
		                 "onCombochanged" : self.onCombochanged,
		                 "onDBActivate": self.onDBActivate
                         }

		self.namRss = self.builder.get_object("namRss")
		self.linkRss = self.builder.get_object("linkRss")
		self.descRss = self.builder.get_object("descRss")
		self.namItem = self.builder.get_object("namItem")
		self.linkItem = self.builder.get_object("linkItem")
		self.descItem = self.builder.get_object("descItem")


        #inicializar la base de datos, conectandola
		self.dbobj = Dbclass('RSSdata','rssuser','rss')
		self.dbobj.connect()
        
        #combobox
		self.viselcomb = self.builder.get_object("combobox1")
		self.viselcomb.set_sensitive(False) #solo activo en los menus eliminar y visualizar

        #cogemos la barra de estado
		self.status_bar = self.builder.get_object("statusbar1")
		self.status_bar.push(0, "Conectado a la base de datos")

        #boton inicialmente desactivado
		self.button1 = self.builder.get_object("Button")
		self.button1.set_sensitive(False)  
      
        
		self.builder.connect_signals(self.handlers)
		
		self.window = self.builder.get_object("rssWindow")
		print self.window.get_size()
		self.window.show_all()

    def onCombochanged(self,box):
		#Visualizar primero los datos antes de eliminar
     
        tree_iter = box.get_active_iter()
        if tree_iter != None:
			model = box.get_model()
			self.delTitRss = model[tree_iter][0]
			self.delid = model[tree_iter][1]

			for cmp in self.lista:
				print "+++++++++++++++++"
				print type(cmp["TitItem"])
				print cmp["TitItem"]
				if cmp["TitItem"].decode('unicode-escape').encode('utf-8') == self.delTitRss:

					reg = self.dbobj.showData(str(cmp["Id"]),cmp["TitItem"])
					print "igual"
					print cmp
					break
				else:
				    print "no igual"
				    print cmp 
				    
			
			
			print reg
			self.fillTextbox(reg)

    def onButtonPressed(self,button):
		   self.dbobj.delData(self.delid,self.delTitRss)
		   self.status_bar.push(0, "Datos eliminados")

    def onDBActivate(self,menuitem):

		self.status_bar.push(0, menuitem.get_label())
		#Sacando información en la barra de estado
		self.action = menuitem.get_label()
	
		if self.action == "Visualizar":
			
			self.visualizarData()
		else:
			self.eliminarData()
	
    def visualizarData(self):
		self.clearTextbox()
		self.viselcomb.set_sensitive(True)
		self.button1.set_sensitive(False)	
		self.fillCombobox()
	
    def eliminarData(self):
		self.clearTextbox()
		self.viselcomb.set_sensitive(True)
		self.button1.set_sensitive(True)	
		self.fillCombobox()		

    def clearTextbox(self):
		self.namRss.get_buffer().set_text("")
		self.linkRss.set_uri("")
		self.descRss.get_buffer().set_text("")
		self.namItem.get_buffer().set_text("")
		self.linkRss.set_uri("")
		self.descItem.get_buffer().set_text("")

		

    def fillCombobox(self):
        store = Gtk.ListStore(str,str)
        self.lista = self.dbobj.listDataClase()
        
        store.clear()
        self.viselcomb.clear()
        #llenamos el combobox
        for cmp in self.lista:
			store.append([cmp["TitItem"].decode('unicode-escape').encode('utf-8'),str(cmp["Id"])])

        self.viselcomb.set_model(store)
        cell = Gtk.CellRendererText()
        self.viselcomb.pack_start(cell, True)
        self.viselcomb.add_attribute(cell, 'text', 0)
    
    def fillTextbox(self, datalist):
		
		print "filltextbox"
		cmplist = ["TitRss","DescRss","LinkRss","TitItem","DescItem","LinkItem"]                
		for cmp in datalist:
			if cmp == "TitRss":
				self.namRss.get_buffer().set_text(str(datalist[cmplist[0]]).decode('unicode-escape').encode('utf-8'))
			elif cmp == "DescRss":
				self.descRss.get_buffer().set_text(str(datalist[cmplist[1]]).decode('unicode-escape').encode('utf-8'))
			elif cmp == "LinkRss": 
				self.linkRss.set_uri(str(datalist[cmplist[2]]).decode('unicode-escape').encode('utf-8'))
			elif cmp == "TitItem":
				self.namItem.get_buffer().set_text(str(datalist[cmplist[3]]).decode('unicode-escape').encode('utf-8'))
 			elif cmp == "DescItem":
				self.descItem.get_buffer().set_text(str(datalist[cmplist[4]]).decode('unicode-escape').encode('utf-8'))
			elif cmp == "LinkItem":
				self.linkItem.set_uri(str(datalist[cmplist[5]]).decode('unicode-escape').encode('utf-8'))	



    def onDBUpdate(self,menuitem):
		print "Update"
		#os.system("./rssReader/scrapy crawl spiRss")
			     	
		
    def onAboutDialog(self, *args):
        self.about = self.builder.get_object("aboutdialog1")
        self.about.show_all()
    
    def onCloseAbout(self, *args):
        self.about = self.builder.get_object("aboutdialog1")
        self.about.hide()  
              
    def destroy(self,window):	     	
		self.dbobj.disconnect()
		Gtk.main_quit()

def main():
    app = RSS_GUI()
    Gtk.main()

if __name__ == "__main__":
    main()

