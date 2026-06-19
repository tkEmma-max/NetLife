import 'package:flutter/material.dart';

class AppColors {
  // Dominante (60%) - Fond
  static const Color background = Color(0xFFF8F9FA);

  // Secondaire (30%) - Vert Émeraude (identité, nature)
  static const Color primary = Color(0xFF059669);
  static const Color primaryLight = Color(0xFFD1FAE5);
  static const Color primaryDark = Color(0xFF047857);

  // Pour rétrocompatibilité
  static const Color secondary = Color(0xFF059669);
  static const Color secondaryLight = Color(0xFFD1FAE5);
  static const Color forest = Color(0xFF059669);
  static const Color water = Color(0xFF3B82F6);

  // Gris (structure)
  static const Color border = Color(0xFF9CA3AF);
  static const Color textSecondary = Color(0xFF6B7280);
  static const Color textTertiary = Color(0xFF9CA3AF);

  // Noir (lisibilité)
  static const Color textPrimary = Color(0xFF111827);

  // Accent (10%) - Orange Alerte (urgence uniquement)
  static const Color danger = Color(0xFFF97316);
  static const Color dangerLight = Color(0xFFFFEDD5);

  // États
  static const Color success = Color(0xFF059669);
  static const Color warning = Color(0xFFF97316);
  static const Color error = Color(0xFFEF4444);
  static const Color info = Color(0xFF3B82F6);

  // Surface
  static const Color surface = Color(0xFFFFFFFF);
  static const Color surfaceElevated = Color(0xFFFFFFFF);

  // Urgence
  static const Color emergency = Color(0xFFF97316);
  static const Color emergencyLight = Color(0xFFFFEDD5);
}