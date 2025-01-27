from pydantic import BaseModel, Field

class PlaceOrderRequest(BaseModel):
    script: str = Field()