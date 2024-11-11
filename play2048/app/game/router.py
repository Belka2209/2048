from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.game.dao import UserDAO
from app.game.schemas import SetBestScoreRequest, SetBestScoreResponse, TelegramIDModel
from app.database import get_session




router = APIRouter(prefix='', tags=['ИГРА'])
templates = Jinja2Templates(directory='app/templates')


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("pages/index.html", {"request": request})

@router.put("/api/bestScore/{user_id}", response_model=SetBestScoreResponse, summary="Set Best Score")
async def set_best_score(
        user_id: int,
        request: SetBestScoreRequest,
        session = Depends(get_session)
):
    """
    Установить лучший счет пользователя.
    Обновляет значение `best_score` в базе данных для текущего `user_id`.
    """
    score = request.score
    user = await UserDAO.find_one_or_none(session=session, filters=TelegramIDModel(telegram_id=user_id))
    user.best_score = score
    await session.commit()
    return SetBestScoreResponse(status="success", best_score=score)

@router.get("/records", response_class=HTMLResponse)
async def read_records(request: Request, session = Depends(get_session)):
    # Получаем топовые рекорды с их позициями
    records = await UserDAO.get_top_scores(session=session)
    # Передаем актуальный список рекордов в шаблон
    return templates.TemplateResponse("pages/records.html", {"request": request, "records": records})
