from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import String, Integer, Column, Float, ForeignKey


class Point(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    route_id = Column(Integer, ForeignKey('routes.id'))
    route = relationship("Route", back_populates="points")

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    points = relationship("Point", back_populates="route")

