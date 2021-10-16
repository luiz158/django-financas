from django.contrib import admin
from django.urls import path

from dashboard.views import inicio
from movimentacoes.views import criar_movimentacao


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path("criar-movimentacao/", criar_movimentacao, name="criar_movimentacao")
]
