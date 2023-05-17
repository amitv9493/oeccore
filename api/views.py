from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import generics
from django_filters import rest_framework as filters
from django.core.cache import cache
from rest_framework.filters import OrderingFilter
# Create your views here.

# =======================================================================

from rest_framework import status
from django.http import HttpResponse

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

# ==========================================================================

# function based api_view

# @api_view(["GET","POST"])
# def enquiry_list(request):
#     if request.method =="GET":
#         enquirydata = enquiry.objects.all()
#         serializer = enquirySerializers(enquirydata, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = enquirySerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# @api_view(["GET", "DELETE", "PUT","PATCH"])
# def enquiry_detail(request, pk):
#     try:
#         enquirydata = enquiry.objects.get(pk=pk)
#     except enquiry.DoesNotExist:
#         return Response(data=None, status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         serializer = enquirySerializers(enquirydata)
#         return Response(serializer.data)
    
#     elif request.method == "PUT":
#         id = pk
#         enquirydata = enquiry.objects.get(pk=id)
#         serializer = enquirySerializers(enquirydata, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == "PATCH":
#         id = pk
#         enquirydata = enquiry.objects.get(pk=id)
#         serializer = enquirySerializers(enquirydata, data=request.data, partial =True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == "DELETE":
#         enquirydata.delete()
#         return Response(data=None,status=status.HTTP_204_NO_CONTENT)


# =====================================================================
# generic class based views with mixins 

# viewsets 

# Modelviewset
from rest_framework.viewsets import ModelViewSet
from .persmissions import Mypermission
from rest_framework.permissions import  DjangoModelPermissions, IsAdminUser
from rest_framework import authentication
from django.db.models import Q
from .serializers import *
from application.models import Application
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .renderers import UserRenderes
from .paginator import CustomPagination
from enquiry.models import Course
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter
# ENQUIRY VIEWS 

from rest_framework.generics import ListAPIView

class course_view_only(ListAPIView):
    # permission_classes = [DjangoModelPermissions, IsAdminUser]
    # authentication_classes= [ JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["^course_name"]
    filterset_fields = [
        'university',
        'course_levels',
        'intake',
        
    ]
    
    def get_queryset(self):
        
        # qs = super().get_queryset().select_related('university')
        # qs = qs.prefetch_related('intake')
        ielts_score = self.request.query_params.get('ielts_score')
        pte_score = self.request.query_params.get('pte_score')
        tofel_score = self.request.query_params.get('tofel_score')
        intake = self.request.query_params.get('intake')

        query = Q()  # Initialize an empty Q object

        if intake:
            query |= Q(intake=intake)
        if ielts_score:
            query |= Q(university__ielts_score__lte=ielts_score)
        if pte_score:
            query |= Q(university__pte__lte=pte_score)
        if tofel_score:
            query |= Q(university__tofel__lte=tofel_score)

        cache_key = 'course_queryset'
        queryset = cache.get(cache_key)
        if queryset is None:
            queryset = super().get_queryset().select_related('university').prefetch_related('intake')
            cache.set(cache_key, queryset)
            queryset = queryset.filter(query)
        return queryset
            

    # queryset = Course.objects.exclude(university__active = False).exclude(Active=False)
    queryset = Course.objects.filter(university__active = True, Active=True)
    serializer_class = course_serializer_view_only
    pagination_class = CustomPagination

class university_view(ListAPIView):
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    queryset = University.objects.exclude(active = False)
    serializer_class = uni_serializer
    # pagination_class = CustomPagination

class application_status_view(ListAPIView):
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    queryset = application_status.objects.all()
    serializer_class = applicationStatusserializer
    
class current_education_view(ListAPIView):
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    queryset = current_education.objects.all()
    serializer_class = currentEducationSerializer    
    
class assigned_user_view(ListAPIView):
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    queryset = User.objects.filter(is_active=True)
    serializer_class = userlist
    
class enquiry_status_view(ListAPIView):
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    queryset = enquiry_status.objects.all()
    serializer_class = enquiryStatusSerializer
    
class course_level_view(ListAPIView):
        permission_classes = [DjangoModelPermissions, IsAdminUser]
        authentication_classes= [ JWTAuthentication]
        filter_backends =[DjangoFilterBackend]
        queryset = course_levels.objects.all()
        serializer_class = Levelserializer

class countryview(ListAPIView):
        permission_classes = [DjangoModelPermissions, IsAdminUser]
        authentication_classes= [ JWTAuthentication]
        filter_backends =[DjangoFilterBackend]
        queryset = Country.objects.all()
        serializer_class = countryserializer

