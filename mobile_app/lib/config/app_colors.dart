import 'package:flutter/material.dart';

class AppColors {
  // Couleurs principales (Orange = urgence, Vert = environnement)
  static const Color primary = Color(0xFFF97316);      // Orange vif
  static const Color primaryDark = Color(0xFFEA580C);   // Orange foncé
  static const Color secondary = Color(0xFF22C55E);     // Vert alerte
  static const Color secondaryLight = Color(0xFFDCFCE7); // Vert clair

  // Neutres
  static const Color background = Color(0xFFF8FAFC);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color cardBackground = Color(0xFFFFFFFF);

  // Textes
  static const Color textPrimary = Color(0xFF1E293B);
  static const Color textSecondary = Color(0xFF64748B);
  static const Color textTertiary = Color(0xFF94A3B8);

  // États
  static const Color danger = Color(0xFFEF4444);
  static const Color warning = Color(0xFFF59E0B);
  static const Color success = Color(0xFF10B981);
  static const Color info = Color(0xFF3B82F6);

  // Badges et indicateurs
  static const Color emergency = Color(0xFFEF4444);
  static const Color emergencyLight = Color(0xFFFEE2E2);
}