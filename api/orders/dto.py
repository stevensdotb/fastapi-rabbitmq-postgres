import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class StatusEnum(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    customer_name: str = Field(min_length=5, max_length=30, description="Customer name must be at least 15 characters long")
    product_name: str = Field(min_length=5, max_length=30, description="Product name must be at least 15 characters long")
    quantity: int = Field(ge=1, description="Quantity must be greater than 0")


class OrderDTO(OrderBase):
    id: int
    status: StatusEnum = Field(default=StatusEnum.PENDING)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class CreateOrderDTO(OrderBase):
    pass
