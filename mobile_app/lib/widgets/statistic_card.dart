// WIDGET STATISTIQUE DYNAMIQUE
// Affiche des chiffres (alertes, interventions, etc.)
// Les valeurs viennent des paramètres (dynamiques)

import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';

class StatisticCard extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color? iconColor;

  const StatisticCard({
    super.key,
    required this.label,
    required this.value,
    required this.icon,
    this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: AppColors.textTertiary.withOpacity(0.15),
            width: 1,
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  icon,
                  size: 18,
                  color: iconColor ?? AppColors.primary,
                ),
                const SizedBox(width: 8),
                Text(
                  value,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w700,
                    color: AppColors.textPrimary,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 4),
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
}