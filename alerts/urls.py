from django.urls import path
from . import views

urlpatterns=[
    path(
        "create/",
        views.create_alert
    ),
    path(
        "delete/<int:alert_id>/",
        views.delete_alert
    ),
    path(
        "edit/<int:alert_id>/",
        views.edit_alert
    ),
    path(
        "search/",
        views.search_assets_view,
        name="search_assets"
    )
]