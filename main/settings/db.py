from main.jsonenv import env


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.get("db_name"),
        "USER": env.get("db_user"),
        "PASSWWORD": env.get("db_password"),
        "HOST": "localhost",
        "PORT": "5431",
    }
}
