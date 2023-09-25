from typing import Optional, List
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

import models
from .consts import DefaultConstructor


class BasicButtons(DefaultConstructor):
    i_am_m: str = "Я парень"
    i_am_f: str = "Я девушка"
    cities: List[str] = ["Москва", "Санкт-Петербург"]
    i_have_accomodation: str = "Уже есть жилье"
    i_am_looking_for_accomodation: str = "Хочу заселиться"
    with_boys: str = "С парнями"
    with_girls: str = "С девушками"
    with_anyone: str = "С кем угодно"
    with_accomodation: str = "С жильем"
    without_accomodation: str = "Без жилья"
    any: str = "Без разницы"
    leave_as_is: str = "Оставить как есть"
    clear: str = "Очистить"
    finish: str = "Завершить"
    menu_reapply: str = "1"
    menu_show_my_profile: str = "2"
    menu_show_opp_profile: str = "3"
    like: str = "❤️"
    dislike: str = "👎"
    sleep: str = "💤"
    show_received: str = "Показывай!"

    @staticmethod
    def ask_full_name(user: models.user.User) -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
        if user.full_name:
            schema = [1]
            btns = [str(user.full_name)]
            return BasicButtons._create_kb(btns, schema)
        return ReplyKeyboardRemove()

    @staticmethod
    def ask_sex() -> ReplyKeyboardMarkup:
        schema = [2]
        btns = [BasicButtons.i_am_m, BasicButtons.i_am_f]
        return BasicButtons._create_kb(btns, schema)

    @staticmethod
    def ask_age(user: models.user.User) -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
        if user.age:
            schema = [1]
            btns = [str(user.age)]
            return BasicButtons._create_kb(btns, schema)
        return ReplyKeyboardRemove()

    @staticmethod
    def ask_location() -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
        if BasicButtons.cities is None:
            return ReplyKeyboardRemove()
        schema: List[int] = [1]
        for city in BasicButtons.cities[1:]:
            if schema[-1] == 1:
                schema[-1] = 2
            elif schema[-1] == 2:
                schema.append(1)
        return BasicButtons._create_kb(BasicButtons.cities, schema)

    @staticmethod
    def ask_application_type() -> ReplyKeyboardMarkup:
        schema = [2]
        btns = [BasicButtons.i_have_accomodation, BasicButtons.i_am_looking_for_accomodation]
        return BasicButtons._create_kb(btns, schema)

    @staticmethod
    def ask_acceptable_sex() -> ReplyKeyboardMarkup:
        schema = [3]
        btns = [BasicButtons.with_boys, BasicButtons.with_girls, BasicButtons.with_anyone]
        return BasicButtons._create_kb(btns, schema)

    @staticmethod
    def ask_acceptable_application_type() -> ReplyKeyboardMarkup:
        schema = [3]
        btns = [BasicButtons.with_accomodation, BasicButtons.without_accomodation, BasicButtons.any]
        return BasicButtons._create_kb(btns, schema)

    @staticmethod
    def ask_description(user: models.user.User) -> ReplyKeyboardMarkup | ReplyKeyboardRemove:
        if user.description:
            schema = [1]
            btns = [BasicButtons.leave_as_is]
            return BasicButtons._create_kb(btns, schema)
        return ReplyKeyboardRemove()

    @staticmethod
    def ask_photos() -> ReplyKeyboardMarkup:
        schema = [2]
        btns = [BasicButtons.clear, BasicButtons.finish]
        return BasicButtons._create_kb(btns, schema)

    @staticmethod
    def menu() -> ReplyKeyboardMarkup:
        schema = [3]
        btns = [BasicButtons.menu_reapply, BasicButtons.menu_show_my_profile, BasicButtons.menu_show_opp_profile]
        return BasicButtons._create_kb(btns, schema)

    @staticmethod
    def scrolling() -> ReplyKeyboardMarkup:
        schema = [3]
        btns = [BasicButtons.like, BasicButtons.dislike, BasicButtons.sleep]
        return BasicButtons._create_kb(btns, schema)

    @staticmethod
    def ask_reveal() -> ReplyKeyboardMarkup:
        schema = [1]
        btns = [BasicButtons.show_received]
        return BasicButtons._create_kb(btns, schema)

    @staticmethod
    def scrolling_received() -> ReplyKeyboardMarkup:
        schema = [2]
        btns = [BasicButtons.like, BasicButtons.dislike]
        return BasicButtons._create_kb(btns, schema)
