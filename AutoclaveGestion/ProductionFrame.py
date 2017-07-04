#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import Constants
import wx.grid
from datetime import datetime 
from ProcessNotebook import ProcessNotebook
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
import logging

COL_FECHA = 0
COL_HORA_INICIO = 3
COL_HORA_FIN = 4

def GetDurationProcess(start_time, end_time):
	start_hours, start_minutes = start_time.split(':')
	end_hours, end_minutes = end_time.split(':')

	start_total_minutes = int(start_hours)*60 + int(start_minutes)
	end_total_minutes   = int(end_hours)*60 + int(end_minutes)

	difference = end_total_minutes - start_total_minutes

	if(difference < 0):
		difference += 1440

	difference_hours_part   = str(difference / 60)
	difference_minutes_part = str(difference % 60)
	
	return difference_hours_part + ':' + difference_minutes_part

def GetDurationDepletion(results):
	duration_minutes = 0
	last_index = len(results) -1

	last_temperature = results[last_index].Temperatura

	last_index -= 1
	
	while((results[last_index].Temperatura > (last_temperature -1)) and (last_index >= 0)):
		duration_minutes +=1
		last_index -= 1

	duration_hours_part   = str(duration_minutes / 60)
	duration_minutes_part = str(duration_minutes % 60)
	
	return duration_hours_part + ':' + duration_minutes_part

	

def GetDurationSlope(duration_process, duration_depletion):

	duration_process_hrs, duration_process_mins = duration_process.split(':')
	duration_depletion_hrs, duration_depletion_mins = duration_depletion.split(':')
	
	total_process_minutes  = int(duration_process_hrs)*60 + int(duration_process_mins)
	total_depletion_minutes= int(duration_depletion_hrs)*60 + int(duration_depletion_mins)

	difference = total_process_minutes - total_depletion_minutes

	difference_hours_part   = str(difference / 60)
	difference_minutes_part = str(difference % 60)

	return difference_hours_part + ':' + difference_minutes_part

def GetSlope(results, duration_slope, duration_depletion):
	duration_slope_hrs, duration_slope_mins = duration_slope.split(':')
	total_slope_minutes  = int(duration_slope_hrs)*60 + int(duration_slope_mins)

	if(total_slope_minutes == 0):
		return '0'
	elif(total_slope_minutes >= len(results)):
		return '0'
	else:
		slope =  (results[total_slope_minutes].Temperatura - results[0].Temperatura)/(total_slope_minutes) 
	
	return '%.2f' % slope

