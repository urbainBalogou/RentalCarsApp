from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Q
from datetime import datetime, date

from .models import (
    Voiture, Client, Reservation, Chauffeur,
    Facture, Commentaire, Entretien, Document
)
from .serializers import (
    VoitureSerializer, VoitureListSerializer, ClientSerializer,
    ReservationSerializer, ReservationCreateSerializer, ChauffeurSerializer,
    FactureSerializer, CommentaireSerializer, EntretienSerializer,
    DocumentSerializer
)


# ==================== VOITURES API ====================
class VoitureListAPIView(generics.ListAPIView):
    """Liste toutes les voitures disponibles"""
    serializer_class = VoitureListSerializer

    def get_queryset(self):
        queryset = Voiture.objects.all()
        # Filtres optionnels
        disponible = self.request.query_params.get('disponible', None)
        if disponible is not None:
            queryset = queryset.filter(disponibilite=disponible.lower() == 'true')
        return queryset


class VoitureDetailAPIView(generics.RetrieveAPIView):
    """Détail d'une voiture par ID ou slug"""
    serializer_class = VoitureSerializer

    def get_object(self):
        lookup_field = self.kwargs.get('lookup_field')
        if lookup_field.isdigit():
            return get_object_or_404(Voiture, id=lookup_field)
        else:
            return get_object_or_404(Voiture, slug=lookup_field)


