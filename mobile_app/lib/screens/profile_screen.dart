// ÉCRAN PROFIL LIFENET
// Gestion du compte utilisateur
import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';
import 'alerts_screen.dart';
import 'notifications_screen.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Données simulées (à remplacer par l'API)
    final String userName = 'Franck';
    final String userEmail = 'franck@email.com';
    final String userCity = 'Douala, Cameroun';
    final int reportCount = 12;
    final int resolvedCount = 8;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text(
          'Profil',
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
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            // ----- CARTE PROFIL -----
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(20),
                border: Border.all(
                  color: AppColors.textTertiary.withOpacity(0.1),
                  width: 1,
                ),
              ),
              child: Column(
                children: [
                  // Avatar
                  Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      color: AppColors.primary.withOpacity(0.15),
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: AppColors.primary.withOpacity(0.3),
                        width: 2,
                      ),
                    ),
                    child: Center(
                      child: Text(
                        userName.isNotEmpty ? userName[0].toUpperCase() : '?',
                        style: TextStyle(
                          fontSize: 32,
                          fontWeight: FontWeight.w600,
                          color: AppColors.primary,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    userName,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w600,
                      color: AppColors.textPrimary,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    userEmail,
                    style: const TextStyle(
                      fontSize: 14,
                      color: AppColors.textSecondary,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
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

            const SizedBox(height: 24),

            // ----- STATISTIQUES -----
            Row(
              children: [
                _buildStatItem('Signalements', reportCount.toString()),
                _buildStatItem('Résolus', resolvedCount.toString()),
                _buildStatItem('En cours', (reportCount - resolvedCount).toString()),
              ],
            ),

            const SizedBox(height: 24),

            // ----- MENU -----
            Container(
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: AppColors.textTertiary.withOpacity(0.1),
                  width: 1,
                ),
              ),
              child: Column(
                children: [
                  _buildMenuItem(
                    icon: Icons.history,
                    label: 'Historique des signalements',
                    onTap: () {
                      // TODO: Naviguer vers historique
                    },
                  ),
                  _buildDivider(),
                  _buildMenuItem(
                    icon: Icons.star_border,
                    label: 'Mes récompenses',
                    onTap: () {
                      // TODO: Naviguer vers récompenses
                    },
                  ),
                  _buildDivider(),
                  _buildMenuItem(
                    icon: Icons.settings_outlined,
                    label: 'Paramètres',
                    onTap: () {
                      // TODO: Naviguer vers paramètres
                    },
                  ),
                  _buildDivider(),
                  _buildMenuItem(
                    icon: Icons.help_outline,
                    label: 'Aide et support',
                    onTap: () {
                      // TODO: Naviguer vers aide
                    },
                  ),
                  _buildDivider(),
                  _buildMenuItem(
                    icon: Icons.logout,
                    label: 'Déconnexion',
                    color: AppColors.danger,
                    onTap: () {
                      _showLogoutDialog(context);
                    },
                  ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // ----- VERSION -----
            Center(
              child: Text(
                'LifeNet v1.0.0',
                style: TextStyle(
                  fontSize: 12,
                  color: AppColors.textTertiary,
                ),
              ),
            ),
          ],
        ),
      ),
     bottomNavigationBar: BottomNavigationBar(
       type: BottomNavigationBarType.fixed,
       backgroundColor: AppColors.surface,
       selectedItemColor: AppColors.primary,
       unselectedItemColor: AppColors.textTertiary,
       currentIndex: 4,
       onTap: (index) {
         switch (index) {
           case 0:
             Navigator.pop(context);
             break;
           case 1:
             Navigator.push(
               context,
               MaterialPageRoute(builder: (_) => const AlertsScreen()),
             );
             break;
           case 2:
             // TODO: ReportScreen
             break;
           case 3:
             Navigator.push(
               context,
               MaterialPageRoute(builder: (_) => const NotificationsScreen()),
             );
             break;
           case 4:
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

  Widget _buildStatItem(String label, String value) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: AppColors.textTertiary.withOpacity(0.1),
            width: 1,
          ),
        ),
        child: Column(
          children: [
            Text(
              value,
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.w700,
                color: AppColors.textPrimary,
              ),
            ),
            Text(
              label,
              style: const TextStyle(
                fontSize: 12,
                color: AppColors.textSecondary,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMenuItem({
    required IconData icon,
    required String label,
    required VoidCallback onTap,
    Color? color,
  }) {
    return ListTile(
      leading: Icon(
        icon,
        color: color ?? AppColors.textSecondary,
        size: 22,
      ),
      title: Text(
        label,
        style: TextStyle(
          fontSize: 15,
          color: color ?? AppColors.textPrimary,
        ),
      ),
      trailing: Icon(
        Icons.chevron_right,
        color: AppColors.textTertiary,
        size: 20,
      ),
      onTap: onTap,
      contentPadding: const EdgeInsets.symmetric(horizontal: 16),
    );
  }

  Widget _buildDivider() {
    return Divider(
      height: 1,
      color: AppColors.textTertiary.withOpacity(0.1),
    );
  }

  void _showLogoutDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
        title: const Text('Déconnexion'),
        content: const Text('Voulez-vous vraiment vous déconnecter ?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Annuler'),
          ),
          ElevatedButton(
            onPressed: () {
              // TODO: Appeler API logout
              Navigator.pushReplacementNamed(context, '/login');
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.danger,
            ),
            child: const Text('Se déconnecter'),
          ),
        ],
      ),
    );
  }
}