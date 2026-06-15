// PALETTE DE COULEURS LIFENET
// Style : moderne, minimaliste, inspiré de Chariow / Fiverr
// Les couleurs principales sont utilisées par touches, jamais en fond plein

import 'package:flutter/material.dart';

class AppColors {
  // ----- COULEURS D'IDENTITÉ (utilisées par petites touches) -----
  static const Color primary = Color(0xFF006D5B);      // Vert profond (soutenu, pas agressif)
  static const Color primaryLight = Color(0xFFE8F3F1); // Vert très pâle (pour accents doux)
  static const Color accent = Color(0xFF2D9CDB);       // Bleu tech (pour liens, icônes)

  // ----- FONDS (neutres, majoritaires) -----
  static const Color background = Color(0xFFF5F7FA);   // Gris très clair (presque blanc)
  static const Color surface = Color(0xFFFFFFFF);      // Blanc pur pour cartes
  static const Color surfaceElevated = Color(0xFFFAFBFC); // Blanc légèrement grisé

  // ----- TEXTES (lisibilité maximale) -----
  static const Color textPrimary = Color(0xFF1A1F36);   // Gris très foncé (presque noir)
  static const Color textSecondary = Color(0xFF6B7280); // Gris moyen
  static const Color textTertiary = Color(0xFF9CA3AF);  // Gris clair

  // ----- ÉTATS & RETOURS -----
  static const Color success = Color(0xFF10B981);       // Vert
  static const Color warning = Color(0xFFF59E0B);       // Orange
  static const Color error = Color(0xFFEF4444);         // Rouge
  static const Color info = Color(0xFF3B82F6);          // Bleu

  // ----- EFFETS (glassmorphism, flous) -----
  static const Color glassBackground = Color(0xCCFFFFFF); // Blanc 80% opaque
  static const Color glassBorder = Color(0x33FFFFFF);     // Blanc 20% opaque
}