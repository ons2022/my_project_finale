from rest_framework.decorators import api_view ,permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    is_admin = request.data.get('is_admin', False)

    # Check if username and password are provided
    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = is_admin  # Assign admin role if needed
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
    except IntegrityError:
        return Response({'error': 'An error occurred while creating the user.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        
        role = 'admin' if user.is_staff else 'user'  # Use is_staff to check admin status

        # Return the JWT tokens and the role
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': role
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])  # Only allow admins
def get_all_users(request):
    users = User.objects.all().values('id', 'username', 'is_staff', 'is_active')
    return Response(users, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])  # Only allow admins
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
