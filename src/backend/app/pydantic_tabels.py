from datetime import date as dt_date

from pydantic import BaseModel, ConfigDict, Field


class top_100(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="название репозитория")
    owner: str = Field(..., description="владелец репозитория")
    position_cur: int = Field(..., description="текущая позиция в топе")
    position_prev: int = Field(..., description="предыдущая позиция в топе")
    stars: int = Field(..., description="количество звёзд")
    watchers: int = Field(..., description="количество просмотров")
    forks: int = Field(..., description="количество форков")
    open_issues: int = Field(..., description="количество открытых issues")
    language: str = Field(..., description="язык")


class activity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: dt_date = Field(..., description="дата")
    commits: int = Field(..., description="количество коммитов за конкретный день")
    authors: list[str] = Field(
        ..., description="список разработчиков, которые выполняли коммиты"
    )
