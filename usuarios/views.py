from allauth.socialaccount.models import SocialToken, SocialAccount
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, force_str, smart_bytes, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer, RegistroSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from usuarios.permissions import IsOwnerOrAdmin
import json

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer
    permission_classes = [IsOwnerOrAdmin]

    # Apenas superusuários podem listar todos os usuários
    # Usuários comuns só podem listar a si mesmos
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            email = self.request.query_params.get('email')
            if email:
                return Usuario.objects.filter(email=email)
            return Usuario.objects.all()
        return Usuario.objects.filter(id=user.id)
    
    # Médicos podem buscar pacientes pelo email
    @action(detail=False, methods=['get'], url_path='busca-paciente-email')
    def busca_paciente_email(self, request):
        user = self.request.user

        # Permitir apenas médicos
        if not user.is_medico:
            raise PermissionDenied("Você não tem permissão para acessar esse recurso.")

        # Buscar paciente pelo email
        email = self.request.query_params.get('email')
        if not email:
            return Response(
                {"detail": "O parâmetro 'email' é obrigatório."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            paciente = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise NotFound("Paciente não encontrado com o email fornecido.")

        serializer = self.get_serializer(paciente)
        return Response(serializer.data)

class RegistroUsuario(generics.CreateAPIView):
    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Chama o método create do serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Cria o usuário
        user = serializer.save()

        # Retorna a resposta personalizada
        return Response(
            {"message": "Usuário criado com sucesso!"},
            status=status.HTTP_201_CREATED
        )

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(
            {'success': True, 'message': 'Email para redefinição de senha enviado.'},
            status=status.HTTP_200_OK
        )

class PasswordTokenCheckAPI(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Usuario.objects.get(id=id)

            return Response(
                {'success': True, 'message': 'Token válido.', 'uidb64': uidb64, 'token': token},
                status=status.HTTP_200_OK
            )
                
        except DjangoUnicodeDecodeError as identifier:
            return Response(
                    {'error': 'Token inválido.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

class SetNewPasswordAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'success': True, 'message': 'Senha redefinida com sucesso!'},
            status=status.HTTP_200_OK
        )

@login_required
def google_login_callback(request):
    user = request.user

    social_accounts = SocialAccount.objects.filter(user=user)
    # print(f"Social account for user: {social_accounts}")

    social_account = social_accounts.first()

    if not social_account:
        # print(f"No social account found for user {user}")
        return redirect(f'{settings.FRONTEND_URL}/login/callback/?error=NoSocialAccount')
    
    token = SocialToken.objects.filter(account=social_account, account__provider='google').first()

    if token:
        # print(f"Google token found: {token.token}")
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        return redirect(f'{settings.FRONTEND_URL}/login/callback/?access_token={access_token}')
    else:
        # print(f'No Google token found for user: {user}')
        return redirect(f'{settings.FRONTEND_URL}/login/callback/?error=NoGoogleToken')
    
@csrf_exempt
def validate_google_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            google_access_token = data.get('access_token')

            if not google_access_token:
                return JsonResponse({'detail': 'O campo access_token é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({'valid': True})
        except json.JSONDecodeError:
            return JsonResponse({'detail': 'Json inválido.'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
