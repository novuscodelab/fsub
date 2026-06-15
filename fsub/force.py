from fsub.config import BUTTON_TITLE, FORCE_MESSAGE, FORCE_SUB_
from fsub.database import full_dynamic_fsub, get_setting

SETTING_FORCE_MESSAGE = "force_message"
SETTING_JOIN_BUTTON = "join_button_text"


def get_static_fsubs():
    return dict(FORCE_SUB_)


def get_dynamic_fsubs():
    return {index: chat_id for index, chat_id in enumerate(full_dynamic_fsub(), start=len(FORCE_SUB_) + 1)}


def get_all_fsubs():
    data = get_static_fsubs()
    data.update(get_dynamic_fsubs())
    return data


def get_force_message_template():
    return get_setting(SETTING_FORCE_MESSAGE, FORCE_MESSAGE)


def get_join_button_title():
    return get_setting(SETTING_JOIN_BUTTON, BUTTON_TITLE)
