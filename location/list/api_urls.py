from django.urls import path
from .api_views import (
    # Voitures
    VoitureListAPIView,
    VoitureDetailAPIView,
    voitures_disponibles,

    # Clients
    ClientListCreateAPIView,
    ClientDetailAPIView,

    # Réservations
    ReservationListAPIView,
    ReservationCreateAPIView,
    ReservationDetailAPIView,
    calculer_prix_reservation,

    # Chauffeurs
    ChauffeurListAPIView,
    ChauffeurDetailAPIView,

    # Factures
    FactureListAPIView,
    FactureDetailAPIView,

    # Commentaires
    CommentaireListCreateAPIView,

    # Entretiens
    EntretienListAPIView,

    # Documents
    DocumentListAPIView,

    # Status
    api_status,
)

# URLs de l'API
urlpatterns = [
    # Status de l'API
    path('status/', api_status, name='api_status'),

    # Voitures
    path('voitures/', VoitureListAPIView.as_view(), name='voitures_list'),
    path('voitures/disponibles/', voitures_disponibles, name='voitures_disponibles'),
    path('voitures/<str:lookup_field>/', VoitureDetailAPIView.as_view(), name='voiture_detail'),

    # Clients
    path('clients/', ClientListCreateAPIView.as_view(), name='clients_list_create'),
    path('clients/<int:pk>/', ClientDetailAPIView.as_view(), name='client_detail'),

    # Réservations
    path('reservations/', ReservationListAPIView.as_view(), name='reservations_list'),
    path('reservations/create/', ReservationCreateAPIView.as_view(), name='reservation_create'),
    path('reservations/<int:pk>/', ReservationDetailAPIView.as_view(), name='reservation_detail'),
    path('reservations/calculer-prix/', calculer_prix_reservation, name='calculer_prix'),

    # Chauffeurs
    path('chauffeurs/', ChauffeurListAPIView.as_view(), name='chauffeurs_list'),
    path('chauffeurs/<int:pk>/', ChauffeurDetailAPIView.as_view(), name='chauffeur_detail'),

    # Factures
    path('factures/', FactureListAPIView.as_view(), name='factures_list'),
    path('factures/<int:pk>/', FactureDetailAPIView.as_view(), name='facture_detail'),

    # Commentaires
    path('commentaires/', CommentaireListCreateAPIView.as_view(), name='commentaires_list_create'),

    # Entretiens
    path('entretiens/', EntretienListAPIView.as_view(), name='entretiens_list'),

    # Documents
    path('documents/', DocumentListAPIView.as_view(), name='documents_list'),
]
from django.urls import path
from .api_views import (
    # Voitures
    VoitureListAPIView,
    VoitureDetailAPIView,
    voitures_disponibles,

    # Clients
    ClientListCreateAPIView,
    ClientDetailAPIView,

    # Réservations
    ReservationListAPIView,
    ReservationCreateAPIView,
    ReservationDetailAPIView,
    calculer_prix_reservation,

    # Chauffeurs
    ChauffeurListAPIView,
    ChauffeurDetailAPIView,

    # Factures
    FactureListAPIView,
    FactureDetailAPIView,

    # Commentaires
    CommentaireListCreateAPIView,

    # Entretiens
    EntretienListAPIView,

    # Documents
    DocumentListAPIView,

    # Status
    api_status,

    # Root  ← Ajoutez cette ligne
    api_root,
)

# URLs de l'API
urlpatterns = [
    # Root de l'API  ← Ajoutez cette ligne EN PREMIER
    path('', api_root, name='api_root'),

    # Status de l'API
    path('status/', api_status, name='api_status'),

    # ... toutes vos autres URLs restent identiques
]