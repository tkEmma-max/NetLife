// ÉCRAN NOTIFICATIONS LIFENET
// Historique des notifications reçues

import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';
import 'alerts_screen.dart';
import 'report_screen.dart';

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({super.key});

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  // Données simulées (à remplacer par l'API)
  final List<Map<String, dynamic>> _mockNotifications = [
    {
      'title': 'Alerte Feu de brousse',
      'body': 'Un feu a été signalé à Bonamoussadi. Équipe d\'intervention en route.',
      'time': 'Il y a 15 min',
      'isRead': false,
      'type': 'alerte',
    },
    {
      'title': 'Signalement pris en charge',
      'body': 'Votre signalement de déchet sauvage à Bali a été pris en charge.',
      'time': 'Il y a 2h',
      'isRead': false,
      'type': 'update',
    },
    {
      'title': 'Intervention terminée',
      'body': 'Le feu de brousse à Logbaba est éteint. Zone sécurisée.',
      'time': 'Il y a 5h',
      'isRead': true,
      'type': 'update',
    },
    {
      'title': 'Bienvenue sur LifeNet !',
      'body': 'Merci de rejoindre la communauté. Signalez les dangers autour de vous.',
      'time': 'Il y a 2 jours',
      'isRead': true,
      'type': 'info',
    },
  ];

  int get _unreadCount {
    return _mockNotifications.where((n) => n['isRead'] == false).length;
  }

  // Navigation vers les autres écrans
  void _navigateToAlerts() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => const AlertsScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Row(
          children: [
            const Text(
              'Notifications',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.w600,
                color: AppColors.textPrimary,
              ),
            ),
            const SizedBox(width: 10),
            if (_unreadCount > 0)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                decoration: BoxDecoration(
                  color: AppColors.danger,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  _unreadCount.toString(),
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
          ],
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          TextButton(
            onPressed: () {
              setState(() {
                for (var notification in _mockNotifications) {
                  notification['isRead'] = true;
                }
              });
            },
            child: const Text(
              'Tout marquer lu',
              style: TextStyle(
                fontSize: 13,
                color: AppColors.primary,
              ),
            ),
          ),
        ],
      ),
      body: _mockNotifications.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.notifications_off_outlined,
                    size: 64,
                    color: AppColors.textTertiary.withOpacity(0.3),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Aucune notification',
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
              itemCount: _mockNotifications.length,
              itemBuilder: (context, index) {
                final notification = _mockNotifications[index];
                final isRead = notification['isRead'] as bool;

                return Padding(
                  padding: const EdgeInsets.only(bottom: 10),
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: isRead ? AppColors.surface : AppColors.primary.withOpacity(0.05),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: isRead
                            ? AppColors.textTertiary.withOpacity(0.1)
                            : AppColors.primary.withOpacity(0.2),
                        width: 1,
                      ),
                    ),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Icône selon le type
                        Container(
                          padding: const EdgeInsets.all(8),
                          decoration: BoxDecoration(
                            color: _getTypeColor(notification['type'] as String)
                                .withOpacity(0.12),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Icon(
                            _getTypeIcon(notification['type'] as String),
                            color: _getTypeColor(notification['type'] as String),
                            size: 20,
                          ),
                        ),
                        const SizedBox(width: 14),
                        // Contenu
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                notification['title'] as String,
                                style: TextStyle(
                                  fontSize: 15,
                                  fontWeight: isRead ? FontWeight.w500 : FontWeight.w600,
                                  color: AppColors.textPrimary,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                notification['body'] as String,
                                style: TextStyle(
                                  fontSize: 14,
                                  color: AppColors.textSecondary,
                                ),
                              ),
                              const SizedBox(height: 6),
                              Row(
                                children: [
                                  const Icon(
                                    Icons.access_time,
                                    size: 14,
                                    color: AppColors.textTertiary,
                                  ),
                                  const SizedBox(width: 4),
                                  Text(
                                    notification['time'] as String,
                                    style: const TextStyle(
                                      fontSize: 12,
                                      color: AppColors.textTertiary,
                                    ),
                                  ),
                                ],
                              ),
                            ],
                          ),
                        ),
                        // Point non lu
                        if (!isRead)
                          Container(
                            width: 10,
                            height: 10,
                            decoration: const BoxDecoration(
                              color: AppColors.primary,
                              shape: BoxShape.circle,
                            ),
                          ),
                      ],
                    ),
                  ),
                );
              },
            ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        backgroundColor: AppColors.surface,
        selectedItemColor: AppColors.primary,
        unselectedItemColor: AppColors.textTertiary,
        currentIndex: 3,
        onTap: (index) {
          switch (index) {
            case 0:
              Navigator.pop(context);
              break;
            case 1:
              _navigateToAlerts();
              break;
            case 2:
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const ReportScreen()),
              );
              break;
            case 3:
              break;
            case 4:
              // TODO: ProfileScreen
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

  IconData _getTypeIcon(String type) {
    switch (type) {
      case 'alerte':
        return Icons.warning_amber_rounded;
      case 'update':
        return Icons.sync_alt;
      case 'info':
        return Icons.info_outline;
      default:
        return Icons.notifications_outlined;
    }
  }

  Color _getTypeColor(String type) {
    switch (type) {
      case 'alerte':
        return AppColors.danger;
      case 'update':
        return AppColors.warning;
      case 'info':
        return AppColors.info;
      default:
        return AppColors.textSecondary;
    }
  }
}