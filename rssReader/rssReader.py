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

from gi.repository import Gtk, GdkPixbuf, Gdk, GObject

import os, sys
import re
from dbclass import Dbclass
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy import log

from rssReader.spiders.rssSpider import RssSpider

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
		                 "onDBActivate": self.onDBActivate,
		                 "onButtonPressed": self.onButtonPressed,
		                 "onbtnUpClicked": self.onbtnUpClicked,
		                 "onbtnCancelClicked": self.onbtnCancelClicked
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
		self.button1 = self.builder.get_object("eliBtn")
		self.button1.set_sensitive(False)

		#progress bar
		self.prog = self.builder.get_object("progbar")

		
		self.builder.connect_signals(self.handlers)
		
		self.window = self.builder.get_object("rssWindow")
		self.window.show_all()

    def onCombochanged(self,box):
		#Visualizar primero los datos antes de eliminar
     
        tree_iter = box.get_active_iter()
        if tree_iter != None:
			model = box.get_model()
			self.delTitRss = model[tree_iter][0]
			self.delid = model[tree_iter][1]

			for cmp in self.lista:
				if str(cmp["Id"]) == self.delid:

					reg = self.dbobj.showData(str(cmp["Id"]))
					break

			self.fillTextbox(reg)

    def onButtonPressed(self,button):
		   
		self.dbobj.delData(self.delid)
		self.status_bar.push(0, "Datos eliminados")
			   
		self.fillCombobox() 
		self.clearTextbox()

    def onDBActivate(self,menuitem):

		self.status_bar.push(0, menuitem.get_label())
		#Sacando información en la barra de estado
		self.action = menuitem.get_label()
	
		if self.action == "Visualizar":
			self.visualizarData()
		else:
			self.eliminarData()
	
    def visualizarData(self):
		self.opt = "1"
		self.clearTextbox()
		self.viselcomb.set_sensitive(True)	
		self.fillCombobox()
	
    def eliminarData(self):
		self.opt = "2"
		self.clearTextbox()
		self.viselcomb.set_sensitive(True)
		self.fillCombobox()		

    def clearTextbox(self):
		self.namRss.get_buffer().set_text("")
		self.linkRss.set_uri("")
		self.descRss.get_buffer().set_text("")
		self.namItem.get_buffer().set_text("")
		self.linkRss.set_uri("")
		self.descItem.get_buffer().set_text("")
		#print "clearTextbox self.button1.set_sensitive(False)"
		self.button1.set_sensitive(False)
		self.viselcomb.set_sensitive(False)

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
		if self.opt == "1":
			self.button1.set_sensitive(False)	
		elif self.opt == "2":
			self.button1.set_sensitive(True)			
		
		cmplist = ["TitRss","DescRss","LinkRss","TitItem","DescItem","LinkItem"]                
		for cmp in datalist:
			if cmp == "TitRss":				
				self.namRss.get_buffer().set_text(self.filtrarhtml(str(datalist[cmplist[0]]).decode('unicode-escape').encode('utf-8')))
			elif cmp == "DescRss":
				self.descRss.get_buffer().set_text(self.filtrarhtml(str(datalist[cmplist[1]]).decode('unicode-escape').encode('utf-8')))
			elif cmp == "LinkRss": 
				self.linkRss.set_uri(str(datalist[cmplist[2]]).decode('unicode-escape').encode('utf-8'))
			elif cmp == "TitItem":
				self.namItem.get_buffer().set_text(self.filtrarhtml(str(datalist[cmplist[3]]).decode('unicode-escape').encode('utf-8')))
 			elif cmp == "DescItem":
				self.descItem.get_buffer().set_text(self.filtrarhtml(str(datalist[cmplist[4]]).decode('unicode-escape').encode('utf-8')))
			elif cmp == "LinkItem":
				self.linkItem.set_uri(str(datalist[cmplist[5]]).decode('unicode-escape').encode('utf-8'))	


    def onDBUpdate(self,menuitem):
		#print "onDBUpdate self.button1.set_sensitive(True)"
		self.button1.set_sensitive(False)  
		self.upd = self.builder.get_object("UpdateDialog")
		self.upd.show_all()
		
    def onbtnCancelClicked(self,button):
		self.upd = self.builder.get_object("UpdateDialog")
		self.upd.hide()  
		
    def onbtnUpClicked(self,button):
        #spider = RssSpider(domain='elperiodico.com')
        #crawler = Crawler(get_project_settings())
        #crawler.configure()
        
        #crawler.crawl(spider)
        #crawler.signals.connect(self.stop_reactor,signals.engine_stopped)
        #crawler.start()
        
        #reactor.run()
        os.system("scrapy crawl spiRss")
			
        self.status_bar.push(0, "Base De Datos Actualizada")
        self.upd = self.builder.get_object("UpdateDialog")
        self.upd.hide()          		
		
    def onAboutDialog(self, *args):
        self.about = self.builder.get_object("aboutdialog1")
        self.about.show_all()
    
    def onCloseAbout(self, *args):
        self.about = self.builder.get_object("aboutdialog1")
        self.about.hide()  
              
    def destroy(self,window):	     	
		self.dbobj.disconnect()
		Gtk.main_quit()

    #def stop_reactor(self):
 
        #print "jojo" #reactor.stop() #Stops reactor to prevent script from hanging
  
    def filtrarhtml(self,string):
        sr = re.search('<.*>', string)
        if sr == None:
			return string
        if ((len(string)-1)==sr.end):  #tag acaba con el string
			if sr.start()==0:  #tag es todo el string
				return ""
			else:
				return string[:sr.start()]  #texto delante
        else:
			if sr.start()==0:  #tag empiza string	
				return string[sr.end():]
			else:			
				return string[:sr.start()]+string[sr.end():]  #texto delante      

def main():
    app = RSS_GUI()
    Gtk.main()

if __name__ == "__main__":
    main()

