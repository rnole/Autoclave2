#!/usr/bin/env python
# -*- coding: utf-8 -*- 
DATABASE_PATH	    = "sqlite:///../AutoclaveMonitoreo.sqlite"
MAIN_FRAME_TITLE    = "B�squeda de Datos Sistema de Monitoreo Autoclave 2"
RESULTS_FRAME_TITLE = "Resultados de Producci�n"
QUALITY_FRAME_TITLE = "Resultados de Calidad"
PROCESS_FRAME_TITLE = "Base de datos: Proceso "
DYNAMIC_BUTTON_TITLE = "Ver Tabla/Gr�fico"

MAIN_FRAME_POS	= (100, 100)
MAIN_FRAME_SIZE = (600, 200)

RESULTS_FRAME_POS  = (100, 100)
RESULTS_FRAME_SIZE = (800, 500)

def ChangeDate2ddmmyy(date):

	year, month, day = date.split('/')
	return day + '/' + month + '/' + year

def ChangeDate2yymmdd(date):
	day, month, year = date.split('/')
	return year + '/' + month + '/' + day
