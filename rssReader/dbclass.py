#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       dbclass.py       
#       
#  Copyright 2013 Sergio Morlans <https://github.com/ikkipower/CRUD.git>
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

from math import sqrt
import MySQLdb 

class Dbclass:

#Common functions

      def __init__ (self,dbname,dbuser,dbpasswd):
		  self.dbname = dbname
		  self.dbuser = dbuser
		  self.dbpasswd = dbpasswd
		  
      def connect(self):
         print "Dbclass created"
         self.mycon = MySQLdb.connect(host='localhost', user='rssuser',passwd='rss', db='RSSdata')
         self.micursor = self.mycon.cursor(MySQLdb.cursors.DictCursor);
         print "Dbclass connected"     
 
      def disconnect(self):
         self.micursor.close()
         self.mycon.commit()  
 
#Functions called from Pipeline      
      def insData(self,insTitRss, insDescRss, insLinkRss, insTitItem, insDescItem, insLinkItem):
											                                                              
         query = "INSERT INTO entrada (TitRss, DescRss, LinkRss, TitItem, DescItem, LinkItem) VALUES (\""+insTitRss+"\",\""+insDescRss+"\",\""+insLinkRss+"\",\""+insTitItem+"\",\""+insDescItem+"\",\""+insLinkItem+"\")" 
                                                                                          
         
         self.micursor.execute(query)
         self.mycon.commit() 

      def showTituloItem(self):

         query= "SELECT TitItem FROM entrada WHERE 1;" 
         self.micursor.execute(query)
         self.mycon.commit()      
         registro = self.micursor.fetchall()      
         
         aux = []
         for p in registro:
			 aux.append(p['TitItem'])
         return aux

#functions called from rssReader.py


#      def delData(self,cId,cname):
         
#         query = "DELETE FROM ships WHERE Id = "+cId+" AND Clase =\""+cname+"\";"
#         self.micursor.execute(query)
#         self.mycon.commit() 
      
      def showData(self, delid,ctitname):
        
         query= "SELECT * FROM entrada WHERE Id = "+delid+" AND TitItem =\""+ctitname+"\";" 
         self.micursor.execute(query)   
         self.mycon.commit()   
         registro = self.micursor.fetchone()
        
         # Imprimimos el registro resultante
         print registro    
         return registro
         

      def listDataClase(self):
         query= "SELECT Id,TitItem FROM entrada WHERE 1;" 
         self.micursor.execute(query)
         self.mycon.commit()      
         registro = self.micursor.fetchall()      
         print "listDataClase"
         return registro
           



