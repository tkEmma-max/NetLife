// ÉCRAN DE CONNEXION
// Responsable : authentification des utilisateurs existants
// Route : appelé depuis main.dart ou après déconnexion

import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';
import 'register_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  // Contrôleurs des champs du formulaire
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // Fond avec dégradé vertical (vert forêt -> bleu eau)
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [AppColors.forest, AppColors.water],
          ),
        ),
        child: SafeArea(
          // SafeArea évite les zones avec notch (iPhone) ou barre d'état
          child: Center(
            child: SingleChildScrollView(
              // SingleChildScrollView permet de scroll si le clavier apparaît
              padding: const EdgeInsets.all(24),
              child: Card(
                elevation: 8,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(24),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        // ----- LOGO -----
                        const Icon(
                          Icons.forest,
                          size: 80,
                          color: AppColors.forest,
                        ),
                        const SizedBox(height: 16),

                        // ----- TITRE -----
                        Text(
                          'LifeNet',
                          style: Theme.of(context).textTheme.headlineLarge,
                        ),
                        const SizedBox(height: 32),

                        // ----- CHAMP EMAIL -----
                        TextFormField(
                          controller: _emailController,
                          decoration: const InputDecoration(
                            labelText: 'Email',
                            prefixIcon: Icon(Icons.email),
                          ),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Email requis';
                            }
                            if (!value.contains('@')) {
                              return 'Email invalide';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 16),

                        // ----- CHAMP MOT DE PASSE -----
                        TextFormField(
                          controller: _passwordController,
                          obscureText: true, // Cache le texte (affiche des •••)
                          decoration: const InputDecoration(
                            labelText: 'Mot de passe',
                            prefixIcon: Icon(Icons.lock),
                          ),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Mot de passe requis';
                            }
                            if (value.length < 6) {
                              return 'Minimum 6 caractères';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 24),

                        // ----- BOUTON CONNEXION -----
                        ElevatedButton(
                          onPressed: () {
                            if (_formKey.currentState!.validate()) {
                              // TODO: Appeler l'API Django (NetLife backend)
                              // Endpoint attendu : POST http://10.0.2.2:8000/api/login/
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('Connexion en cours...')),
                              );
                            }
                          },
                          child: const Text('SE CONNECTER'),
                        ),
                        const SizedBox(height: 16),

                        // ----- LIEN VERS INSCRIPTION -----
                        TextButton(
                          onPressed: () {
                            // Navigation vers l'écran d'inscription
                            Navigator.push(
                              context,
                              MaterialPageRoute(builder: (_) => const RegisterScreen()),
                            );
                          },
                          child: const Text('Pas encore de compte ? Créer un compte'),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}