def GetGridData(startDate, finalDate, orderNumber, selectedAutoclave):

	matrixTable = []

	if(orderNumber == ''):

		#Filtramos por fechas
		engine = create_engine(Constants.DATABASE_PATH, echo=False)
		Session = sessionmaker(bind=engine)
		session = Session()
		selected_table = Constants.Autoclave_dict[selectedAutoclave]
		starting_points = []
		
		starting_points = session.query(selected_table).filter(selected_table.Fecha >= startDate,
						selected_table.Fecha <= finalDate,
						selected_table.Start_status == 1).all()
		
		for i in range(len(starting_points)):
			#with each starting point, get its corresponding stopping point
			stopping_point = session.query(selected_table).filter(selected_table.id >= (starting_points[i].id + 1),
										selected_table.End_status == 1).first()

			results = session.query(selected_table).filter(selected_table.id >= (starting_points[i].id), 
							      	      selected_table.id <= (stopping_point.id -1)).all()

			
			print 'len results: ', len(results)

			Proceso = 'Lavado' if(results[5].Lavado == True) else 'Tenido'
			Redes_o_Madejas = 'Red' if(results[5].Red_madeja == True) else 'Madeja'
			Peso_tinta = results[5].Peso_tinta_redes if(results[5].Red_madeja == True) else results[5].Peso_tinta_madejas
			Material = 'Polyester' if(results[5].Polyester == True) else 'Nylon'
			Fecha = Constants.ChangeDate2ddmmyy(results[0].Fecha)
			
			products_list = ((results[5].Producto1, results[5].Peso1),
					 (results[5].Producto2, results[5].Peso2),
					 (results[5].Producto3, results[5].Peso3),
					 (results[5].Producto4, results[5].Peso4),
					 (results[5].Producto5, results[5].Peso5),
					 (results[5].Producto6, results[5].Peso6))

			duration_process = GetDurationProcess(results[0].Hora, results[len(results) - 1].Hora)
			duration_depletion = GetDurationDepletion(results)
			duration_slope	= GetDurationSlope(duration_process, duration_depletion)
			slope = GetSlope(results, duration_slope, duration_depletion)

			for producto_num, peso_num in products_list:
				if(producto_num != 0):
					row = []
					row.append(Fecha)
					row.append(producto_num)
					row.append(peso_num)
					row.append(results[0].Hora)
					row.append(results[len(results) - 1].Hora)
					row.append(duration_process)
					row.append(duration_slope)
					row.append(duration_depletion)
					row.append(slope)

					row.append(Proceso)
					row.append(Redes_o_Madejas)
					row.append(Peso_tinta)
					row.append(Material)
					row.append(results[5].Usuario)
					matrixTable.append(row)

	else:
		#Filtramos por numero de orden
		engine = create_engine(Constants.DATABASE_PATH, echo=False)
		Session = sessionmaker(bind=engine)
		session = Session()
		selected_table = Constants.Autoclave_dict[selectedAutoclave]
		stopping_points = []
		orderNumber = int(orderNumber)

		next_stopping_point = session.query(selected_table).first()
		
		while(1):
		
			orderNumber_found = session.query(selected_table).filter(selected_table.id > next_stopping_point.id).filter(
										or_(selected_table.Producto1 == orderNumber,
										    selected_table.Producto2 == orderNumber,
										    selected_table.Producto3 == orderNumber,
										    selected_table.Producto4 == orderNumber,
										    selected_table.Producto5 == orderNumber,
										    selected_table.Producto6 == orderNumber)).first()

			if(orderNumber_found == None):
				logging.debug('No more orderNumbers found')
				break

			previous_starting_point = session.query(selected_table).filter(selected_table.id <= orderNumber_found.id,
									selected_table.Start_status == 1).order_by(selected_table.id.desc()).first()

			next_stopping_point = session.query(selected_table).filter(selected_table.id >= orderNumber_found.id,
										selected_table.End_status == 1).first()							
			if(next_stopping_point == None):
				logging.debug('No more stopping_points')
				break


			results = session.query(selected_table).filter(selected_table.id >= previous_starting_point.id, 
								      selected_table.id < next_stopping_point.id).all()

			row = []
			Fecha = Constants.ChangeDate2ddmmyy(results[0].Fecha)
			row.append(Fecha)
			row.append(orderNumber)

			if(orderNumber == results[5].Producto1):
				row.append(results[5].Peso1)
			elif(orderNumber == results[5].Producto2):
				row.append(results[5].Peso2)
			elif(orderNumber == results[5].Producto3):
				row.append(results[5].Peso3)
			elif(orderNumber == results[5].Producto4):
				row.append(results[5].Peso4)
			elif(orderNumber == results[5].Producto5):
				row.append(results[5].Peso5)
			elif(orderNumber == results[5].Producto6):
				row.append(results[5].Peso6)

			duration_process = GetDurationProcess(results[0].Hora, results[len(results) - 1].Hora)
			duration_depletion = GetDurationDepletion(results)
			duration_slope	= GetDurationSlope(duration_process, duration_depletion)
			slope = GetSlope(results, duration_slope, duration_depletion)

			row.append(results[0].Hora)
			row.append(results[len(results) - 1].Hora)
			row.append(duration_process)
			row.append(duration_slope)
			row.append(duration_depletion)
			row.append(slope)
			
			Proceso = 'Lavado' if(results[5].Lavado == True) else 'Tenido'
			Redes_o_Madejas = 'Red' if(results[5].Red_madeja == True) else 'Madeja'
			Peso_tinta = results[5].Peso_tinta_redes if(results[5].Red_madeja == True) else results[5].Peso_tinta_madejas
			Material = 'Polyester' if(results[5].Polyester == True) else 'Nylon'

			row.append(Proceso)
			row.append(Redes_o_Madejas)
			row.append(Peso_tinta)
			row.append(Material)
			row.append(results[5].Usuario)
			matrixTable.append(row)
	
	return matrixTable

class ProductionTable(wx.grid.PyGridTableBase):

	colLabels = ("Fecha", "Nº orden", "Peso", "Hora Inicio", "Hora Fin", "Duración de \nProceso",
			"Duración\n Pendiente", "Duración\n Agotamiento", "Pendiente\n(ºC/min)", "Proceso", 
			"Red/Madeja", "Peso\nColorante", "Material", "Usuario")

	def __init__(self, startDate, finalDate, orderNumber, selectedAutoclave):

		self.matrixTable = GetGridData(startDate, finalDate, orderNumber, selectedAutoclave)
		wx.grid.PyGridTableBase.__init__(self)
		self.odd=wx.grid.GridCellAttr()
        	self.odd.SetBackgroundColour("light blue")
		self.even=wx.grid.GridCellAttr()
        	self.even.SetBackgroundColour("white")

	def GetNumberRows(self):
		return len(self.matrixTable)

	def GetNumberCols(self):
		return len(self.colLabels)

	def GetColLabelValue(self, col):
		return self.colLabels[col]

	def IsEmptyCell(self, row, col):
		return False

	def GetValue(self, row, col):
		return self.matrixTable[row][col]	

	def GetAttr(self, row, col, kind):
	        attr = [self.even, self.odd][row % 2]
        	attr.IncRef()
	        return attr

	def SetValue(self, row, col, value):
		pass


