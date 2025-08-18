# backend/api/views.py

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Parent, Child, ScoreTransaction, Reward, RewardRequest
from .serializers import (
    ParentSerializer,
    ChildSerializer,
    ScoreTransactionSerializer,
    RewardSerializer,
    RewardRequestSerializer,
    UserSerializer,
)
from .permissions import IsParent, IsChild, IsOwnerOrParent

User = get_user_model()


# ---------------------------
# Auth/Users
# ---------------------------

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role')

        if not username or not password or role not in ['parent', 'child']:
            return Response({'detail': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, role=role)

        if role == 'parent':
            Parent.objects.create(user=user)
        else:
            Child.objects.create(user=user)

        return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'username': user.username, 'role': user.role})


# ---------------------------
# Parents
# ---------------------------

class ParentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParent]


# ---------------------------
# Children
# ---------------------------

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
        # Only allow parents to create children and auto-link to themselves
        if self.request.user.role != 'parent':
            raise PermissionDenied('Only parents can create children.')
        child = serializer.save()
        child.parents.add(self.request.user.parent_profile)


# ---------------------------
# Score Transactions
# ---------------------------

class ScoreTransactionViewSet(viewsets.ModelViewSet):
    """
    Parents:
      - list: all transactions for their children (including child-initiated redemptions)
      - create/update/delete: allowed (add/subtract/redeem on behalf if desired)
    Children:
      - list: only their own transactions
      - create/update/delete: not allowed
    """
    serializer_class = ScoreTransactionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsParent]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'parent':
            parent = user.parent_profile
            # Show all transactions for the parent's children (not just those created by this parent),
            # so redemptions (which have parent=None) are visible.
            return ScoreTransaction.objects.filter(
                child__in=parent.children.all()
            ).order_by('-created_at')
        elif user.role == 'child':
            child = user.child_profile
            return ScoreTransaction.objects.filter(child=child).order_by('-created_at')
        return ScoreTransaction.objects.none()

    def perform_create(self, serializer):
        # Only parents reach here due to permissions; attach the acting parent
        parent = self.request.user.parent_profile
        serializer.save(parent=parent)


# ---------------------------
# Rewards
# ---------------------------

class RewardViewSet(viewsets.ModelViewSet):
    serializer_class = RewardSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsParent]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'parent':
            parent = user.parent_profile
            return Reward.objects.filter(parent=parent)
        elif user.role == 'child':
            # Rewards offered by any of the child's parents
            child = user.child_profile
            parents = child.parents.all()
            return Reward.objects.filter(parent__in=parents)
        return Reward.objects.none()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def redeem(self, request, pk=None):
        """
        Child self-redeems a reward:
          - Creates a ScoreTransaction with transaction_type='redeem'
          - Parent is left as None (or could attach a parent if you want a specific one)
        """
        reward = self.get_object()
        user = request.user

        if user.role != 'child':
            return Response({'detail': 'Only children can redeem rewards.'}, status=status.HTTP_403_FORBIDDEN)

        child = user.child_profile
        if child.score_balance < reward.cost:
            return Response({'detail': 'Not enough points to redeem this reward.'}, status=status.HTTP_400_BAD_REQUEST)

        ScoreTransaction.objects.create(
            child=child,
            parent=None,  # redemption without a specific parent actor
            points=-reward.cost,
            transaction_type='redeem',
            description=f'Redeemed reward: {reward.name}',
        )

        return Response({'detail': f'Reward {reward.name} redeemed successfully!'}, status=status.HTTP_200_OK)


# ---------------------------
# Reward Requests (Child -> Parent approval)
# ---------------------------

class RewardRequestViewSet(viewsets.ModelViewSet):
    """
    Children:
      - create: request a reward
      - list/retrieve: view their own requests
    Parents:
      - list: see pending requests for their children (approved=False)
      - approve: custom action to approve and deduct points
    """
    serializer_class = RewardRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'parent':
            parent = user.parent_profile
            # Pending requests for this parent's children
            return RewardRequest.objects.filter(
                child__in=parent.children.all()
            ).order_by('-requested_at')
        elif user.role == 'child':
            child = user.child_profile
            return RewardRequest.objects.filter(child=child).order_by('-requested_at')
        return RewardRequest.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'child':
            raise PermissionDenied('Only children can create reward requests.')
        child = user.child_profile

        reward = serializer.validated_data.get('reward')
        # Ensure the requested reward is from one of the child's parents
        if reward.parent not in child.parents.all():
            raise PermissionDenied('You can only request rewards from your own parent(s).')

        serializer.save(child=child, approved=False)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsParent])
    def approve(self, request, pk=None):
        """
        Parent approves a pending reward request:
          - Verifies parent-child relation
          - Deducts points via a 'redeem' ScoreTransaction
        """
        try:
            req = self.get_queryset().get(pk=pk)
        except RewardRequest.DoesNotExist:
            return Response({'detail': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

        if req.approved:
            return Response({'detail': 'Request already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        parent_user = request.user
        parent = parent_user.parent_profile

        # Security: ensure this child belongs to this parent
        if parent not in req.child.parents.all():
            return Response({'detail': 'Not authorized for this child.'}, status=status.HTTP_403_FORBIDDEN)

        # Check balance and redeem
        if req.child.score_balance < req.reward.cost:
            return Response({'detail': 'Child does not have enough points.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create redemption transaction; attach acting parent
        ScoreTransaction.objects.create(
            child=req.child,
            parent=parent,
            points=-req.reward.cost,
            transaction_type='redeem',
            description=f"Approved reward: {req.reward.name}",
        )

        # Mark request approved
        req.approved = True
        req.approved_at = timezone.now()
        req.approved_by = parent_user
        req.save(update_fields=['approved', 'approved_at', 'approved_by'])

        return Response({'detail': 'Reward request approved and points deducted.'}, status=status.HTTP_200_OK)
