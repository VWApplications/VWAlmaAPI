from django.urls import path, include

urlpatterns = [
    path('', include('alma.core.urls')),
    path('users/', include('alma.accounts.urls')),
    path('disciplines/', include('alma.disciplines.urls')),
    path('groups/', include('alma.groups.urls')),
    path('sections/', include('alma.sections.urls')),
    path('questions/', include('alma.questions.urls'))
]
