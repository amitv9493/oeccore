from rest_framework import serializers

from enquiry.models import enquiry, Course, University
from application.models import Application
from master.models import *
from django.contrib.auth.models import User
# from notifications.models import Notification
from django.core.mail import EmailMessage
from django.conf import settings
from .passwordGenerator import GeneratePassword
from django.contrib.admin.models import LogEntry
from broadcasts.models import BroadcastMessage


from django.contrib.contenttypes.models import ContentType

        
class enquiry_view_serializer(serializers.ModelSerializer):
    class Meta:
        model = enquiry
        fields = ['id','student_name',]

class uni_serializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('id','univ_name',)
    
class course_serializer_view_only(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "course_name", )

class applicationStatusserializer(serializers.ModelSerializer):
    class Meta:
        model = application_status
        fields = "__all__"

class userlist(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class enquiryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = enquiry_status
        fields = "__all__"

class currentEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = current_education
        fields = "__all__"
        
class Levelserializer(serializers.ModelSerializer):
    class Meta:
        model = course_levels
        fields = "__all__"
        
class countryserializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"
        
'''=================================================================================================

                            UNIVERSITY RELATED SERIALIZERS
'''

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = "__all__"

class intakeserializer(serializers.ModelSerializer):
    class Meta:
        model = intake
        fields = "__all__"


class CourseSerializers(serializers.ModelSerializer):
    university = serializers.SlugRelatedField(slug_field='univ_name',queryset=University.objects.all())
    course_levels= serializers.SlugRelatedField(queryset= course_levels.objects.all(), slug_field='levels')
    documents_required= serializers.SlugRelatedField(queryset=documents_required.objects.all(), slug_field='docu_name')
    course_requirements =serializers.SlugRelatedField(queryset=course_requirements.objects.all(), slug_field='requirement')

    class Meta:
        model = Course    
        fields = "__all__"

class application_status_serialzer(serializers.ModelSerializer):
    class Meta:
        model = application_status
        fields = ['id', 'App_status']
        
class enquiry_view_serializer(serializers.ModelSerializer):
    class Meta:
        model = enquiry
        fields = ['id','student_name',]

class applicationserializers(serializers.ModelSerializer):
    name = enquiry_view_serializer()
    assigned_users = userlist()
    status = application_status_serialzer()
    added_by = userlist()

    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ('added_by',)
        
class application_update_serializer(serializers.ModelSerializer):
    class Meta:
        model = Application  
        fields = '__all__'
        read_only_fields = ['added_by']


class enquirySerializers(serializers.ModelSerializer):

    # added_by = serializers.StringRelatedField()
    # country_interested =serializers.SlugRelatedField(slug_field='country_name', queryset=Country.objects.all())
    # university_interested =serializers.SlugRelatedField(slug_field='univ_name', queryset=University.objects.all())
    # course_interested =serializers.SlugRelatedField(slug_field='course_name', queryset=Course.objects.all())
    # level_applying_for =serializers.SlugRelatedField(queryset=course_levels.objects.all(),slug_field='levels')
    # # intake_interested =serializers.StringRelatedField()
    # intake_interested = intakeserializer()
    
    # assigned_users =serializers.SlugRelatedField(queryset=User.objects.filter(is_active=True),slug_field='username')
    # current_education =serializers.SlugRelatedField(queryset=current_education.objects.all(),slug_field='current_education')
    # enquiry_status = serializers.SlugRelatedField(queryset=enquiry_status.objects.all(), slug_field='status')
    

    added_by = userlist()
    country_interested = countryserializer()
    university_interested = uni_serializer()
    course_interested = course_serializer_view_only()
    level_applying_for = Levelserializer()
    intake_interested = intakeserializer()
    
    assigned_users =userlist ()
    current_education = currentEducationSerializer()
    enquiry_status = enquiryStatusSerializer()
    

    class Meta:
        model =  enquiry
        fields = "__all__"
        read_only_fields = ['added_by']

class enquiry_add_serializer(serializers.ModelSerializer):
    class Meta:
        model = enquiry
        fields ="__all__"
        read_only_fields = ['added_by']
        
    # def to_representation(self, instance):
    #     data= super().to_representation(instance)
        #     data['country_interested']= instance.
    #     return data
# =======================================================================================
# UNIVERSITY REQUIREMENT SERIALZER



# =======================================================================================

# class notificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields =['id','timestamp', 'description', 'recipient']
        

# class notificationMarkreadSerializer(serializers.ModelSerializer):

#     mark_read = serializers.BooleanField()
#     class Meta:
#         model = Notification
#         fields =['mark_read']
                                             
    
#     def update(self, instance, validated_data):

#         if validated_data['mark_read'] ==True:
#             instance.mark_as_read()
#             instance.save()
        
#         return super().update(instance, validated_data)


from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password




class UserProfileSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ["id", "first_name", "last_name", "username", "email"]

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    class Meta:
        model=User
        fields = [ 'username' ,'password']


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(max_length=55,style={'input_type':'password'}, write_only=True)
    password = serializers.CharField(max_length=55,style={'input_type':'password'},validators=[validate_password], write_only=True)
    password2 = serializers.CharField(max_length=55,style={'input_type':'password'}, write_only=True)

    class Meta:
        model = User
        fields =['current_password','password','password2']

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        user = self.context.get('user')
        success= user.check_password(attrs['current_password'])

        if not success:
            raise serializers.ValidationError("Current Password do not match")
            
        if password != password2:
            raise serializers.ValidationError("password do not match")
        
        if password == password2 and success:
            user.set_password(password)
            user.save()
            return attrs

"""See imported modules carefully for resetview"""
from .utils import Util
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError 
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PasswordResetSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    class Meta:
        fields = ['email_id']

    def validate(self, attrs):
        email = attrs['email_id']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)
            link = 'http://localhost:8100/api/user/resetpassword/'+uid+'/'+token
            print(link)
            password = GeneratePassword()
            user.set_password(password)
            user.save()
            # send email 
            data={
                'subject':"Reset Your Password",
                'body': "Below is your temporary password. Please Login with this it and change the password. \n" + "temp Password : " + password +'\n' + 'username: '+ user.username,
                'to_email': [user.email]
            }
            
            email = EmailMessage(
                subject= data['subject'],
                body=data['body'],
                from_email= settings.EMAIL_HOST_USER,
                to = data['to_email'],
                )
                
            email.send()
            print("email sent")
            return attrs
        raise serializers.ValidationError("This email is not registered!")


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=55,style={'input_type':'password'},validators=[validate_password], write_only=True)
    password2 = serializers.CharField(max_length=55,style={'input_type':'password'}, write_only=True)

    class Meta:
        fields =['password','password2']

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        uid = self.context.get('uid')
        token = str(self.context.get('token'))
        print(token)
        id = smart_str(urlsafe_base64_decode(uid)) # type: ignore
        user = User.objects.get(id=id)
        
        # try:
        #     if not PasswordResetTokenGenerator().check_token(user, token):
        #         raise serializers.ValidationError("Link is expired or already used!")

        #     if password == password2:
        #         user.set_password(password)
        #         user.save()
        #         return attrs
        #     raise serializers.ValidationError("password do not match")

        # except DjangoUnicodeDecodeError as indentifier:
        #     PasswordResetTokenGenerator().check_token(user,token)
        try:
            if password == password2:
                if PasswordResetTokenGenerator().check_token(user, token):
                    print("token is correct")
                    user.set_password(password)
                    user.save()
                    return attrs
                raise serializers.ValidationError("token is expired or already used!")
            raise serializers.ValidationError("password do not match")
                
        except DjangoUnicodeDecodeError as indentifier:
                PasswordResetTokenGenerator().check_token(user,token)
                raise serializers.ValidationError("Token is not valid or expired.")
                
                
class content_type_serializer(serializers.ModelSerializer):
    app_content = serializers.ReadOnlyField(source = 'app_labeled_name')
    
    class Meta:
        model = ContentType
        fields = ['app_content']

class recentAction_Serializer(serializers.ModelSerializer):
    user = userlist()
    content_type = content_type_serializer()
    class Meta:
        model = LogEntry
        fields = "__all__"
        

        
        
class Broadcast_Message_Serializer(serializers.ModelSerializer):
    class Meta:
        model =BroadcastMessage
        fields = "__all__"
        
from comment.models.comments import Comment
class CommentSerializer(serializers.ModelSerializer):
    user =  userlist()
    class Meta:
        model = Comment
        fields = ['id',
                  'user',
                  'email',
                  'object_id',
                  'content',
                  'posted',
                  'edited',
                  'parent',
                  
                  ]
     
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
