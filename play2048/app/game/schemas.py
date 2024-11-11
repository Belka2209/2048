from pydantic import BaseModel


class TelegramIDModel(BaseModel):
    telegram_id: int

    
class UserModel(TelegramIDModel):
    username: str
    first_name: str
    last_name: str
    best_score: int

class SetBestScoreRequest(BaseModel):
    score: int


class SetBestScoreResponse(BaseModel):
    status: str
    best_score: int
