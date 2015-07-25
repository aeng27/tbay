from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    bids = relationship("Bid", backref="item")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    items = relationship("Item", backref="user")
    bids = relationship("Bid", backref="user")
    
class Bid(Base):
    __tablename__ = "bid"
    
    id = Column(Integer, primary_key=True)
    price_point = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
    
Base.metadata.create_all(engine)

beyonce = User(username="Beyonce", password="Queen B")
michelle = User(username = "Michelle", password = "Queen M")
kelly = User(username = "Kelly", password = "Queen K")

baseball = Item(name = "Destiny's baseball", description = "One badass baseball", user = beyonce)

michelle_bid1 = Bid(price_point = 10.00, user = michelle, item = baseball)
kelly_bid1 = Bid(price_point = 10.50, user = kelly, item = baseball)
michelle_bid2 = Bid(price_point = 30.50, user = michelle, item = baseball)
kelly_bid2 = Bid(price_point = 30.00, user = kelly, item = baseball)

session.add_all([beyonce,michelle,kelly,baseball, michelle_bid1, michelle_bid2, kelly_bid1, kelly_bid2])
session.commit()

bids = session.query(Bid.id).order_by(Bid.price_point).all()
winning_bid= bids[-1:]
winner = session.query(Bid).get(winning_bid)

print winner.user.username

