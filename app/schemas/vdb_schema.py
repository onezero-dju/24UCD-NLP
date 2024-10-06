from pydantic import BaseModel

# 요청 스키마: 아이템 생성
class ItemCreate(BaseModel):
    name: str
    description: str | None = None  # 선택적 필드
    price: float

# 응답 스키마: 아이템 정보 반환
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

    class Config:
        orm_mode = True