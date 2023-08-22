import models

undefined = "Что то пошло не так, возможно сообщение не того типа"

greeting = "Бот, созданный помочь найти сожителя, приветствует тебя!"

menu = "Главное меню\n\n1. Заполнить анкету заново\n2. Показать мою анкету\n3. Смотреть анкеты"

ask_full_name = "Введите ваше ФИО"
ask_sex = "Введите ваш пол"
ask_age = "Введите ваш возраст"
ask_location = "Введите ваш город"
ask_application_type = "Введите тип вашей анкеты"
ask_acceptable_sex = "Введите пол сожителя"
ask_acceptable_application_type = "Введите тип сожителя"
ask_description = "Введите описание"
ask_photos = "Добавьте фотографии"
photo_added = "Фотография добавлена"


def my_profile(user: models.user.User) -> str:
    sex = "Мужской" if user.sex else "Женский"

    application_type = "Уже есть жилье" if user.application_type == models.user.ApplicationTypes.has_accomodation else "Хочу заселиться"
    acceptable_sex = ""
    acceptable_application_type = ""
    if user.acceptable_sex is None:
        acceptable_sex = "Любой"
    elif user.acceptable_sex:
        acceptable_sex = "Мужской"
    elif not user.acceptable_sex:
        acceptable_sex = "Женский"

    if user.acceptable_application_type == models.user.ApplicationTypes.has_accomodation:
        acceptable_application_type = "С жильем"
    elif user.acceptable_application_type == models.user.ApplicationTypes.searching_for:
        acceptable_application_type = "Без жилья"
    elif user.acceptable_application_type == models.user.ApplicationTypes.any:
        acceptable_application_type = "Без разницы"

    m = f"Тип анкеты: {application_type}\n" \
        f"Пол сожителя: {acceptable_sex}\n" \
        f"Тип поиска: {acceptable_application_type}\n\n" \
        f"Ваша анкета:\n" \
        f"{user.full_name}, {sex}, {user.age}, {user.location}\n" \
        f"{user.description}"
    return m
