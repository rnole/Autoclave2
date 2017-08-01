# -*- coding: utf-8 -*-
import wx
import Constants
from datetime import datetime 
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker


def DeleteDataAutoclave(startDate, finalDate, selectedAutoclave):
		
	if((startDate == '') or (finalDate == '')):
		dlg = wx.MessageDialog(None, 'Ingresar fechas correctas', 'MessageDialog', wx.OK)
		dlg_result = dlg.ShowModal()
		dlg.Destroy()
		return

	engine = create_engine(Constants.DATABASE_PATH, echo=False)
	Session = sessionmaker(bind=engine)
	session = Session()
	selected_table = Constants.Autoclave_dict[selectedAutoclave]

	starting_points = session.query(selected_table).filter(selected_table.Fecha >= startDate,
					selected_table.Fecha <= finalDate,
					selected_table.Start_status == 1).all()

	for i in range(len(starting_points)):
		stopping_point = session.query(selected_table).filter(selected_table.id >= (starting_points[i].id + 1),
										selected_table.End_status == 1).first()

		session.query(selected_table).filter(selected_table.id >= (starting_points[i].id), 
							      	      selected_table.id <= (stopping_point.id)).delete()
		
	session.commit()

	dlg = wx.MessageDialog(None, '¡Datos borrados!', 'MessageDialog', wx.OK)
	dlg_result = dlg.ShowModal()
	dlg.Destroy()
