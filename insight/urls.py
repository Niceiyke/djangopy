from django.urls import path

from .views import DeviationDeploymentView,DeviationUpdateView, FilterForm, InsightDataCreateView,InsightDataDeleteView,InsightDataListView,InsightDataUpdateView,DeviationListView,DeviationCreateView,DeviationDeleteView,DashboardView

urlpatterns = [
    path('',InsightDataListView.as_view(),name='list-data'),
    path('dashboard',DashboardView,name='dashboard'),
    path('create',InsightDataCreateView.as_view(),name='create-data'),
    path('<str:pk>/edit',InsightDataUpdateView.as_view(),name='update-data'),
    path('<str:pk>/delete',InsightDataDeleteView.as_view(),name='delete-data'),
    path('deviation',DeviationListView,name='list-deviation'),
    path('create-deviation/<int:pk>',DeviationCreateView,name='create-deviation'),
    path('deviation/<int:pk>',DeviationUpdateView.as_view(),name='update-deviation'),
    path('deviation/<str:pk>/delete',DeviationDeleteView.as_view(),name='delete-deviation'),
    path('deviation/filter',FilterForm,name='filter'),
    path('deviation/deployment',DeviationDeploymentView,name='dev-dashboard')

]
