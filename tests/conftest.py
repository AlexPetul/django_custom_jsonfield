import django


def pytest_configure(config):
    from django.conf import settings

    settings.configure(
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
        },
        SECRET_KEY="doesn't really matter",
    )

    django.setup()
