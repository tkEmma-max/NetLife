// ÉCRAN D'INSCRIPTION
// Responsable : création d'un nouveau compte utilisateur
// Route : appelée depuis LoginScreen (lien "Créer un compte")

import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  // Contrôleurs des champs du formulaire
  final _formKey = GlobalKey<FormState>();
  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // Fond avec dégradé (identique à LoginScreen pour cohérence)
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [AppColors.forest, AppColors.water],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
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
                          'Créer un compte',
                          style: Theme.of(context).textTheme.headlineLarge,
                        ),
                        const SizedBox(height: 32),

                        // ----- CHAMP NOM D'UTILISATEUR -----
                        TextFormField(
                          controller: _usernameController,
                          decoration: const InputDecoration(
                            labelText: 'Nom d\'utilisateur',
                            prefixIcon: Icon(Icons.person),
                          ),
                          validator: (value) {
                            if (value == null || value.isEmpty) {
                              return 'Nom d\'utilisateur requis';
                            }
                            if (value.length < 3) {
                              return 'Minimum 3 caractères';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 16),

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
                          obscureText: true,
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
                        const SizedBox(height: 16),

                        // ----- CHAMP CONFIRMATION MOT DE PASSE -----
                        TextFormField(
                          controller: _confirmPasswordController,
                          obscureText: true,
                          decoration: const InputDecoration(
                            labelText: 'Confirmer le mot de passe',
                            prefixIcon: Icon(Icons.lock_outline),
                          ),
                          validator: (value) {
                            if (value != _passwordController.text) {
                              return 'Les mots de passe ne correspondent pas';
                            }
                            return null;
                          },
                        ),
                        const SizedBox(height: 24),

                        // ----- BOUTON INSCRIPTION -----
                        ElevatedButton(
                          onPressed: () {
                            if (_formKey.currentState!.validate()) {
                              // TODO: Appeler l'API Django (NetLife backend)
                              // Endpoint attendu : POST http://10.0.2.2:8000/api/register/
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(content: Text('Inscription en cours...')),
                              );
                            }
                          },
                          child: const Text('S\'INSCRIRE'),
                        ),
                        const SizedBox(height: 16),

                        // ----- LIEN RETOUR CONNEXION -----
                        TextButton(
                          onPressed: () {
                            Navigator.pop(context); // Retourne à l'écran précédent (Login)
                          },
                          child: const Text('Déjà un compte ? Se connecter'),
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