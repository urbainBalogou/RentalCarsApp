from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from list.models import Client
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator  # Import correct
from django.urls import reverse
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.hashers import make_password
from django.contrib import messages

User = get_user_model()

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        mail = request.POST.get("mail")
        tel = request.POST.get("telephone")
        nom = request.POST.get("username")
        prenom = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            messages.error(request,"Un utilisateur existe déjà avec ce nom")
            return render(request, 'accounts/signup.html')
        if User.objects.filter(email=mail).exists():
            messages.error(request,"Un utilisateur déjà enregistré avec cet email")
            return render(request, 'accounts/signup.html')


        user = User.objects.create_user(
            email=mail,
            username=username,
            password=password,
        )
        client = Client(nom=nom,
                        prenom=prenom,
                        numero_tel=tel,
                        email=mail)
        client.save()

        login(request, user, backend='accounts.backend.EmailBackend')
        return redirect('index')
    return render(request, 'accounts/signup.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('password')
        #print(f"email: {email}")
        #print(f"password: {password}")
        if not email or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'accounts/login.html')

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect('index')
        else:
            messages.error(request, "Identifiants invalides.")
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')





def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            # Vérifie si l'email est associé à un utilisateur
            user = User.objects.get(email=email)

            # Générer le lien de réinitialisation
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)  # Correction ici
            lien_reset = f"http://{current_site.domain}{reverse('password_reset_confirm', args=[uid, token])}"

            # Préparer l'email
            sujet = "Réinitialisation de votre mot de passe"
            message = f"""
            Bonjour,

            Vous avez demandé à réinitialiser votre mot de passe. Cliquez sur le lien ci-dessous pour définir un nouveau mot de passe :
            {lien_reset}

            Si vous n'avez pas demandé cette réinitialisation, ignorez cet email.

            Cordialement,
            L'équipe de support.
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            # Envoyer l'email
            send_mail(
                subject=sujet,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,  # Affiche une erreur en cas de problème
            )

            return render(request, 'accounts/password_reset/password_reset_complete.html')
        except User.DoesNotExist:
            # Si l'email n'existe pas, montrer un message générique (pour éviter de révéler l'existence des comptes)
            return render(request, 'accounts/password_reset/password_reset_confirm.html')
    return render(request, 'accounts/password_reset/password_reset_email.html')


def PasswordResetConfirmView(request, uidb64, token):
    try:
        # Décoder l'UID pour obtenir l'utilisateur
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Vérifier si le token est valide pour cet utilisateur
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            # Récupérer le mot de passe saisi
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("password2")

            # Vérifier que les mots de passe correspondent
            if new_password and new_password == confirm_password:
                # Modifier le mot de passe de l'utilisateur
                user.password = make_password(new_password)
                user.save()

                # Rediriger vers la page de connexion avec un message de succès
                return redirect('login')  # Nom de la vue de connexion
            else:
                # Si les mots de passe ne correspondent pas, renvoyer une erreur
                return render(request, 'accounts/password_reset/password_reset_form.html', {
                    'uidb64': uidb64,
                    'token': token,
                    'error': "Les mots de passe ne correspondent pas.",
                })

        # Afficher le formulaire de réinitialisation de mot de passe
        return render(request, 'accounts/password_reset/password_reset_form.html', {
            'uidb64': uidb64,
            'token': token,
        })
    else:
        # Si le lien est invalide ou expiré
        return render(request, 'accounts/password_reset/password_reset_invalid.html')
