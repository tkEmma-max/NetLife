import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';
import 'package:mobile_app/widgets/avatar_widget.dart';
import 'package:mobile_app/widgets/statistic_card.dart';
import 'package:mobile_app/widgets/alert_card.dart';
import 'package:mobile_app/widgets/incident_map.dart';
import 'package:mobile_app/screens/report_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // Données simulées (à remplacer par l'API plus tard)
  final String userName = 'Franck';
  final String userCity = 'Douala, Cameroun';
  final int notificationCount = 2;

  final List<Map<String, dynamic>> mockAlerts = [
    {
      'type': 'Feu de brousse',
      'location': 'Quartier Bonamoussadi',
      'gravity': 'Critique',
      'time': 'Il y a 15 min',
      'status': 'en cours',
      'lat': 4.0583,
      'lon': 9.7591,
    },
    {
      'type': 'Inondation',
      'location': 'Zone de Maképé',
      'gravity': 'Élevé',
      'time': 'Il y a 2h',
      'status': 'en attente',
      'lat': 4.0452,
      'lon': 9.7678,
    },
  ];

  final List<Map<String, dynamic>> mockIncidents = [
    {'type': 'Feu', 'gravity': 5, 'lat': 4.0583, 'lon': 9.7591},
    {'type': 'Inondation', 'gravity': 4, 'lat': 4.0452, 'lon': 9.7678},
    {'type': 'Déchet', 'gravity': 2, 'lat': 4.0621, 'lon': 9.7715},
    {'type': 'Feu', 'gravity': 3, 'lat': 4.0389, 'lon': 9.7557},
  ];

  int _selectedIndex = 0;

  void _onNavTap(int index) {
    setState(() {
      _selectedIndex = index;
    });
    if (index == 2) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => const ReportScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // ============================================
              // 1. HEADER
              // ============================================
              Row(
                children: [
                  AvatarWidget(name: userName, size: 44),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Bonjour, $userName 👋',
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
                              userCity,
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
                        onPressed: () {},
                      ),
                      if (notificationCount > 0)
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
                                notificationCount > 9 ? '9+' : '$notificationCount',
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
              // 2. CARTES STATISTIQUES (Alertes + Interventions)
              // ============================================
              Row(
                children: [
                  StatisticCard(
                    label: 'Alertes à proximité',
                    value: '2',
                    icon: Icons.warning_amber_rounded,
                    iconColor: AppColors.danger,
                  ),
                  const SizedBox(width: 12),
                  StatisticCard(
                    label: 'Interventions en cours',
                    value: '1',
                    icon: Icons.construction,
                    iconColor: AppColors.warning,
                  ),
                ],
              ),

              const SizedBox(height: 20),

              // ============================================
              // 3. BOUTON PRINCIPAL : SIGNALER UN DANGER
              // ============================================
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => const ReportScreen()),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.danger,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(16),
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
                    onPressed: () {},
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
              ...mockAlerts.map((alert) => Padding(
                    padding: const EdgeInsets.only(bottom: 10),
                    child: AlertCard(
                      type: alert['type']!,
                      location: alert['location']!,
                      gravity: alert['gravity']!,
                      time: alert['time']!,
                      status: alert['status']!,
                      onTap: () {},
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
                incidents: mockIncidents,
                height: 200,
                latitude: 4.0511,
                longitude: 9.7679,
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
                    color: AppColors.textTertiary.withOpacity(0.1),
                    width: 1,
                  ),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: [
                    _buildImpactItem('56', 'Signalements'),
                    _buildImpactItem('12', 'Résolus'),
                    _buildImpactItem('2', 'Actives'),
                    _buildImpactItem('340', 'Citoyens'),
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
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: AppColors.textTertiary.withOpacity(0.1),
                    width: 1,
                  ),
                ),
                child: Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(10),
                      decoration: BoxDecoration(
                        color: AppColors.warning.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.local_fire_department,
                        color: AppColors.warning,
                        size: 22,
                      ),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Feu de brousse signalé',
                            style: TextStyle(
                              fontWeight: FontWeight.w600,
                              color: AppColors.textPrimary,
                            ),
                          ),
                          const SizedBox(height: 2),
                          Text(
                            'Statut : En cours • Il y a 15 min',
                            style: const TextStyle(
                              fontSize: 13,
                              color: AppColors.textSecondary,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 28),

              // ============================================
              // 8. CONSEIL DE PRÉVENTION
              // ============================================
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.primary.withOpacity(0.06),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(
                    color: AppColors.primary.withOpacity(0.12),
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
                        'Conseil du jour : En cas de feu de brousse, alertez les autorités et éloignez-vous de la zone.',
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

      // ============================================
      // 9. BARRE DE NAVIGATION INFÉRIEURE
      // ============================================
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: AppColors.surface,
        selectedItemColor: AppColors.primary,
        unselectedItemColor: AppColors.textTertiary,
        currentIndex: _selectedIndex,
        onTap: _onNavTap,
        elevation: 2,
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
      ),
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
}