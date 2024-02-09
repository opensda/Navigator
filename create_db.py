from database import Base, engine
from models import Point, Route

print('creating db...')


Base.metadata.create_all(engine)