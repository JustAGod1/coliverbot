import models

undefined = "Что то пошло не так, возможно сообщение не того типа"
try_again = "Попробуйте еще раз"

greeting = "Бот, созданный помочь найти сожителя, приветствует тебя!"

menu = "Главное меню\n\n1. Заполнить анкету заново\n2. Показать мою анкету\n3. Смотреть анкеты"
show_opp_placeholder = "✨🔍"
like = "Твой лайк отправлен!"
sleep = "Ждем лайков от других пользователей"

ask_full_name = "Давай знакомиться! Какое имя ты хочешь видеть в своей анкете?"
ask_sex = "Давай уточним пол"
ask_age = "Укажи свой возраст"
ask_location = "Расскажи, где ты уже живешь или хочешь жить"
ask_application_type = "Как у тебя с жильем прямо сейчас?"
ask_acceptable_sex = "С кем тебе хотелось бы жить?"
ask_acceptable_application_type = "Можем сузить круг поиска, какие анкеты стоит искать?"
ask_description = "Введите описание"
ask_photos = "Добавьте фотографии"
photo_added = "Фотография добавлена"
photos_cleared = "Фотографии удалены"


def profile(user: models.user.User) -> str:
    sex = "Мужской" if user.sex else "Женский"

    application_type = "Уже есть жилье" if user.application_type == models.user.ApplicationTypes.has_accomodation \
        else "Хочу заселиться"
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
