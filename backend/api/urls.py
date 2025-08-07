from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParentViewSet, ChildViewSet, ScoreTransactionViewSet, RewardViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'parents', ParentViewSet, basename='parent')
router.register(r'children', ChildViewSet, basename='child')
router.register(r'score-transactions', ScoreTransactionViewSet, basename='scoretransaction')
router.register(r'rewards', RewardViewSet, basename='reward')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
