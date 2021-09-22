from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"
    verbose_name = "accounts Models"

    def ready(self):
        import accounts.signals
