#!/usr/bin/env python
# -*- coding: utf-8 -*-
from table_def import Autoclave1_table
from table_def import Autoclave2_table
from table_def import Autoclave3_table

DATABASE_PATH	    = "sqlite:///../AutoclaveMonitoreo.sqlite"
MAIN_FRAME_TITLE    = "Búsqueda de Datos: Monitoreo de Autoclaves"
RESULTS_FRAME_TITLE = "Resultados de Producción"
QUALITY_FRAME_TITLE = "Resultados de Calidad"
PROCESS_FRAME_TITLE = "Base de datos: Proceso "
DYNAMIC_BUTTON_TITLE = "Ver Tabla/Gráfico"

MAIN_FRAME_POS	= (100, 100)
MAIN_FRAME_SIZE = (600, 200)

RESULTS_FRAME_POS  = (100, 100)
RESULTS_FRAME_SIZE = (800, 500)

Autoclave_dict = [Autoclave1_table, Autoclave2_table, Autoclave3_table]

def ChangeDate2ddmmyy(date):

	year, month, day = date.split('/')
	return day + '/' + month + '/' + year

def ChangeDate2yymmdd(date):
	day, month, year = date.split('/')
	return year + '/' + month + '/' + day

