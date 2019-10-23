from rest_framework import serializers

from .models import Company, User, Transfer

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('id', 'url', 'datetime', 'resource', 'transferred', 'user')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'url', 'name', 'quota')

class UserSerializer(serializers.ModelSerializer):
    company_details = CompanySerializer(source="company", read_only=True)
    class Meta:
        model = User
        fields = ('id', 'url', 'name', 'email', 'company', 'company_details')


# Alternative: to show all users' transfers on users api address
# and all companies' users on companies api address:

# class UserSerializer(serializers.ModelSerializer):
#     transfers = TransferSerializer(many=True, read_only=True)
#     # transferred = TransferSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = User
#         fields = ('id', 'url', 'name', 'email', 'company', 'transfers')
#
# class CompanySerializer(serializers.ModelSerializer):
#     users = UserSerializer(many=True, read_only=True)
#     class Meta:
#         model = Company
#         fields = ('id', 'url', 'name', 'quota', 'users')


