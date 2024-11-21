from app.api.urls import SpyCats as cats_urls, Missions as mission_urls
from app.api.routers import app

from app.decorators import error_handler
from app.database import *

from fastapi.responses import RedirectResponse
import pydantic as _p

import typing as _t
import uuid


@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse("/docs")


@app.get((get_cat_url := cats_urls.get_spy_cat).path_with_prefix, tags=[get_cat_url.tag])
@error_handler
async def get_spy_cat(id: uuid.UUID) -> SpyCatModel:
    return await SpyCat.load_instance(id)


@app.get(cats_urls.get_all_spy_cats.path_with_prefix, tags=[get_cat_url.tag])
@error_handler
async def get_all_spy_cats() -> _t.Sequence[SpyCat]:
    return await SpyCat.get_all()


class MissionResponse(_p.BaseModel):
    mission: Mission
    mission_targets: list[Target]


@app.get((get_mission_url := mission_urls.get_mission).path_with_prefix, tags=[get_mission_url.tag])
@error_handler
async def get_mission(id: uuid.UUID) -> MissionResponse:
    instance = await Mission.load_instance(id)
    return MissionResponse(mission=instance, mission_targets=instance.targets)


@app.get(mission_urls.get_missions.path_with_prefix, tags=[get_mission_url.tag])
@error_handler
async def get_all_mission() -> _t.Sequence[Mission]:
    return await Mission.get_all()
