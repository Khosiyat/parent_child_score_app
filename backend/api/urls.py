from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParentViewSet, ChildViewSet, ScoreTransactionViewSet, RewardViewSet, RegisterView, ScoreTransactionCreateView, RewardListView, RedeemRewardView

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
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/score-transactions/', ScoreTransactionCreateView.as_view(), name='score-transaction-create'),
    path('api/rewards/', RewardListView.as_view(), name='reward-list'),
    path('api/rewards/redeem/', RedeemRewardView.as_view(), name='reward-redeem'),
]
