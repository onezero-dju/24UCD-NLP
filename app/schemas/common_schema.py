from datetime import datetime
from pydantic import BaseModel


class StandardResponse(BaseModel):
    success: bool
    message: str
    data: dict | None = None  # data 필드는 선택적으로, 없을 수도 있음

# 사용 예시:
# return StandardResponse(success=True, message="Operation completed", data={"key": "value"})


class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

# 사용 예시:
# class UserResponse(TimestampMixin):
#     id: int
#     name: str