class ProductionFrame(wx.Frame):
	def __init__(self, startDate, finalDate, orderNumber, selectedAutoclave):
		wx.Frame.__init__(self, parent=None, id=-1, title=Constants.RESULTS_FRAME_TITLE, 
				pos=Constants.RESULTS_FRAME_POS, size=Constants.RESULTS_FRAME_SIZE)

		self.MainPanel = wx.Panel(self, id=-1)
		self.startDate = startDate
		self.finalDate = finalDate
		self.orderNumber = orderNumber
		self.selectedAutoclave = selectedAutoclave
		self.PanelInit()

	def PanelInit(self):
		
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.grid1 = wx.grid.Grid(self.MainPanel)
		self.grid1.SetTable(ProductionTable(self.startDate, self.finalDate, self.orderNumber, self.selectedAutoclave))
		self.grid1.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
		self.grid1.HideRowLabels()
		self.grid1.SetLabelBackgroundColour("light blue")
		
		mainSizer.Add(self.grid1, 0, wx.ALL, 10)
		self.MainPanel.SetSizer(mainSizer)
		mainSizer.Fit(self)
		
		#Adding events
		self.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnSelectCell)
		self.grid1.Bind(wx.EVT_KEY_DOWN, self.OnKey)
		
	
	def OnKey(self, event):
		# If Ctrl+C is pressed...
		if event.ControlDown() and event.GetKeyCode() == 67:
		    	self.copy()

		# Skip other Key events
		if event.GetKeyCode():
			event.Skip()
			return

	def copy(self):
		 
		# Number of rows and cols
		topleft = self.grid1.GetSelectionBlockTopLeft()
		if list(topleft) == []:
			topleft = []
		else:
		    	topleft = list(topleft[0])

		bottomright = self.grid1.GetSelectionBlockBottomRight()

		if list(bottomright) == []:
			bottomright = []
		else:
			bottomright = list(bottomright[0])

		if list(self.grid1.GetSelectionBlockTopLeft()) == []:
			rows = 1
		    	cols = 1
		    	iscell = True
		else:
			rows = bottomright[0] - topleft[0] + 1
		    	cols = bottomright[1] - topleft[1] + 1
		    	iscell = False

		# data variable contain text that must be set in the clipboard
		data = ''
		# For each cell in selected range append the cell value in the data variable
		# Tabs '    ' for cols and '\r' for rows
		for r in range(rows):
			for c in range(cols):
				if iscell:
					data += str(self.grid1.GetCellValue(self.grid1.GetGridCursorRow() + r, self.grid1.GetGridCursorCol() + c))
				else:
			    		data += str(self.grid1.GetCellValue(topleft[0] + r, topleft[1] + c))
				if c < cols - 1:
			    		data += ' '
		    	data += '\n'

		# Create text data object
		clipboard = wx.TextDataObject()
		# Set data object value
		clipboard.SetText(data)
		# Put the data in the clipboard
		if wx.TheClipboard.Open():
			wx.TheClipboard.SetData(clipboard)
			wx.TheClipboard.Close()
		else:
			wx.MessageBox("Can't open the clipboard", "Error")


	def OnSelectCell(self, evt):
		selectedDate = Constants.ChangeDate2yymmdd(self.grid1.GetCellValue(evt.GetRow(), COL_FECHA))
		startTime =  self.grid1.GetCellValue(evt.GetRow(), COL_HORA_INICIO)
		endTime	= self.grid1.GetCellValue(evt.GetRow(), COL_HORA_FIN)

		# create a Session		
		engine = create_engine(Constants.DATABASE_PATH, echo=False)
		Session = sessionmaker(bind=engine)
		session = Session()
		selected_table = Constants.Autoclave_dict[self.selectedAutoclave]

		results = session.query(selected_table).filter(selected_table.Fecha >= selectedDate).\
							filter(selected_table.Hora >= startTime).all()
		
		next_stopping_point = session.query(selected_table).filter(selected_table.id > results[0].id,
									selected_table.End_status == 1).first()

		results = session.query(selected_table).filter(selected_table.id >= results[0].id,
								selected_table.id <= (next_stopping_point.id - 1)).all()

		self.processNotebook = ProcessNotebook(results)
		self.processNotebook.Show()
		self.processNotebook.Maximize(True)
