#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import wx
import wx.grid
from numpy import array, arange
from wxmplot.plotpanel import PlotPanel
from mpldatacursor import datacursor

class QualityPlotPanel(PlotPanel):

	def __init__(self, parent, queryResults):
		PlotPanel.__init__(self, parent)

		Presion1_plot_array 	= []
		Presion2_plot_array 	= []
		PresionInt_plot_array 	= []
		Temperatura_plot_array	= []
		
		for row in queryResults:
			Presion1_plot_array.append(row.Presion1)
			Presion2_plot_array.append(row.Presion2)
			PresionInt_plot_array.append(row.Presion_interior)
			Temperatura_plot_array.append(row.Temperatura)
	
		self.CreateData(Presion1_plot_array, Presion2_plot_array, PresionInt_plot_array, Temperatura_plot_array)
		line1 = self.plot(self.x, self.y1, title= "Parametros de Proceso - Autoclave 2", 
					ylabel="Presion[psi]", xlabel="Tiempo de Proceso[min]", 
					marker='o', color="blue", label='Presion Bomba 1', xmax=140, ymin=0, ymax=100,
					legendfontsize=5, labelfontsize=6)

		line2 = self.oplot(self.x, self.y2, marker='o', color="lightgreen", label='Presion Bomba 2')
		line3 = self.oplot(self.x, self.y3, marker='o', color="red", label='Presion Interior')
		line4 = self.oplot(self.x, self.y4, marker='o', color="orange", label='Temperatura', 
						y2label='Temperatura[C]', side='right', ymin=0, ymax=140 , show_legend=True, legend_loc='lc')
		
		datacursor(line1, hide_button=1)
		datacursor(line2, hide_button=1)
		datacursor(line3, hide_button=1)
		datacursor(line4, hide_button=1)
	

		
	def CreateData(self, Presion1_array, Presion2_array, PresionInt_array, Temperatura_array):

		self.x  = array(arange(0,len(Presion1_array), 1))
		self.y1 = array(Presion1_array)
		self.y2 = array(Presion2_array)
		self.y3 = array(PresionInt_array)
		self.y4 = array(Temperatura_array)






