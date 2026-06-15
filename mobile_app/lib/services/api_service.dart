// SERVICE API LIFENET
// Responsable : tous les appels vers le backend Django (NetLife)
// Centralise les requêtes HTTP, les tokens, les erreurs

import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:mobile_app/config/app_constants.dart';

class ApiService {
  // Singleton : une seule instance dans toute l'app
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  // Token JWT stocké en mémoire (plus tard on le sauvegardera)
  String? _token;

  // Getter pour savoir si l'utilisateur est connecté
  bool get isLoggedIn => _token != null;

  // Définir le token après connexion
  void setToken(String token) {
    _token = token;
  }

  // Supprimer le token (déconnexion)
  void clearToken() {
    _token = null;
  }

  // Headers communs pour toutes les requêtes authentifiées
  Map<String, String> _getHeaders() {
    return {
      'Content-Type': 'application/json',
      if (_token != null) 'Authorization': 'Bearer $_token',
    };
  }

  // ----- POINTS D'ENTRÉE API -----

  // Connexion
  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('${AppConstants.baseUrl}/api/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      _token = data['token'];
      return data;
    } else {
      throw Exception('Échec de la connexion : ${response.body}');
    }
  }

  // Inscription
  Future<Map<String, dynamic>> register(
    String username,
    String email,
    String password,
  ) async {
    final response = await http.post(
      Uri.parse('${AppConstants.baseUrl}/api/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'email': email,
        'password': password,
      }),
    );

    if (response.statusCode == 201) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Échec de l\'inscription : ${response.body}');
    }
  }

  // Déconnexion
  Future<void> logout() async {
    // TODO: appeler l'API de déconnexion si besoin
    _token = null;
  }
}