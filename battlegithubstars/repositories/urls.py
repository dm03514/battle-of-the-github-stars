from django.conf.urls import url
from repositories.views import GitHubBattleFormView


urlpatterns = [
    url(r'^githubbattle/', GitHubBattleFormView.as_view(), name='githubbattle')
]
