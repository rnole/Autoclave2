# -*- coding: utf-8 -*-
import wx
import Constants
from wx.lib.pubsub import pub
from ProductionFrame import ProductionFrame
from QualityFrame import QualityFrame


class MainModel():

	def __init__(self):
		self.productionCheckbox_value = False
		self.qualityCheckbox_value = False
		self.productionCheckbox_enabled = True
		self.qualityCheckbox_enabled = True

	def SetCheckbox(self, cbx_label, cbx_value):

		if(cbx_label == 'Producci�n'):
			self.productionCheckbox_value = cbx_value

			if(cbx_value == True):
				self.qualityCheckbox_enabled = False
			else:
				self.qualityCheckbox_enabled = True
	
		elif(cbx_label == 'Calidad'):
			self.qualityCheckbox_value = cbx_value

			if(cbx_value == True):
				self.productionCheckbox_enabled = False
			else:
				self.productionCheckbox_enabled = True
			

		pub.sendMessage('Checkboxes changed')

	def FilterHandler(self, startDate, finalDate, orderNumber):
		if((self.productionCheckbox_value == False) and (self.qualityCheckbox_value == False)):
			dlg = wx.MessageDialog(None, 'Ning�n filtro seleccionado', 'MessageDialog', wx.OK)
			dlg_result = dlg.ShowModal()
			dlg.Destroy()


		elif(self.AreDatesCorrect(startDate, finalDate) == False):
			return

		elif(self.productionCheckbox_value == True):
			ResultsFrame = ProductionFrame(self.startDate, self.finalDate, orderNumber)
			ResultsFrame.Show()

		elif(self.qualityCheckbox_value == True):
			ResultsFrame = QualityFrame(self.startDate, self.finalDate, orderNumber)
			ResultsFrame.Show()	

	def AreDatesCorrect(self, firstdate, seconddate):
		try:
			self.startDate = Constants.ChangeDate2yymmdd(firstdate)
			self.finalDate = Constants.ChangeDate2yymmdd(seconddate)

			if(self.startDate <= self.finalDate):
				return True
			else: 
				dlg = wx.MessageDialog(None, 'Fecha final debe ser mayor a la fecha inicial', 'MessageDialog', wx.OK)
				dlg_result = dlg.ShowModal()
				dlg.Destroy()
				return False

		except ValueError:	
			if((firstdate == '') and (seconddate == '')):
				self.startDate = ''
				self.finalDate = ''
				return True
			else:
				dlg = wx.MessageDialog(None, 'Error de formato en las fechas', 'MessageDialog', wx.OK)
				dlg_result = dlg.ShowModal()
				dlg.Destroy()
				return False

class MainFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, -1, title=Constants.MAIN_FRAME_TITLE, pos=Constants.MAIN_FRAME_POS, 
					size=Constants.MAIN_FRAME_SIZE,	style=wx.DEFAULT_FRAME_STYLE & \
						~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

		self.MainPanel = wx.Panel(self, id=-1)
		self.PanelInit()
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

	def PanelInit(self):
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		dateSizer =  wx.BoxSizer(wx.HORIZONTAL)
		orderNumberSizer = wx.BoxSizer(wx.HORIZONTAL)
		checkBoxesSizer  = wx.BoxSizer(wx.HORIZONTAL)

		StartDate_label = wx.StaticText(self.MainPanel, -1, "Fecha Desde:")
		self.StartDate  = wx.TextCtrl(self.MainPanel, -1, "")

		FinalDate_label = wx.StaticText(self.MainPanel, -1, "Fecha Hasta:")
		self.FinalDate  = wx.TextCtrl(self.MainPanel, -1, "")

		OrderNumber_label = wx.StaticText(self.MainPanel, -1, "Nro. Orden:")
		self.OrderNumber = wx.TextCtrl(self.MainPanel, -1, "")

		FilterButton = wx.Button(self.MainPanel, -1, "Generar Reporte")
		self.Bind(wx.EVT_BUTTON, self.OnFilterButtonClick, FilterButton)
	
		self.productionCheckbox = wx.CheckBox(self.MainPanel, -1, "Producci�n")
		self.qualityCheckbox    = wx.CheckBox(self.MainPanel, -1, "Calidad")
		self.Bind(wx.EVT_CHECKBOX, self.OnProductionCheckbox, self.productionCheckbox)
	        self.Bind(wx.EVT_CHECKBOX, self.OnQualityCheckbox, self.qualityCheckbox)
		

		dateSizer.Add(StartDate_label, 0, wx.ALL, 5)
		dateSizer.Add(self.StartDate, 0,wx.ALL, 5)
		dateSizer.Add(FinalDate_label, 0,wx.ALL, 5)
		dateSizer.Add(self.FinalDate, 0,wx.ALL, 5)
		orderNumberSizer.Add(OrderNumber_label, 0,wx.ALL, 5)
		orderNumberSizer.Add(self.OrderNumber, 0,wx.ALL, 5)
		checkBoxesSizer.Add(self.productionCheckbox, 0,wx.ALL, 5)		
		checkBoxesSizer.Add(self.qualityCheckbox, 0,wx.ALL, 5)		

		mainSizer.Add(dateSizer, 0)
		mainSizer.Add(orderNumberSizer, 0)
		mainSizer.Add(checkBoxesSizer, 0)
		mainSizer.Add(FilterButton, 0)
		self.MainPanel.SetSizer(mainSizer)

		self.frameModel = MainModel()
		pub.subscribe(self.UpdateCheckboxes, 'Checkboxes changed')

	def OnProductionCheckbox(self, evt):
		self.frameModel.SetCheckbox('Producci�n', self.productionCheckbox.GetValue())
	
	def OnQualityCheckbox(self, evt):
		self.frameModel.SetCheckbox('Calidad', self.qualityCheckbox.GetValue())

	def UpdateCheckboxes(self):
		self.productionCheckbox.Enable(self.frameModel.productionCheckbox_enabled)
		self.qualityCheckbox.Enable(self.frameModel.qualityCheckbox_enabled)

	def OnFilterButtonClick(self, evt):
		self.frameModel.FilterHandler(self.StartDate.GetValue(),  self.FinalDate.GetValue(), self.OrderNumber.GetValue())

	def OnCloseWindow(self, event):
		self.Destroy()


if __name__ == '__main__':
	app = wx.PySimpleApp()
	myFrame = MainFrame()
	myFrame.Show()
	app.MainLoop()

