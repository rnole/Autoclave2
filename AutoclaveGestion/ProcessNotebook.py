#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import wx
from ProcessPanel import ProcessPanel
from QualityPlotPanel import QualityPlotPanel

class ProcessNotebook(wx.Frame):

	def __init__(self, queryResults):
		wx.Frame.__init__(self, None, -1, "Tabla y gráfica de proceso seleccionado")
		nb = wx.Notebook(self, -1, style=wx.BK_DEFAULT)

		p1 = ProcessPanel(nb, queryResults)
		nb.AddPage(p1, "Tabla")

		p2 = QualityPlotPanel(nb, queryResults)
		nb.AddPage(p2, "Gráfico")

