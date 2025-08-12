from rest_framework import serializers
from .models import User, Parent, Child, ScoreTransaction, Reward

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Parent
        fields = ['id', 'user']

class ChildSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    parents = ParentSerializer(many=True, read_only=True)
    score_balance = serializers.IntegerField(read_only=True)

    class Meta:
        model = Child
        fields = ['id', 'user', 'parents', 'score_balance']

class ScoreTransactionSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(read_only=True)
    child = serializers.PrimaryKeyRelatedField(queryset=Child.objects.all())

    class Meta:
        model = ScoreTransaction
        fields = ['id', 'child', 'parent', 'points', 'transaction_type', 'description', 'created_at']
        read_only_fields = ['parent', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        # Attach parent from logged-in user if role=parent
        if request and hasattr(request, 'user') and request.user.role == 'parent':
            parent = request.user.parent_profile
            validated_data['parent'] = parent
        return super().create(validated_data)

class RewardSerializer(serializers.ModelSerializer):
    parent = ParentSerializer(read_only=True)

    class Meta:
        model = Reward
        fields = ['id', 'parent', 'name', 'cost', 'description']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.role == 'parent':
            validated_data['parent'] = request.user.parent_profile
        return super().create(validated_data)



from .models import ScoreTransaction, Reward

class ScoreTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreTransaction
        fields = ['id', 'child', 'points', 'description', 'created_at']

class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = ['id', 'name', 'cost', 'description']
