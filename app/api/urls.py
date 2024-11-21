from app.utils.urls import URLs, URLPath


class SpyCats(URLs, prefix="/cats"):
    create_spy_cat: URLPath = "/create_spy_cat"
    get_spy_cat: URLPath = "/get_spy_cat/{id}"
    get_all_spy_cats: URLPath = "/get_all_spy_cats"
    delete_spy_cat: URLPath = "/delete_spy_cat/{id}"
    update_salary: URLPath = "/update_cat_salary/{id}"


class Missions(URLs, prefix="/missions"):
    create_mission: URLPath = "/create_missions"
    get_mission: URLPath = "/get_mission/{id}"
    get_missions: URLPath = "/get_missions"
    delete_mission: URLPath = "/delete_mission/{id}"
    sign_mission_to_cat: URLPath = "/signed_mission_cat/{mission_id}/{cat_id}"
    mark_target_is_complete: URLPath = "/mark_target_is_complete/{target_id}"
    edit_target_note: URLPath = "/edit_target_note/{target_id}"
