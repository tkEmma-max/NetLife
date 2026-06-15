// POINT D'ENTRÉE PRINCIPAL DE L'APPLICATION
// Ce fichier est exécuté en premier au démarrage

import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_theme.dart';
import 'package:mobile_app/screens/login_screen.dart';

void main() {
  runApp(const LifeNetApp());
}

class LifeNetApp extends StatelessWidget {
  const LifeNetApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'LifeNet',
      theme: AppTheme.lightTheme,
      debugShowCheckedModeBanner: false,
      // LoginScreen est maintenant l'écran d'accueil
      home: const LoginScreen(),
    );
  }
}