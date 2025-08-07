from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Parent, Child, ScoreTransaction, Reward
from .serializers import (
    ParentSerializer, ChildSerializer, ScoreTransactionSerializer, RewardSerializer,
    UserSerializer
)
from .permissions import IsParent, IsChild, IsOwnerOrParent

User = get_user_model()

class ParentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]

class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrParent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'parent':
            parent = user.parent_profile
            return parent.children.all()
        elif user.role == 'child':
            return Child.objects.filter(user=user)
        return Child.objects.none()

    def perform_create(self, serializer):
        # Only allow parents to create children
        if self.request.user.role == 'parent':
            child = serializer.save()
            child.parents.add(self.request.user.parent_profile)

class ScoreTransactionViewSet(viewsets.ModelViewSet):
    queryset = ScoreTransaction.objects.all().order_by('-created_at')
    serializer_class = ScoreTransactionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsParent]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'parent':
            parent = user.parent_profile
            return ScoreTransaction.objects.filter(parent=parent)
        elif user.role == 'child':
            child = user.child_profile
            return ScoreTransaction.objects.filter(child=child)
        return ScoreTransaction.objects.none()

class RewardViewSet(viewsets.ModelViewSet):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsParent]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'parent':
            parent = user.parent_profile
            return Reward.objects.filter(parent=parent)
        elif user.role == 'child':
            # Return all rewards of parents of the child
            child = user.child_profile
            parents = child.parents.all()
            return Reward.objects.filter(parent__in=parents)
        return Reward.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def redeem(self, request, pk=None):
        reward = self.get_object()
        user = request.user
        if user.role != 'child':
            return Response({'detail': 'Only children can redeem rewards.'}, status=status.HTTP_403_FORBIDDEN)

        child = user.child_profile
        if child.score_balance < reward.cost:
            return Response({'detail': 'Not enough points to redeem this reward.'}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct points via ScoreTransaction
        ScoreTransaction.objects.create(
            child=child,
            parent=None,
            points=-reward.cost,
            transaction_type='redeem',
            description=f'Redeemed reward: {reward.name}'
        )

        return Response({'detail': f'Reward {reward.name} redeemed successfully!'}, status=status.HTTP_200_OK)
