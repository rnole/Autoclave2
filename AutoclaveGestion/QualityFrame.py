#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import wx
import wx.grid
import Constants
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from table_def import PLC_registers
from ProcessNotebook import ProcessNotebook
from numpy import array, arange
from wxmplot.plotframe import PlotFrame
from mpldatacursor import datacursor



class QualityModel():
	def __init__(self):
		return

	def GetDatesList(self, startDate, finalDate, orderNumber):
		dates_list = []
		self.starting_points = []

		
		if(orderNumber == ''):
			#Filtramos por fechas
			# create a Session
			engine = create_engine(Constants.DATABASE_PATH, echo=False)
			Session = sessionmaker(bind=engine)
			session = Session()

			self.starting_points = session.query(PLC_registers).filter(PLC_registers.Fecha >= startDate,
									PLC_registers.Fecha <= finalDate,
									PLC_registers.Start_status == 1).all()

			print 'len starting_points: ', len(self.starting_points)

		else:
			#Filtramos por numero de orden
			engine = create_engine(Constants.DATABASE_PATH, echo=False)
			Session = sessionmaker(bind=engine)
			session = Session()

			self.stopping_points = []
			self.orderNumber = int(orderNumber)
			next_stopping_point = session.query(PLC_registers).first()
			
			while(1):
			
				self.orderNumber_found = session.query(PLC_registers).filter(PLC_registers.id > next_stopping_point.id).filter(
											or_(PLC_registers.Producto1 == self.orderNumber,
											    PLC_registers.Producto2 == self.orderNumber,
											    PLC_registers.Producto3 == self.orderNumber,
											    PLC_registers.Producto4 == self.orderNumber,
											    PLC_registers.Producto5 == self.orderNumber,
											    PLC_registers.Producto6 == self.orderNumber)).first()
							
				if(self.orderNumber_found == None):
					print 'Entre a if(orderNumber_found)'
					break

				previous_starting_point = session.query(PLC_registers).filter(PLC_registers.id <= self.orderNumber_found.id,
									PLC_registers.Start_status == 1).order_by(PLC_registers.id.desc()).first()

				next_stopping_point = session.query(PLC_registers).filter(PLC_registers.id >= self.orderNumber_found.id,
									PLC_registers.End_status == 1).first()

				if(next_stopping_point == None):
					print 'Entre a if'
					break

				print 'orderNumber_found: ', self.orderNumber_found.id
				print 'previous_starting_point: ', previous_starting_point.id
				print 'next_stopping_point: ', next_stopping_point.id
				self.starting_points.append(previous_starting_point)
				

		for i in range(len(self.starting_points)):
			print 'ID starting point: ', self.starting_points[i].id
			dates_list.append(self.starting_points[i].Fecha)

		return dates_list


	def DynamicButtonHandler(self, evt):
		button = evt.GetEventObject()
        	print "The button you pressed was labeled: " + button.GetLabel()
		print "The button you pressed has ID: " + str(button.GetId())
		

		#Aqui hacer queries
		# create a Session		
		engine = create_engine(Constants.DATABASE_PATH, echo=False)
		Session = sessionmaker(bind=engine)
		session = Session()
		
		stopping_point = session.query(PLC_registers).filter(PLC_registers.id >= (self.starting_points[button.GetId()].id + 1),
								     PLC_registers.End_status == 1).first()

		results = session.query(PLC_registers).filter(PLC_registers.id >= (self.starting_points[button.GetId()].id), 
							      PLC_registers.id <= (stopping_point.id -1)).all()

		Presion1_plot_array 	= []
		Presion2_plot_array 	= []
		PresionInt_plot_array 	= []
		Temperatura_plot_array	= []
		
		for row in results:
			Presion1_plot_array.append(row.Presion1)
			Presion2_plot_array.append(row.Presion2)
			PresionInt_plot_array.append(row.Presion_interior)
			Temperatura_plot_array.append(row.Temperatura)

		self.processNotebook = ProcessNotebook(results)
		self.processNotebook.Show()
		self.processNotebook.Maximize(True)



class QualityFrame(wx.Frame):
	def __init__(self, startDate, finalDate, orderNumber):
		wx.Frame.__init__(self, parent=None, id=-1, title=Constants.QUALITY_FRAME_TITLE, 
				pos=Constants.RESULTS_FRAME_POS, size=Constants.RESULTS_FRAME_SIZE)

		self.MainPanel = wx.Panel(self, id=-1)
		self.startDate = startDate
		self.finalDate = finalDate
		self.orderNumber = orderNumber
		self.qualityModel = QualityModel()
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
