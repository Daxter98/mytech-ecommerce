from django.apps import AppConfig


class OrdenesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ordenes'
    default_site = 'ecommerce.'
    icon = 'fa fa-shopping-cart'
