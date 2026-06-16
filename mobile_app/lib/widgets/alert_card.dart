// WIDGET ALERTE À PROXIMITÉ
// Affiche une alerte avec type, lieu, gravité, heure

import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';

class AlertCard extends StatelessWidget {
  final String type;
  final String location;
  final String gravity;
  final String time;
  final String status;
  final VoidCallback onTap;

  const AlertCard({
    super.key,
    required this.type,
    required this.location,
    required this.gravity,
    required this.time,
    required this.status,
    required this.onTap,
  });

  Color _getGravityColor() {
    switch (gravity.toLowerCase()) {
      case 'critique':
        return AppColors.danger;
      case 'élevé':
        return AppColors.warning;
      case 'modéré':
        return AppColors.info;
      case 'faible':
        return AppColors.success;
      default:
        return AppColors.textSecondary;
    }
  }

  IconData _getTypeIcon() {
    switch (type.toLowerCase()) {
      case 'feu':
      case 'feu de brousse':
        return Icons.local_fire_department;
      case 'inondation':
        return Icons.water_drop;
      case 'déchet':
      case 'déchet sauvage':
        return Icons.delete_outline;
      case 'pollution':
        return Icons.warning_amber_outlined;
      default:
        return Icons.error_outline;
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
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
            // Icône du type
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: _getGravityColor().withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                _getTypeIcon(),
                color: _getGravityColor(),
                size: 24,
              ),
            ),
            const SizedBox(width: 16),
            // Informations
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Text(
                        type,
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 2,
                        ),
                        decoration: BoxDecoration(
                          color: _getGravityColor().withOpacity(0.15),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          gravity,
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w600,
                            color: _getGravityColor(),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text(
                    location,
                    style: const TextStyle(
                      fontSize: 14,
                      color: AppColors.textSecondary,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Row(
                    children: [
                      const Icon(
                        Icons.access_time,
                        size: 14,
                        color: AppColors.textTertiary,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        time,
                        style: const TextStyle(
                          fontSize: 12,
                          color: AppColors.textTertiary,
                        ),
                      ),
                      const SizedBox(width: 12),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 2,
                        ),
                        decoration: BoxDecoration(
                          color: status == 'en cours'
                              ? AppColors.warning.withOpacity(0.15)
                              : AppColors.success.withOpacity(0.15),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          status,
                          style: TextStyle(
                            fontSize: 10,
                            fontWeight: FontWeight.w500,
                            color: status == 'en cours'
                                ? AppColors.warning
                                : AppColors.success,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
            // Flèche "Voir plus"
            Icon(
              Icons.chevron_right,
              color: AppColors.textTertiary,
            ),
          ],
        ),
      ),
    );
  }
}