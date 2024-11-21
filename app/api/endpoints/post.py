from app.api.urls import SpyCats as cats_urls, Missions as mission_urls
from app.api.routers import app

from app.decorators import error_handler
from app.database import *

import fastapi as _fa


@app.post((create_cat_url := cats_urls.create_spy_cat).path_with_prefix, tags=[create_cat_url.tag])
@error_handler
async def create_spy_cat(cat: SpyCatModel):
    created = await SpyCat.create_table(cat)
    assert created is not None, "400: Failed to create SpyCat."

    return _fa.Response("SpyCat created!", status_code=_fa.status.HTTP_201_CREATED)


@app.post((create_mission_url := mission_urls.create_mission).path_with_prefix, tags=[create_mission_url.tag])
@error_handler
async def create_missions(targets: list[TargetModel]):
    mission = await Mission.create_table({})
    assert mission is not None, "400: Failed to create Mission."

    assert len(set(targets)) == len(targets), "400: All targets need to be unique."

    for target in targets:
        await Target.create_table((target.model_dump() | {"mission_id": mission.id}))

    return _fa.Response("Mission created", status_code=_fa.status.HTTP_201_CREATED)
