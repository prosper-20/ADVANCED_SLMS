from rest_framework import serializers
from courses.models import Course, Subject
from users.models import User

class StudentCourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"



class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    
    def save(self):
        user = User(
            email = self.validated_data["email"],
            username = self.validated_data["username"]
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({"Error": "Both passwords must match"})
        user.set_password(password)
        user.save()
        return user


