#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import wx
import wx.grid
import Constants
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from ProcessNotebook import ProcessNotebook
from numpy import array, arange
from wxmplot.plotframe import PlotFrame
from mpldatacursor import datacursor
import logging

class QualityModel():
	def __init__(self, selectedAutoclave):
		self.selectedAutoclave = selectedAutoclave
		return

	def GetDatesList(self, startDate, finalDate, orderNumber):
		dates_list = []
		self.starting_points = []

		
		if(orderNumber == ''):
			#Filtramos por fechas
			engine = create_engine(Constants.DATABASE_PATH, echo=False)
			Session = sessionmaker(bind=engine)
			session = Session()
			selected_table = Constants.Autoclave_dict[self.selectedAutoclave]
			self.starting_points = session.query(selected_table).filter(selected_table.Fecha >= startDate,
									selected_table.Fecha <= finalDate,
									selected_table.Start_status == 1).all()

			
		else:
			#Filtramos por numero de orden
			engine = create_engine(Constants.DATABASE_PATH, echo=False)
			Session = sessionmaker(bind=engine)
			session = Session()
			selected_table = Constants.Autoclave_dict[self.selectedAutoclave]
			self.stopping_points = []
			self.orderNumber = int(orderNumber)
			next_stopping_point = session.query(selected_table).first()
			
			while(1):
			
				self.orderNumber_found = session.query(selected_table).filter(selected_table.id > next_stopping_point.id).filter(
											or_(selected_table.Producto1 == self.orderNumber,
											    selected_table.Producto2 == self.orderNumber,
											    selected_table.Producto3 == self.orderNumber,
											    selected_table.Producto4 == self.orderNumber,
											    selected_table.Producto5 == self.orderNumber,
											    selected_table.Producto6 == self.orderNumber)).first()
							
				if(self.orderNumber_found == None):
					logging.debug('No more orderNumbers found')
					break

				previous_starting_point = session.query(selected_table).filter(selected_table.id <= self.orderNumber_found.id,
									selected_table.Start_status == 1).order_by(selected_table.id.desc()).first()

				next_stopping_point = session.query(selected_table).filter(selected_table.id >= self.orderNumber_found.id,
									selected_table.End_status == 1).first()

				if(next_stopping_point == None):
					logging.debug('No more stopping_points')
					break

				self.starting_points.append(previous_starting_point)
				

		for i in range(len(self.starting_points)):
			dates_list.append(self.starting_points[i].Fecha)

		return dates_list


	def DynamicButtonHandler(self, evt):
		button = evt.GetEventObject()	

		#Aqui hacer queries	
		engine = create_engine(Constants.DATABASE_PATH, echo=False)
		Session = sessionmaker(bind=engine)
		session = Session()
		selected_table = Constants.Autoclave_dict[self.selectedAutoclave]
		stopping_point = session.query(selected_table).filter(selected_table.id >= (self.starting_points[button.GetId()].id + 1),
								     selected_table.End_status == 1).first()

		results = session.query(selected_table).filter(selected_table.id >= (self.starting_points[button.GetId()].id), 
							      selected_table.id <= (stopping_point.id -1)).all()

		Presion1_plot_array 	= []
		Presion2_plot_array 	= []
		PresionInt_plot_array 	= []
		Temperatura_plot_array	= []
		
		for row in results:
			Presion1_plot_array.append(row.Presion1)
			Presion2_plot_array.append(row.Presion2)
			PresionInt_plot_array.append(row.Presion_interior)
			Temperatura_plot_array.append(row.Temperatura)

		self.processNotebook = ProcessNotebook(results, self.selectedAutoclave, results[0].Fecha,
						results[0].Hora, results[len(results) - 1].Hora)
		self.processNotebook.Show()
		self.processNotebook.Maximize(True)



class QualityFrame(wx.Frame):
	def __init__(self, startDate, finalDate, orderNumber, selectedAutoclave):
		wx.Frame.__init__(self, parent=None, id=-1, title=Constants.QUALITY_FRAME_TITLE, 
				pos=Constants.RESULTS_FRAME_POS, size=Constants.RESULTS_FRAME_SIZE)

		self.MainPanel = wx.Panel(self, id=-1)
		self.startDate = startDate
		self.finalDate = finalDate
		self.orderNumber = orderNumber
		self.qualityModel = QualityModel(selectedAutoclave)
		self.PanelInit()

	def PanelInit(self):

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.dates_list = self.qualityModel.GetDatesList(self.startDate, self.finalDate, self.orderNumber)				
		
		for i in range(len(self.dates_list)):
			rowSizer 	= wx.BoxSizer(wx.HORIZONTAL)
			rowData_string  = self.dates_list[i] + " - %.2d" % (i+1)
			rowData_label 	= wx.StaticText(self.MainPanel, -1, rowData_string)
			row_button 	= wx.Button(self.MainPanel, i, Constants.DYNAMIC_BUTTON_TITLE, size=(120, 26))
			self.Bind(wx.EVT_BUTTON, self.OnClick_DynamicButton, row_button)

			rowSizer.Add(rowData_label, 0,wx.CENTER, 3)
			rowSizer.Add(row_button, 0,wx.LEFT, 45)
			mainSizer.Add(rowSizer, 0,wx.ALL, 5)
		
		self.MainPanel.SetSizer(mainSizer)
		mainSizer.Fit(self)

	def OnClick_DynamicButton(self, event):
		self.qualityModel.DynamicButtonHandler(event)