@api_view(['GET'])
def voitures_disponibles(request):
    """Retourne les voitures disponibles pour une période donnée"""
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')

    if not date_debut or not date_fin:
        return Response(
            {'error': 'Les paramètres date_debut et date_fin sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
    except ValueError:
        return Response(
            {'error': 'Format de date invalide. Utilisez AAAA-MM-JJ'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Voitures non réservées pour la période
    voitures_reservees = Reservation.objects.filter(
        fin_location__gte=date_debut,
        deb_location__lte=date_fin
    ).values_list('voiture_id', flat=True)

    voitures_disponibles = Voiture.objects.filter(
        disponibilite=True
    ).exclude(id__in=voitures_reservees)

    serializer = VoitureListSerializer(voitures_disponibles, many=True)
    return Response(serializer.data)


# ==================== CLIENTS API ====================
class ClientListCreateAPIView(generics.ListCreateAPIView):
    """Liste et création de clients"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Détail, modification et suppression d'un client"""
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# ==================== RÉSERVATIONS API ====================
class ReservationListAPIView(generics.ListAPIView):
    """Liste toutes les réservations"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        client_id = self.request.query_params.get('client_id', None)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset


class ReservationCreateAPIView(generics.CreateAPIView):
    """Création d'une nouvelle réservation"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationCreateSerializer

    def perform_create(self, serializer):
        reservation = serializer.save()

        # Envoi d'email de confirmation
        try:
            send_mail(
                subject="Nouvelle Réservation",
                message=f"Une nouvelle réservation a été effectuée par {reservation.client.nom} "
                        f"pour la voiture {reservation.voiture.marque} {reservation.voiture.model}. "
                        f"Début : {reservation.deb_location}, Fin : {reservation.fin_location}, "
                        f"Point de livraison : {reservation.lieu}.",
                from_email="elonovacar@site.com",
                recipient_list=["elonovacar@gmail.com", "urbainbalogou19@gmail.com"],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Erreur d'envoi d'email : {e}")


class ReservationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Détail, modification et suppression d'une réservation"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


@api_view(['POST'])
def calculer_prix_reservation(request):
    """Calcule le prix d'une réservation avant la création"""
    voiture_id = request.data.get('voiture_id')
    avec_chauffeur = request.data.get('avec_chauffeur', True)
    region = request.data.get('region', 'maritime')
    date_debut = request.data.get('deb_location')
    date_fin = request.data.get('fin_location')

    if not all([voiture_id, date_debut, date_fin]):
        return Response(
            {'error': 'voiture_id, deb_location et fin_location sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        voiture = Voiture.objects.get(id=voiture_id)
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()

        nombre_jours = (date_fin - date_debut).days + 1

        if avec_chauffeur and region == "maritime":
            prix_jour = voiture.prix_location_ville_chauffeur
        elif avec_chauffeur and region != "maritime":
            prix_jour = voiture.prix_location_hors_ville_chauffeur
        elif not avec_chauffeur and region == "maritime":
            prix_jour = voiture.prix_location_ville_sans_chauffeur
        else:
            prix_jour = voiture.prix_location_hors_ville_sans_chauffeur

        montant_total = prix_jour * nombre_jours

        return Response({
            'voiture': VoitureSerializer(voiture).data,
            'nombre_jours': nombre_jours,
            'prix_par_jour': prix_jour,
            'montant_total': montant_total
        })

    except Voiture.DoesNotExist:
        return Response(
            {'error': 'Voiture non trouvée'},
            status=status.HTTP_404_NOT_FOUND
        )
    except ValueError:
        return Response(
            {'error': 'Format de date invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )


# ==================== CHAUFFEURS API ====================
class ChauffeurListAPIView(generics.ListAPIView):
    """Liste tous les chauffeurs"""
    queryset = Chauffeur.objects.all()
    serializer_class = ChauffeurSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        disponible = self.request.query_params.get('disponible', None)
        if disponible is not None:
            queryset = queryset.filter(disponible=disponible.lower() == 'true')
        return queryset


class ChauffeurDetailAPIView(generics.RetrieveAPIView):
    """Détail d'un chauffeur"""
    queryset = Chauffeur.objects.all()
    serializer_class = ChauffeurSerializer


# ==================== FACTURES API ====================
class FactureListAPIView(generics.ListAPIView):
    """Liste toutes les factures"""
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer


class FactureDetailAPIView(generics.RetrieveAPIView):
    """Détail d'une facture"""
    queryset = Facture.objects.all()
    serializer_class = FactureSerializer


# ==================== COMMENTAIRES API ====================
class CommentaireListCreateAPIView(generics.ListCreateAPIView):
    """Liste et création de commentaires"""
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        voiture_id = self.request.query_params.get('voiture_id', None)
        if voiture_id:
            queryset = queryset.filter(voiture_id=voiture_id)
        return queryset


# ==================== ENTRETIENS API ====================
class EntretienListAPIView(generics.ListAPIView):
    """Liste tous les entretiens"""
    queryset = Entretien.objects.all()
    serializer_class = EntretienSerializer


# ==================== DOCUMENTS API ====================
class DocumentListAPIView(generics.ListAPIView):
    """Liste tous les documents"""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


# ==================== API STATUS ====================
@api_view(['GET'])
def api_status(request):
    """Endpoint pour vérifier le statut de l'API"""
    return Response({
        'status': 'OK',
        'message': 'API de location de voitures fonctionnelle',
        'version': '1.0.0'
    })
# ==================== API ROOT ====================
@api_view(['GET'])
def api_root(request):
    """Vue racine de l'API avec la liste de tous les endpoints"""
    return Response({
        'message': 'Bienvenue sur l\'API de location de voitures',
        'version': '1.0.0',
        'endpoints': {
            'status': request.build_absolute_uri('/api/status/'),
            'voitures': {
                'list': request.build_absolute_uri('/api/voitures/'),
                'disponibles': request.build_absolute_uri('/api/voitures/disponibles/'),
                'detail': request.build_absolute_uri('/api/voitures/{id}/')
            },
            'clients': {
                'list': request.build_absolute_uri('/api/clients/'),
                'detail': request.build_absolute_uri('/api/clients/{id}/')
            },
            'reservations': {
                'list': request.build_absolute_uri('/api/reservations/'),
                'create': request.build_absolute_uri('/api/reservations/create/'),
                'detail': request.build_absolute_uri('/api/reservations/{id}/'),
                'calculer_prix': request.build_absolute_uri('/api/reservations/calculer-prix/')
            },
            'chauffeurs': {
                'list': request.build_absolute_uri('/api/chauffeurs/'),
                'detail': request.build_absolute_uri('/api/chauffeurs/{id}/')
            },
            'factures': {
                'list': request.build_absolute_uri('/api/factures/'),
                'detail': request.build_absolute_uri('/api/factures/{id}/')
            },
            'commentaires': request.build_absolute_uri('/api/commentaires/'),
            'entretiens': request.build_absolute_uri('/api/entretiens/'),
            'documents': request.build_absolute_uri('/api/documents/')
        }
    })