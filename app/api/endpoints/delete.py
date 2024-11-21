from app.api.urls import SpyCats as cats_urls, Missions as mission_urls
from app.api.routers import app

from app.decorators import error_handler
from app.database import *

import uuid


@app.delete((delete_cat_url := cats_urls.delete_spy_cat).path_with_prefix, tags=[delete_cat_url.tag])
@error_handler
async def delete_spy_cat(id: uuid.UUID):
    return await SpyCat.remove_by_id(id)


@app.delete((delete_mission_url := mission_urls.delete_mission).path_with_prefix, tags=[delete_mission_url.tag])
@error_handler
async def delete_mission(id: uuid.UUID):
    instance = await Mission.load_instance(id)
    assert instance.spy_cat_id is None, "423: You cannot delete mission when it already signed to cat."
    return await instance.remove()