class intakeView(ListAPIView):
    
        permission_classes = [DjangoModelPermissions, IsAdminUser]
        authentication_classes= [ JWTAuthentication]
        serializer_class = intakeserializer
        filter_backends =[DjangoFilterBackend]
        queryset = intake.objects.all()
        
        
'''==========================================================='''




from django.core.paginator import Paginator


class new_enquiry_view(APIView):
    def get(self, request):
        # Extract the parameters from the AJAX request
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", "")
        order_column_index = int(request.GET.get("order[0][column]", 0))

        # Check that order_column_index is a valid index
        num_columns = int(request.GET.get("columns", 0))
        if order_column_index < 0 or order_column_index >= num_columns:
            order_column_index = 0

        order_column_name = request.GET.get(
            "columns[%d][data]" % order_column_index, "id"
        )
        order_direction = request.GET.get("order[0][dir]", "asc")

        # Build the queryset based on the parameters
        queryset = enquiry.objects.all()
        if search_value:
            queryset = queryset.filter(
                Q(student_name__icontains=search_value)
                | Q(university_interested__univ_name__icontains=search_value)
                | Q(level_applying_for__levels=search_value)
                | Q(course_interested__course_name__icontains=search_value)
                | Q(enquiry_status__status__icontains=search_value)
            )
        queryset = queryset.order_by(
            "%s%s" % ("-" if order_direction == "desc" else "", order_column_name)
        )

        # Paginate the queryset based on the start and length parameters
        paginator = Paginator(queryset, length)
        queryset_page = paginator.get_page(start // length + 1)
        queryset_page_list = queryset_page.object_list

        # Serialize the queryset to JSON
        serializer = enquirySerializers(queryset_page_list, many=True)

        # Build the response
        data = {
            "draw": int(request.GET.get("draw", 0)),
            "recordsTotal": enquiry.objects.count(),
            "recordsFiltered": queryset.count(),
            "data": serializer.data,
        }

        return Response(data)
    
        
class enquiryViewset(ModelViewSet):

    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    queryset = enquiry.objects.prefetch_related('country_interested',
                                                'university_interested',
                                                'course_interested',
                                                'level_applying_for',
                                                'intake_interested',
                                                'assigned_users',
                                                'current_education',
                                                'enquiry_status',
                                                )
    serializer_class = enquirySerializers
    filter_backends =[DjangoFilterBackend, SearchFilter,OrderingFilter]
    
    search_fields = ['^student_name', '^student_phone', '^student_email',]
    
    filterset_fields = ['course_interested','assigned_users','university_interested','intake_interested','enquiry_status','level_applying_for']
    
    pagination_class = CustomPagination
    OrderingFilter = ['date_created']


    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception:
            return Response({"msg":"detail not found"}, status=status.HTTP_204_NO_CONTENT)
        return super().retrieve(request, *args, **kwargs)
    



    def perform_create(self, enquirySerializers):
        enquirySerializers.save(added_by=self.request.user)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs

        return qs.filter(Q(added_by=self.request.user) | Q(assigned_users=self.request.user))
    
from rest_framework import mixins

class add_enquiry(generics.CreateAPIView):
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    serializer_class = enquiry_add_serializer
    queryset = enquiry.objects.all()
    
    def perform_create(self, enquiry_add_serializer):
        enquiry_add_serializer.save(added_by=self.request.user)
    
    
class update_enquiry(generics.RetrieveUpdateDestroyAPIView):
    
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    serializer_class = enquiry_add_serializer
    queryset = enquiry.objects.all()
    
    def perform_update(self, enquiry_add_serializer):
        enquiry_add_serializer.save(added_by=self.request.user)
        
        
        
# APPLICATION VIEWS 
class enquiry_view(ListAPIView):
    
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    queryset = enquiry.objects.all()
    serializer_class = enquiry_view_serializer
    
class new_application_view(APIView):
    def get(self, request):
        # Extract the parameters from the AJAX request
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        order_column_index = int(request.GET.get('order[0][column]', 0))

        # Check that order_column_index is a valid index
        num_columns = int(request.GET.get('columns', 0))
        if order_column_index < 0 or order_column_index >= num_columns:
            order_column_index = 0
        
        order_column_name = request.GET.get('columns[%d][data]' % order_column_index, 'id')
        order_direction = request.GET.get('order[0][dir]', 'asc')

        # Build the queryset based on the parameters
        queryset = Application.objects.all()
        if search_value:
            queryset = queryset.filter(
                Q(name__student_name__icontains=search_value)\
                | Q(assigned_users__username__icontains= search_value)\
                | Q(added_by__username__icontains = search_value))
                
        queryset = queryset.order_by('%s%s' % ('-' if order_direction == 'desc' else '', order_column_name))

        # Paginate the queryset based on the start and length parameters
        paginator = Paginator(queryset, length)
        queryset_page = paginator.get_page(start // length + 1)
        queryset_page_list = queryset_page.object_list

        # Serialize the queryset to JSON
        serializer = applicationserializers(queryset_page_list, many=True)

        # Build the response
        data = {
            'draw': int(request.GET.get('draw', 0)),
            'recordsTotal': Application.objects.count(),
            'recordsFiltered': queryset.count(),
            'data': serializer.data,
        }

        return Response(data)
        
class applicationViewset(ModelViewSet):
    
    
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    serializer_class = applicationserializers
    filter_backends =[DjangoFilterBackend, SearchFilter,OrderingFilter]
    search_fields = ['name__student_name',]
    filterset_fields =['name','assigned_users', 'status',]
    OrderingFilter = ['created_at']
    pagination_class = CustomPagination

    queryset = Application.objects.prefetch_related(
        'name',
        'assigned_users',
        'status',
    )

    def get_queryset(self):
            qs = super().get_queryset()
            if self.request.user.is_superuser:
                return qs
            
            return qs.filter(assigned_users=self.request.user)

    def perform_create(self, enquirySerializers):
        enquirySerializers.save(added_by=self.request.user)

class add_application(generics.CreateAPIView):
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    serializer_class = application_update_serializer
    queryset = Application.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, application_update_serializer):        
        application_update_serializer.save(added_by=self.request.user)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs

        return qs.filter(Q(added_by=self.request.user) | Q(assigned_users=self.request.user))
    

class update_application(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    serializer_class = application_update_serializer
    queryset = Application.objects.all()
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, application_update_serializer):
        application_update_serializer.save(added_by=self.request.user)
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs

        return qs.filter(Q(added_by=self.request.user) | Q(assigned_users=self.request.user))
    

class courseViewset(ModelViewSet):

    permission_classes = [DjangoModelPermissions, IsAdminUser]
    authentication_classes= [ JWTAuthentication]
    serializer_class = CourseSerializers
    filter_backends =[DjangoFilterBackend]
    filterset_fields =['university','course_levels', 'course_name',]
    pagination_class = CustomPagination
    queryset = Course.objects.prefetch_related(
        'university',
        'course_levels',
        'documents_required',
        'course_requirements',
    ).filter(university__active =True)


class university_filter(filters.FilterSet):
    ielts_max = filters.NumberFilter(field_name="ielts_score", lookup_expr='gte')
    ielts_min = filters.NumberFilter(field_name="ielts_score", lookup_expr='lte')
    
    tofel_max = filters.NumberFilter(field_name="tofel", lookup_expr='gte')
    tofel_min = filters.NumberFilter(field_name="tofel", lookup_expr='lte')
    
    pte_max  = filters.NumberFilter(field_name='pte',lookup_expr='gte')
    pte_min = filters.NumberFilter(field_name='pte',lookup_expr='lte')
    
    english_waiver_max = filters.NumberFilter(field_name='english_waiver',lookup_expr='gte')
    english_waiver_min = filters.NumberFilter(field_name='english_waiver',lookup_expr='lte')
    
    academic_max = filters.NumberFilter(field_name='academic_requirement',lookup_expr='gte')
    academic_min = filters.NumberFilter(field_name='academic_requirement',lookup_expr='lte')
    
    gap_max = filters.NumberFilter(field_name='gap',lookup_expr='gte')
    gap_min =filters.NumberFilter(field_name='gap',lookup_expr='lte')
    
    # english_requirement = filters.ModelMultipleChoiceFilter(field_name='english_requirement',queryset = UniversityRequirements.objects.all())
    # (field_name='english_requirement')

    class Meta:
        model = University
        fields = ['ielts_score',
                  'tofel',
                  'pte',
                  'gap',
                  'academic_requirement',
                  'english_waiver',
                  
                  ]


class UniversityListView(generics.ListAPIView):
    # permission_classes = [DjangoModelPermissions, IsAdminUser]
    # authentication_classes= [ JWTAuthentication]
    serializer_class = UniversitySerializer
    filter_backends =[DjangoFilterBackend]
    filterset_fields =['univ_name','country',]
    pagination_class = CustomPagination
    filterset_class = university_filter
    queryset = University.objects.all()
    serializer_class.Meta.fields = ['id',
                                    'univ_name', 
                                    # 'univ_logo',
                                    # 'univ_email',
                                    # 'univ_website',
                                    # 'active',
                                    # 'univ_phone', 
                                    # 'country',
                                    ]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(active=True)
    
class UniversityCreateView(generics.CreateAPIView):
    serializer_class = UniversitySerializer
    filter_backends =[DjangoFilterBackend]
    filterset_fields =['univ_name','country',]
    pagination_class = CustomPagination
    queryset = University.objects.all()
    

'''============================================================================'''



# class University_requirement_view(generics.ListAPIView):
#     queryset = UniversityRequirements.objects.all()
#     serializer_class = UniversityRequirements_Serializer
    
#     # permission_classes = [DjangoModelPermissions, IsAdminUser]
#     # authentication_classes= [ JWTAuthentication]
#     filter_backends =[DjangoFilterBackend]
#     # filterset_fields ={
#     #     'english_waiver':['gte', 'lte'],
#     #     'academic_requirement':['gte', 'lte'],
#     #     'ielts_score':['gte', 'lte'],
#     #     'tofel':['gte', 'lte'],
#     #     'pte':['gte', 'lte'],
#     #     'gap':['gte', 'lte'],
#     #     'english_requirement':['exact'],        
        
        
#     # }
#     filterset_fields = [
#         'english_requirement',
#         'board_not_eligible',
#         'placement_option',
#         'dependency_acceptance',
#         'gap',
#     ]
    
#     pagination_class = CustomPagination
#     filterset_class = university_filter

'''=================================================================================='''

'''Broadcast Message and recent actions Views'''

from rest_framework import authentication
from rest_framework import permissions

from django.contrib.admin.models import LogEntry
class Broadcast_view(generics.ListAPIView):
    queryset = BroadcastMessage.objects.all()
    serializer_class = Broadcast_Message_Serializer
    

    
class recentactions_view(generics.ListAPIView):
    queryset = LogEntry.objects.exclude(change_message = "No fields changed.").filter(content_type__id__in = [17,18]).order_by('-action_time')
    serializer_class = recentAction_Serializer

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_superuser:
            return qs[:10]
        else:
            print('else ran')
            qs = qs.filter(user= self.request.user.id)[:10]
            return qs

'''=================================================================================='''



'''=================================================================================='''

'''USER LOGIN VIEWS '''


from .serializers import ChangePasswordSerializer, LoginSerializer, PasswordResetSerializer, ResetPasswordSerializer, UserProfileSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .renderers import UserRenderes
from django.contrib.auth.models import Group

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    
    def post(self,request, format =None ):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # email = serializer.data.get('email')
            username= serializer.data.get('username')
            password= serializer.data.get('password')
            user =authenticate(username=username, password=password)

            if user is not None:
                try:
                    user_group = (Group.objects.get(user=user.id)).name
                except Exception as e:
                    print("No group assigned to user")
                    user_group = "None"
                    
               
                token= get_tokens_for_user(user)
                return Response({"token":token,"msg":"Login Successful","userid":user.id,"user_status":user_group}, status=status.HTTP_200_OK)

            return Response({"errors":{"msg":-1}}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProfileView(APIView):
    renderer_classes =[UserRenderes]
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    def get(self, request, format=None ):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    renderer_classes =[UserRenderes]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data, context={"user":request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password changed"})
        
        return Response(serializer.errors)



class SendPasswordResetView(APIView):
    renderer_classes = [UserRenderes]
    def post(self, request, format=None):
        # try:
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                return Response({'msg':"Temporary password has been sent to the email id!"}, status=status.HTTP_200_OK)
        # except AssertionError:
        #     return Response({"error":"Not a valid data"})

class PasswordResetView(APIView):
    renderer_classes = [UserRenderes]
    def post(self, request, uid, token, format=None):
        serializer = ResetPasswordSerializer(data=request.data, context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":'password reset successfully'}, status=status.HTTP_200_OK)
            
from comment.models.comments import Comment

class EnquiryCommentView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends =[DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_fields = [ 'object_id']
    ordering = ['posted', 'edited']
    def get_queryset(self):
        qs =  super().get_queryset()
        qs.filter(content_type = 17)
        return qs 

class EnquiryCommentCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    serializer_class = CreateCommentSerializer
    filter_backends =[DjangoFilterBackend, SearchFilter,OrderingFilter]
    
    def create(self, request, *args, **kwargs):
        request.data['content_type'] = 17  # Set the default value for the required field
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, CreateCommentSerializer):
        CreateCommentSerializer.save(user = self.request.user)