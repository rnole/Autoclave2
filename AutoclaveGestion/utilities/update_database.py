import Constants
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from table_def import Autoclave2_table

engine = create_engine(Constants.DATABASE_PATH, echo=False)
Session = sessionmaker(bind=engine)
session = Session()

status_points = session.query(Autoclave2_table).filter(Autoclave2_table.Estatus == 0).all()


for i in range(len(status_points)):
	status_points[i].End_status = 1
	start_point = session.query(Autoclave2_table).filter(Autoclave2_table.id == (status_points[i].id +1)).first()
	start_point.Start_status = 1
	session.commit()


