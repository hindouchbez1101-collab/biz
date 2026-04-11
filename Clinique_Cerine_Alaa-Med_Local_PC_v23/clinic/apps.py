from django.apps import AppConfig


class ClinicConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clinic"

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(_create_groups, sender=self)


def _create_groups(sender, **kwargs):
    """Crée automatiquement les groupes requis après chaque migration."""
    try:
        from django.contrib.auth.models import Group
        for name in ("ADMIN", "GERANT", "RECEPTION", "PHARMACIE"):
            Group.objects.get_or_create(name=name)
    except Exception:
        pass
