#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import wx
import wx.grid
from Constants import DATABASE_PATH, MAIN_FRAME_TITLE, RESULTS_FRAME_TITLE
from Constants import QUALITY_FRAME_TITLE, PROCESS_FRAME_TITLE
from Constants import MAIN_FRAME_POS, MAIN_FRAME_SIZE, RESULTS_FRAME_POS, RESULTS_FRAME_SIZE
from Constants import ChangeDate2ddmmyy, ChangeDate2yymmdd

class ProcessTable(wx.grid.PyGridTableBase):

	colLabels = ("Fecha", "Hora", "P. Interna", "P. Bomba1", "P. Bomba2", "Temperatura")

	def __init__(self, queryResults):	
		self.queryResults = queryResults
		wx.grid.PyGridTableBase.__init__(self)
		self.odd=wx.grid.GridCellAttr()
        	self.odd.SetBackgroundColour("light blue")
		self.even=wx.grid.GridCellAttr()
        	self.even.SetBackgroundColour("white")

	def GetNumberRows(self):
		return len(self.queryResults)

	def GetNumberCols(self):
		return len(self.colLabels)

	def GetColLabelValue(self, col):
		return self.colLabels[col]

	def IsEmptyCell(self, row, col):
		return False

	def GetValue(self, row, col):
		if(col == 0):
			return ChangeDate2ddmmyy(self.queryResults[row].Fecha)
		elif(col == 1):
			return self.queryResults[row].Hora
		elif(col == 2):
			return self.queryResults[row].Presion_interior
		elif(col == 3):
			return self.queryResults[row].Presion1
		elif(col == 4):
			return self.queryResults[row].Presion2
		elif(col == 5):
			return self.queryResults[row].Temperatura

	def SetValue(self, row, col, value):
		pass

	def GetAttr(self, row, col, kind):
	        attr = [self.even, self.odd][row % 2]
        	attr.IncRef()
	        return attr


class ProcessPanel(wx.Panel):
	def __init__(self, parent,queryResults):
		wx.Panel.__init__(self, parent, id=-1)
		self.queryResults = queryResults
		self.PanelInit()

	
	def PanelInit(self):
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		grid1 = wx.grid.Grid(self)
		grid2 = wx.grid.Grid(self)
		self.grid3 = wx.grid.Grid(self, size=(500,32))
		self.FillGrid1(grid1)
		self.FillGrid2(grid2)
		self.FillGrid3()

		mainSizer.Add(grid1, 0, wx.ALL|wx.CENTER, 10)
		mainSizer.Add(grid2, 0, wx.ALL|wx.CENTER, 20)
		mainSizer.Add(self.grid3, 1, wx.ALIGN_CENTER_HORIZONTAL)

		self.SetSizer(mainSizer)
	
	def FillGrid1(self, grid1):
		grid1.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
		grid1.CreateGrid(4,6)
		grid1.HideRowLabels()
		grid1.HideColLabels()
		grid1.SetCellValue(0,0,"Nº Prod 1")
		grid1.SetCellValue(0,1,"Nº Prod 2")
		grid1.SetCellValue(0,2,"Nº Prod 3")
		grid1.SetCellValue(0,3,"Nº Prod 4")
		grid1.SetCellValue(0,4,"Nº Prod 5")
		grid1.SetCellValue(0,5,"Nº Prod 6")
		grid1.SetCellValue(2,0,"Peso 1")
		grid1.SetCellValue(2,1,"Peso 2")
		grid1.SetCellValue(2,2,"Peso 3")
		grid1.SetCellValue(2,3,"Peso 4")
		grid1.SetCellValue(2,4,"Peso 5")
		grid1.SetCellValue(2,5,"Peso 6")

		grid1.SetCellValue(1,0, str(self.queryResults[5].Producto1))
		grid1.SetCellValue(1,1, str(self.queryResults[5].Producto2))
		grid1.SetCellValue(1,2, str(self.queryResults[5].Producto3))
		grid1.SetCellValue(1,3, str(self.queryResults[5].Producto4))
		grid1.SetCellValue(1,4, str(self.queryResults[5].Producto5))
		grid1.SetCellValue(1,5, str(self.queryResults[5].Producto6))
		grid1.SetCellValue(3,0, str(self.queryResults[5].Peso1))
		grid1.SetCellValue(3,1, str(self.queryResults[5].Peso2))
		grid1.SetCellValue(3,2, str(self.queryResults[5].Peso3))
		grid1.SetCellValue(3,3, str(self.queryResults[5].Peso4))
		grid1.SetCellValue(3,4, str(self.queryResults[5].Peso5))
		grid1.SetCellValue(3,5, str(self.queryResults[5].Peso6))

		for col in range(6):
			grid1.SetCellBackgroundColour(0,col,"light blue")
			grid1.SetCellBackgroundColour(2,col,"light blue")
			grid1.SetCellFont(0, col, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
			grid1.SetCellFont(2, col, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
		

	def FillGrid2(self, grid2):
		booleanRenderer = wx.grid.GridCellBoolRenderer()
		grid2.CreateGrid(2,6)
		grid2.HideRowLabels()
		grid2.HideColLabels()
		grid2.SetCellValue(0,0,"Red")
		grid2.SetCellValue(0,1,"Madeja")
		grid2.SetCellValue(0,2,"Lavado")
		grid2.SetCellValue(0,3,"Teñido")
		grid2.SetCellValue(0,4,"Nylon")
		grid2.SetCellValue(0,5,"Polyester")

		for col in range(6):
			grid2.SetCellBackgroundColour(0,col,"light blue")
			grid2.SetCellFont(0, col, wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
			grid2.SetCellRenderer(1, col, booleanRenderer)

		Red	  = '1' if(self.queryResults[5].Red_madeja == True) else '0'
		Madeja	  = '1' if(self.queryResults[5].Red_madeja == False) else '0'
		Lavado    = '1' if(self.queryResults[5].Lavado == True) else '0'
		Tenido    = '1' if(self.queryResults[5].Tenido == True) else '0' 
		Nylon  	  = '1' if(self.queryResults[5].Nylon == True) else '0'
		Polyester = '1' if(self.queryResults[5].Polyester == True) else '0'

		grid2.SetCellValue(1,0, Red)
		grid2.SetCellValue(1,1, Madeja)
		grid2.SetCellValue(1,2, Lavado)
		grid2.SetCellValue(1,3, Tenido)
		grid2.SetCellValue(1,4, Nylon)
		grid2.SetCellValue(1,5, Polyester)
		grid2.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

	def FillGrid3(self):
		self.grid3.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
		self.grid3.SetTable(ProcessTable(self.queryResults))
		self.grid3.HideRowLabels()
		self.grid3.SetLabelBackgroundColour("light blue")
		self.grid3.Bind(wx.EVT_KEY_DOWN, self.OnKey)

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
		topleft = self.grid3.GetSelectionBlockTopLeft()
		if list(topleft) == []:
			topleft = []
		else:
		    	topleft = list(topleft[0])

		bottomright = self.grid3.GetSelectionBlockBottomRight()

		if list(bottomright) == []:
			bottomright = []
		else:
			bottomright = list(bottomright[0])

		if list(self.grid3.GetSelectionBlockTopLeft()) == []:
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
					data += str(self.grid3.GetCellValue(self.grid3.GetGridCursorRow() + r, self.grid3.GetGridCursorCol() + c))
				else:
			    		data += str(self.grid3.GetCellValue(topleft[0] + r, topleft[1] + c))
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




