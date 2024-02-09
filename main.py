from typing import Optional

from fastapi import status, HTTPException


import models

from fastapi import FastAPI, File, UploadFile, Query
from pydantic import BaseModel

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import List


from fastapi.responses import JSONResponse
app = FastAPI()


class RouteData(BaseModel):
    format: str = Query(..., description="Формат файла, должен быть 'csv'")
    file: UploadFile = File(..., description="CSV файл с точками маршрута")


class Point(BaseModel):
    lat: float
    lng: float

    class Config:
        orm_mode = True


class RouteCreate(BaseModel):
    id: Optional[int] = None
    points: List[Point]

    class Config:
        orm_mode = True



engine = create_engine("postgresql://postgres:12345@db:5432/test001",
                       echo=True)


Session = sessionmaker(bind=engine)
session = Session()


@app.post("/api/routes/")
async def create_route(route_data: RouteCreate):
    new_route = models.Route()
    session = Session()

    try:
        session.add(new_route)
        session.commit()

        for point in route_data.points:
            new_point = models.Point(lat=point.lat, lng=point.lng, route=new_route)
            session.add(new_point)
        session.commit()

        created_route = {"id": new_route.id, "points": route_data.points}
        return created_route
    finally:
        session.close()


@app.get("/routes/{route_id}", response_model=RouteCreate, status_code=status.HTTP_200_OK)
def get_route(route_id: int):
    route = session.query(models.Route).filter(models.Route.id == route_id).first()

    return route
