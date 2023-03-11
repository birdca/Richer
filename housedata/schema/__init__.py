from __future__ import annotations

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class House(Base):
    __tablename__ = 'houses'

    houseId = Column(Integer, primary_key=True)
    userId = Column(Integer)
    postId = Column(Integer)
    regionId = Column(Integer)
    regionName = Column(String(255))
    sectionId = Column(Integer)
    streetId = Column(Integer)
    type = Column(Integer)
    kind = Column(Integer)
    floor = Column(Integer)
    allFloor = Column(Integer)
    room = Column(Integer)
    area = Column(Float)
    price = Column(Integer)
    cover = Column(String(255))
    updateTime = Column(Integer)
    closed = Column(Integer)
    sectionName = Column(String(255))
    fullAddress = Column(String(255))
    streetName = Column(String(255))
    alleyName = Column(String(255))
    caseName = Column(String(255))
    layout = Column(String(255))
    iconClass = Column(String(255))
    kindName = Column(String(255))
    coordinateX = Column(Float)
    coordinateY = Column(Float)

#   "houseId":1,
#   "userId":2,
#   "postId":0,
#   "regionId":0,
#   "regionName":"string",
#   "sectionId":0,
#   "streetId":0,
#   "type":0,
#   "kind":0,
#   "floor":0,
#   "allFloor":0,
#   "room":0,
#   "area":0.0,
#   "price":0,
#   "cover":"string",
#   "updateTime":1578233035,
#   "closed":0,
#   "condition":"string",
#   "sectionName":"string",
#   "fullAddress":"string",
#   "streetName":"string",
#   "alleyName":"string",
#   "caseName":"string",
#   "layout":"string",
#   "caseId":0,
#   "iconClass":"string",
#   "kindName":"string",
#   "corordinateX":0.0,
#   "corordinateY":0.0
# }
