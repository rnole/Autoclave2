from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, DateTime, Integer, BigInteger, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///../AutoclaveMonitoreo.sqlite', echo=True)
Base = declarative_base()

class PLC_registers(Base):
	""""""
	__tablename__ = "PLC_registers"
	
	id 			= Column(Integer, primary_key = True, autoincrement=True)
	Fecha 	  		= Column(String)
	Hora 	  		= Column(String)
	Presion1 	  	= Column(Integer)
	Presion2 		= Column(Integer)
	Presion_interior	= Column(Integer)
	Estatus			= Column(Boolean)
	Start_status		= Column(Boolean)
	End_status		= Column(Boolean)
	Producto1		= Column(Integer)
	Producto2		= Column(Integer)
	Producto3		= Column(Integer)
	Producto4		= Column(Integer)
	Producto5		= Column(Integer)
	Producto6		= Column(Integer)
	Temperatura		= Column(Integer)
	Peso1			= Column(Integer)	
	Peso2			= Column(Integer)	
	Peso3			= Column(Integer)	
	Peso4			= Column(Integer)	
	Peso5			= Column(Integer)	
	Peso6			= Column(Integer)
	Lavado			= Column(Boolean)	
	Tenido			= Column(Boolean)	
	Nylon			= Column(Boolean)	
	Polyester		= Column(Boolean)	
	Red_madeja		= Column(Boolean)
	Peso_tinta_redes	= Column(Integer) 
	Peso_tinta_madejas	= Column(Integer) 
	Usuario			= Column(Integer)

if __name__ == '__main__':
	Base.metadata.create_all(engine)


