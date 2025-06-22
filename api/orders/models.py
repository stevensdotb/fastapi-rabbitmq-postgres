from sqlalchemy import Column, Integer, String, DateTime, func

from api.database import Base


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    customer_name = Column(String, index=True)
    product_name = Column(String, index=True)
    quantity = Column(Integer)
    status = Column(String, index=True, default="pending")
    created_at = Column(DateTime, default=func.now())
