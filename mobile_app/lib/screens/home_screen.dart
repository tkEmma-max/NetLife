// ÉCRAN ACCUEIL LIFENET
// Version complète avec données réelles du backend

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:mobile_app/config/app_colors.dart';
import 'package:mobile_app/services/api_service.dart';
import 'package:mobile_app/services/location_service.dart';
import 'package:mobile_app/widgets/avatar_widget.dart';
import 'package:mobile_app/widgets/alert_card.dart';
import 'package:mobile_app/widgets/incident_map.dart';
import 'package:mobile_app/widgets/statistic_card.dart';
import 'package:mobile_app/screens/report_screen.dart';
import 'package:mobile_app/screens/alerts_screen.dart';
import 'package:mobile_app/screens/notifications_screen.dart';
import 'package:mobile_app/screens/profile_screen.dart';
import 'package:geolocator/geolocator.dart';
import 'package:mobile_app/services/geocoding_service.dart';
import 'package:mobile_app/screens/alert_detail_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final ApiService _apiService = ApiService();
  // LocationService n'a pas besoin d'être instancié (méthodes statiques)

  // Données
  Map<String, dynamic> _userProfile = {};
  List<dynamic> _nearbyAlerts = [];
  List<dynamic> _activeInterventions = [];
  List<dynamic> _myReports = [];
  Map<String, dynamic> _dashboardStats = {};
  int _unreadNotifications = 0;
  Position? _currentPosition;

  bool _isLoading = true;
  String _userAddress = '';

  @override
  void initState() {
    super.initState();
    _loadAllData();
  }

  Future<void> _loadAllData() async {
    setState(() => _isLoading = true);

    try {
      // 1. Charger la position
      _currentPosition = await LocationService.getCurrentLocation();

      // 1.5 Convertir la position en adresse
      if (_currentPosition != null) {
        try {
          _userAddress = await GeocodingService.getAddressFromCoordinates(
            _currentPosition!.latitude,
            _currentPosition!.longitude,
          );
        } catch (e) {
          print('Erreur de geocodage: $e');
          _userAddress = 'Position non disponible';
        }
      }

      // 2. Charger le profil utilisateur
      _userProfile = await _apiService.getProfile();

      // 3. Charger les alertes à proximité
      if (_currentPosition != null) {
        _nearbyAlerts = await _apiService.getNearbyAlerts(
          latitude: _currentPosition!.latitude,
          longitude: _currentPosition!.longitude,
          radius: 10,
        );
      }

      // 4. Charger les interventions actives
      _activeInterventions = await _apiService.getActiveInterventions();

      // 5. Charger les statistiques
      _dashboardStats = await _apiService.getDashboardStats();

      // 6. Charger les signalements de l'utilisateur
      _myReports = await _apiService.getMyReports();

      // 7. Charger le nombre de notifications non lues
      _unreadNotifications = await _apiService.getUnreadNotificationCount();

    } catch (e) {
      print('Erreur de chargement: $e');
    }

    setState(() => _isLoading = false);
  }

  Future<void> _refreshData() async {
    await _loadAllData();
  }

  String _getGreeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return 'Bonjour';
    if (hour < 18) return 'Bon après-midi';
    return 'Bonsoir';
  }

  String _getUserName() {
    return _userProfile['username'] ?? 'Citoyen';
  }

  String _getUserCity() {
    // 1. Priorité à la position GPS convertie en adresse
    if (_userAddress.isNotEmpty && _userAddress != 'Position non disponible') {
      return _userAddress;
    }
    // 2. Sinon, on utilise la ville du profil (si disponible)
    if (_userProfile['city'] != null && _userProfile['city'].isNotEmpty) {
      return _userProfile['city'];
    }
    // 3. Fallback
    return 'Cameroun';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: RefreshIndicator(
          onRefresh: _refreshData,
          child: _isLoading
              ? const Center(
                  child: CircularProgressIndicator(
                    color: AppColors.primary,
                  ),
                )
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(20),
                  physics: const AlwaysScrollableScrollPhysics(),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // ============================================
                      // 1. HEADER
                      // ============================================
                      Row(
                        children: [
                          AvatarWidget(
                            name: _getUserName(),
                            size: 44,
                          ),
                          const SizedBox(width: 14),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  '${_getGreeting()}, ${_getUserName()} 👋',
                                  style: const TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.w600,
                                    color: AppColors.textPrimary,
                                  ),
                                ),
                                const SizedBox(height: 2),
                                Row(
                                  children: [
                                    const Icon(
                                      Icons.location_on,
                                      size: 14,
                                      color: AppColors.textSecondary,
                                    ),
                                    const SizedBox(width: 4),
                                    Text(
                                      _getUserCity(),
                                      style: const TextStyle(
                                        fontSize: 13,
                                        color: AppColors.textSecondary,
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                          Stack(
                            clipBehavior: Clip.none,
                            children: [
                              IconButton(
                                icon: const Icon(
                                  Icons.notifications_outlined,
                                  color: AppColors.textSecondary,
                                  size: 26,
                                ),
                                onPressed: () {
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (_) => const NotificationsScreen(),
                                    ),
                                  );
                                },
                              ),
                              if (_unreadNotifications > 0)
                                Positioned(
                                  right: 6,
                                  top: 4,
                                  child: Container(
                                    padding: const EdgeInsets.all(4),
                                    decoration: const BoxDecoration(
                                      color: AppColors.danger,
                                      shape: BoxShape.circle,
                                    ),
                                    constraints: const BoxConstraints(
                                      minWidth: 18,
                                      minHeight: 18,
                                    ),
                                    child: Center(
                                      child: Text(
                                        _unreadNotifications > 9
                                            ? '9+'
                                            : '$_unreadNotifications',
                                        style: const TextStyle(
                                          color: Colors.white,
                                          fontSize: 9,
                                          fontWeight: FontWeight.bold,
                                        ),
                                      ),
                                    ),
                                  ),
                                ),
                            ],
                          ),
                        ],
                      ),

                      const SizedBox(height: 24),

                      // ============================================
                      // 2. CARTES STATISTIQUES
                      // ============================================
                      Row(
                        children: [
                          StatisticCard(
                            label: 'Alertes à proximité',
                            value: '${_nearbyAlerts.length}',
                            icon: Icons.warning_amber_rounded,
                            iconColor: AppColors.danger,
                          ),
                          const SizedBox(width: 12),
                          StatisticCard(
                            label: 'Interventions en cours',
                            value: '${_activeInterventions.length}',
                            icon: Icons.construction,
                            iconColor: AppColors.warning,
                          ),
                        ],
                      ),

                      const SizedBox(height: 20),

                      // ============================================
                      // 3. BOUTON SIGNALEMENT
                      // ============================================
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => const ReportScreen(),
                              ),
                            );
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.danger,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(vertical: 16),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                            elevation: 0,
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: const [
                              Icon(Icons.add_circle_outline, size: 22),
                              SizedBox(width: 10),
                              Text(
                                'Signaler un danger',
                                style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w600,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),

                      const SizedBox(height: 28),

                      // ============================================
                      // 4. ALERTES À PROXIMITÉ
                      // ============================================
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text(
                            'Alertes à proximité',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w600,
                              color: AppColors.textPrimary,
                            ),
                          ),
                          TextButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (_) => const AlertsScreen(),
                                ),
                              );
                            },
                            child: const Text(
                              'Voir plus',
                              style: TextStyle(
                                fontSize: 14,
                                fontWeight: FontWeight.w500,
                                color: AppColors.primary,
                              ),
                            ),
                          ),
                        ],
                      ),

                      const SizedBox(height: 12),

                      // Liste des alertes
                      if (_nearbyAlerts.isEmpty)
                        const Center(
                          child: Padding(
                            padding: EdgeInsets.symmetric(vertical: 20),
                            child: Text(
                              'Aucune alerte à proximité',
                              style: TextStyle(
                                fontSize: 14,
                                color: AppColors.textSecondary,
                              ),
                            ),
                          ),
                        )
                      else
                        ..._nearbyAlerts.take(3).map((alert) => Padding(
                              padding: const EdgeInsets.only(bottom: 10),
                              child: AlertCard(
                                type: alert['danger_type_display'] ?? 'Danger',
                                location: alert['address'] ?? 'Localisation inconnue',
                                gravity: alert['priority'] ?? 'Modéré',
                                time: _formatTime(alert['created_at']),
                                status: alert['status']?.toLowerCase() ?? 'en cours',
                                onTap: () {
                                  // TODO: Détails de l'alerte
                                },
                              ),
                            )),

                      const SizedBox(height: 24),

                      // ============================================
                      // 5. CARTE INTERACTIVE
                      // ============================================
                      const Text(
                        'Carte des incidents',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 12),
                      IncidentMap(
                        incidents: _nearbyAlerts.map((alert) {
                          final lat = double.tryParse(alert['latitude']?.toString() ?? '') ?? 4.0511;
                          final lon = double.tryParse(alert['longitude']?.toString() ?? '') ?? 9.7679;

                          int gravity = 3;
                          final priority = alert['priority']?.toString().toUpperCase() ?? '';
                          if (priority == 'CRITICAL') gravity = 5;
                          else if (priority == 'HIGH') gravity = 4;
                          else if (priority == 'MEDIUM') gravity = 3;
                          else if (priority == 'LOW') gravity = 2;

                          return {
                            'id': alert['id'] ?? 0,
                            'lat': lat,
                            'lon': lon,
                            'type': alert['danger_type'] ?? 'other',
                            'gravity': gravity,
                            'title': alert['title'] ?? '',
                            'address': alert['address'] ?? '',
                          };
                        }).toList(),
                        height: 350,
                        latitude: _currentPosition?.latitude,
                        longitude: _currentPosition?.longitude,
                        onMarkerTap: (alertId) {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => AlertDetailScreen(alertId: alertId),
                            ),
                          );
                        },
                      ),
                      const SizedBox(height: 28),

                      // ============================================
                      // 6. IMPACT COMMUNAUTAIRE
                      // ============================================
                      const Text(
                        'Impact communautaire',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: AppColors.surface,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: AppColors.border.withOpacity(0.1),
                            width: 1,
                          ),
                        ),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            _buildImpactItem(
                              _dashboardStats['total_reports']?.toString() ?? '0',
                              'Signalements',
                            ),
                            _buildImpactItem(
                              _dashboardStats['resolved_incidents']?.toString() ?? '0',
                              'Résolus',
                            ),
                            _buildImpactItem(
                              _dashboardStats['active_alerts']?.toString() ?? '0',
                              'Actives',
                            ),
                            _buildImpactItem(
                              _dashboardStats['total_citizens']?.toString() ?? '0',
                              'Citoyens',
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 28),

                      // ============================================
                      // 7. ACTIVITÉ RÉCENTE
                      // ============================================
                      const Text(
                        'Activité récente',
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 12),

                      if (_myReports.isEmpty)
                        const Center(
                          child: Padding(
                            padding: EdgeInsets.symmetric(vertical: 20),
                            child: Text(
                              'Aucune activité récente',
                              style: TextStyle(
                                fontSize: 14,
                                color: AppColors.textSecondary,
                              ),
                            ),
                          ),
                        )
                      else
                        ..._myReports.take(2).map((report) => Padding(
                              padding: const EdgeInsets.only(bottom: 10),
                              child: Container(
                                padding: const EdgeInsets.all(16),
                                decoration: BoxDecoration(
                                  color: AppColors.surface,
                                  borderRadius: BorderRadius.circular(16),
                                  border: Border.all(
                                    color: AppColors.border.withOpacity(0.1),
                                    width: 1,
                                  ),
                                ),
                                child: Row(
                                  children: [
                                    Container(
                                      padding: const EdgeInsets.all(10),
                                      decoration: BoxDecoration(
                                        color: _getStatusColor(report['status'])
                                            .withOpacity(0.12),
                                        borderRadius: BorderRadius.circular(12),
                                      ),
                                      child: Icon(
                                        _getStatusIcon(report['status']),
                                        color: _getStatusColor(report['status']),
                                        size: 22,
                                      ),
                                    ),
                                    const SizedBox(width: 14),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment:
                                            CrossAxisAlignment.start,
                                        children: [
                                          Text(
                                            report['title'] ?? 'Signalement',
                                            style: const TextStyle(
                                              fontWeight: FontWeight.w600,
                                              color: AppColors.textPrimary,
                                            ),
                                          ),
                                          const SizedBox(height: 2),
                                          Text(
                                            'Statut : ${report['status'] ?? 'En attente'}',
                                            style: const TextStyle(
                                              fontSize: 13,
                                              color: AppColors.textSecondary,
                                            ),
                                          ),
                                          const SizedBox(height: 2),
                                          Text(
                                            _formatTime(report['created_at']),
                                            style: const TextStyle(
                                              fontSize: 12,
                                              color: AppColors.textTertiary,
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            )),

                      const SizedBox(height: 28),

                      // ============================================
                      // 8. CONSEIL DE PRÉVENTION
                      // ============================================
                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: AppColors.primaryLight.withOpacity(0.3),
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: AppColors.primary.withOpacity(0.2),
                            width: 1,
                          ),
                        ),
                        child: Row(
                          children: [
                            const Icon(
                              Icons.lightbulb_outline,
                              color: AppColors.primary,
                              size: 24,
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              child: Text(
                                _getDailyTip(),
                                style: TextStyle(
                                  fontSize: 14,
                                  color: AppColors.textPrimary.withOpacity(0.85),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),

                      const SizedBox(height: 80),
                    ],
                  ),
                ),
        ),
      ),
      bottomNavigationBar: _buildBottomNav(),
    );
  }

  Widget _buildBottomNav() {
    return BottomNavigationBar(
      type: BottomNavigationBarType.fixed,
      backgroundColor: AppColors.surface,
      selectedItemColor: AppColors.primary,
      unselectedItemColor: AppColors.textTertiary,
      currentIndex: 0,
      onTap: (index) {
        switch (index) {
          case 0:
            break;
          case 1:
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const AlertsScreen()),
            );
            break;
          case 2:
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ReportScreen()),
            );
            break;
          case 3:
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const NotificationsScreen()),
            );
            break;
          case 4:
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ProfileScreen()),
            );
            break;
        }
      },
      items: const [
        BottomNavigationBarItem(
          icon: Icon(Icons.home_outlined),
          activeIcon: Icon(Icons.home),
          label: 'Accueil',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.warning_amber_outlined),
          activeIcon: Icon(Icons.warning_amber),
          label: 'Alertes',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.add_circle_outline, size: 32),
          activeIcon: Icon(Icons.add_circle, size: 32),
          label: 'Signaler',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.notifications_outlined),
          activeIcon: Icon(Icons.notifications),
          label: 'Notif.',
        ),
        BottomNavigationBarItem(
          icon: Icon(Icons.person_outline),
          activeIcon: Icon(Icons.person),
          label: 'Profil',
        ),
      ],
    );
  }

  Widget _buildImpactItem(String value, String label) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.w700,
            color: AppColors.textPrimary,
          ),
        ),
        const SizedBox(height: 2),
        Text(
          label,
          style: const TextStyle(
            fontSize: 11,
            color: AppColors.textSecondary,
          ),
        ),
      ],
    );
  }

  String _formatTime(String? isoString) {
    if (isoString == null) return 'Récent';
    try {
      final date = DateTime.parse(isoString);
      final now = DateTime.now();
      final difference = now.difference(date);

      if (difference.inMinutes < 1) return 'À l\'instant';
      if (difference.inMinutes < 60) {
        return 'Il y a ${difference.inMinutes} min';
      }
      if (difference.inHours < 24) {
        return 'Il y a ${difference.inHours}h';
      }
      if (difference.inDays < 7) {
        return 'Il y a ${difference.inDays}j';
      }
      return DateFormat('dd/MM/yyyy').format(date);
    } catch (e) {
      return 'Récent';
    }
  }

  String _getDailyTip() {
    final tips = [
      'En cas de feu de brousse, alertez les autorités et éloignez-vous de la zone.',
      'Les déchets sauvages polluent nos rivières. Signalez-les pour un nettoyage rapide.',
      'Une simple photo peut sauver des vies. Signalez tout danger autour de vous.',
      'La prévention commence par la vigilance. Restez attentif à votre environnement.',
      'Partagez LifeNet avec vos voisins. Plus nous sommes nombreux, plus nous sommes forts.',
    ];
    final index = DateTime.now().day % tips.length;
    return tips[index];
  }

  Color _getStatusColor(String? status) {
    switch (status?.toLowerCase()) {
      case 'resolved':
        return AppColors.success;
      case 'in_progress':
        return AppColors.warning;
      case 'rejected':
        return AppColors.error;
      default:
        return AppColors.primary;
    }
  }

  IconData _getStatusIcon(String? status) {
    switch (status?.toLowerCase()) {
      case 'resolved':
        return Icons.check_circle;
      case 'in_progress':
        return Icons.sync_alt;
      case 'rejected':
        return Icons.cancel;
      default:
        return Icons.pending;
    }
  }
}