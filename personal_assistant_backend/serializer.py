from rest_framework import serializers


# from student_management_system.studentmanagementsystem.models import Student
from .models import User
from .models import Chat
# from student_management_system.studentmanagementsystem.models import Student
from .models import User

class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
    def create(self,validated_data):
        print("check")
        return User.objects.create(**validated_data)

class UserLoginSerializer(serializers.Serializer):    
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
    def create(self,validated_data):
        print("check")
        return User.objects.create(**validated_data)
    



class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
    def create(self,validated_data):
        print("check")
        return User.objects.create(**validated_data)
    

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
		