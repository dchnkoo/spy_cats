from app.api.urls import SpyCats as cats_urls, Missions as mission_urls
from app.api.routers import app

from app.decorators import error_handler
from app.database import *

import fastapi as _fa
import uuid


@app.patch((update_cat_salary_url := cats_urls.update_salary).path_with_prefix, tags=[update_cat_salary_url.tag])
@error_handler
async def update_cat_salary(id: uuid.UUID, salary: int) -> bool:
    cat = await SpyCat.load_instance(id)
    return await cat.update_field("salary", salary)


@app.patch((sign_to_cat_url := mission_urls.sign_mission_to_cat).path_with_prefix, tags=[sign_to_cat_url.tag])
@error_handler
async def sign_to_cat_mission(mission_id: uuid.UUID, cat_id: uuid.UUID) -> bool:
    mission = await Mission.load_instance(mission_id)
    cat = await SpyCat.load_instance(cat_id)
    return await mission.update_field("spy_cat_id", cat.id)


@app.patch(mission_urls.mark_target_is_complete.path_with_prefix, tags=[sign_to_cat_url.tag])
@error_handler
async def mark_target_is_complete(target_id: uuid.UUID):
    target = await Target.load_instance(target_id)
    assert target.complete is False, "400: Target already completed."
    
    updated = await target.update_field("complete", True)
    assert updated is True, "500: Failed to mark target as complete."

    completed = await target.mission.all_tasks_complete()

    if completed:
        return _fa.Response("All targets completed!")
    
    return _fa.Response("Target marked as completed.")


@app.patch(mission_urls.edit_target_note.path_with_prefix, tags=[sign_to_cat_url.tag])
@error_handler
async def edit_target_note(target_id: uuid.UUID, notes: str = _fa.Body(..., embed=True)):
    target = await Target.load_instance(target_id)
    assert target.complete is False, "423: You cannot update notes when target complete."

    targets = await target.mission.tasks()
    for trgt in targets:
        assert trgt.notes != notes, "423: Each target will be unique, that note already exists in targets."
    return await target.update_field("notes", notes)
