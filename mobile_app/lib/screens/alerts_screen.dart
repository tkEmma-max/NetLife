// ÉCRAN ALERTES LIFENET
// Liste complète des alertes avec filtres et recherche

import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';
import 'package:mobile_app/widgets/alert_card.dart';

class AlertsScreen extends StatefulWidget {
  const AlertsScreen({super.key});

  @override
  State<AlertsScreen> createState() => _AlertsScreenState();
}

class _AlertsScreenState extends State<AlertsScreen> {
  String _selectedFilter = 'Tous';
  final List<String> _filters = ['Tous', 'Actives', 'Résolues', 'Rejetées'];

  // Données simulées (à remplacer par l'API)
  final List<Map<String, dynamic>> _mockAlerts = [
    {
      'type': 'Feu de brousse',
      'location': 'Bonamoussadi, Douala',
      'gravity': 'Critique',
      'time': 'Il y a 15 min',
      'status': 'en cours',
    },
    {
      'type': 'Inondation',
      'location': 'Maképé, Douala',
      'gravity': 'Élevé',
      'time': 'Il y a 2h',
      'status': 'en attente',
    },
    {
      'type': 'Déchet sauvage',
      'location': 'Quartier Bali, Douala',
      'gravity': 'Modéré',
      'time': 'Il y a 5h',
      'status': 'résolu',
    },
    {
      'type': 'Pollution eau',
      'location': 'Zone industrielle, Douala',
      'gravity': 'Élevé',
      'time': 'Il y a 1 jour',
      'status': 'en cours',
    },
    {
      'type': 'Feu de brousse',
      'location': 'Logbaba, Douala',
      'gravity': 'Faible',
      'time': 'Il y a 2 jours',
      'status': 'rejeté',
    },
  ];

  List<Map<String, dynamic>> get _filteredAlerts {
    if (_selectedFilter == 'Tous') {
      return _mockAlerts;
    }
    return _mockAlerts.where((alert) {
      final status = alert['status'] as String;
      switch (_selectedFilter) {
        case 'Actives':
          return status == 'en cours' || status == 'en attente';
        case 'Résolues':
          return status == 'résolu';
        case 'Rejetées':
          return status == 'rejeté';
        default:
          return true;
      }
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text(
          'Alertes',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.w600,
            color: AppColors.textPrimary,
          ),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.search, color: AppColors.textSecondary),
            onPressed: () {
              // TODO: Ouvrir la recherche
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // ----- FILTRES -----
          Container(
            color: Colors.white,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            child: Row(
              children: _filters.map((filter) {
                final isSelected = filter == _selectedFilter;
                return Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: FilterChip(
                    label: Text(
                      filter,
                      style: TextStyle(
                        fontSize: 13,
                        fontWeight: isSelected ? FontWeight.w600 : FontWeight.w400,
                        color: isSelected ? Colors.white : AppColors.textSecondary,
                      ),
                    ),
                    selected: isSelected,
                    onSelected: (_) {
                      setState(() {
                        _selectedFilter = filter;
                      });
                    },
                    backgroundColor: AppColors.background,
                    selectedColor: AppColors.primary,
                    checkmarkColor: Colors.white,
                    side: BorderSide.none,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                  ),
                );
              }).toList(),
            ),
          ),

          const Divider(height: 1, color: AppColors.textTertiary),

          // ----- LISTE DES ALERTES -----
          Expanded(
            child: _filteredAlerts.isEmpty
                ? Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.check_circle_outline,
                          size: 64,
                          color: AppColors.textTertiary.withOpacity(0.3),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Aucune alerte dans cette catégorie',
                          style: TextStyle(
                            fontSize: 16,
                            color: AppColors.textSecondary,
                          ),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: _filteredAlerts.length,
                    itemBuilder: (context, index) {
                      final alert = _filteredAlerts[index];
                      return Padding(
                        padding: const EdgeInsets.only(bottom: 12),
                        child: AlertCard(
                          type: alert['type']!,
                          location: alert['location']!,
                          gravity: alert['gravity']!,
                          time: alert['time']!,
                          status: alert['status']!,
                          onTap: () {
                            // TODO: Ouvrir la page de détail
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text('Détails de : ${alert['type']}'),
                                backgroundColor: AppColors.primary,
                              ),
                            );
                          },
                        ),
                      );
                    },
                  ),
          ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: AppColors.surface,
        selectedItemColor: AppColors.primary,
        unselectedItemColor: AppColors.textTertiary,
        currentIndex: 1,
        onTap: (index) {
          switch (index) {
            case 0:
              Navigator.pop(context);
              break;
            case 1:
              break;
            case 2:
              // TODO: Naviguer vers ReportScreen
              break;
            case 3:
              // TODO: Naviguer vers NotificationsScreen
              break;
            case 4:
              // TODO: Naviguer vers ProfileScreen
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
      ),
    );
  }
}