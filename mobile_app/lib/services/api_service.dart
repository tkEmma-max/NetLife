import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:mobile_app/config/app_constants.dart';

class ApiService {
  static final ApiService _instance = ApiService._internal();
  factory ApiService() => _instance;
  ApiService._internal();

  String? _accessToken;
  String? _refreshToken;

  bool get isLoggedIn => _accessToken != null;

  // ----- GESTION DES TOKENS -----

  Future<void> saveTokens(String accessToken, String refreshToken) async {
    _accessToken = accessToken;
    _refreshToken = refreshToken;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('access_token', accessToken);
    await prefs.setString('refresh_token', refreshToken);
  }

  Future<void> loadTokens() async {
    final prefs = await SharedPreferences.getInstance();
    _accessToken = prefs.getString('access_token');
    _refreshToken = prefs.getString('refresh_token');
  }

  Future<void> clearTokens() async {
    _accessToken = null;
    _refreshToken = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');
    await prefs.remove('refresh_token');
  }

  Map<String, String> get _headers {
    return {
      'Content-Type': 'application/json',
      if (_accessToken != null) 'Authorization': 'Bearer $_accessToken',
    };
  }

  // ----- AUTHENTIFICATION -----

  Future<Map<String, dynamic>> login(String email, String password) async {
    print('=== LOGIN REQUEST ===');
    print('Email: $email');
    print('URL: ${AppConstants.baseUrl}/accounts/login/');

    final response = await http.post(
      Uri.parse('${AppConstants.baseUrl}/accounts/login/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );

    print('=== LOGIN RESPONSE ===');
    print('Status: ${response.statusCode}');
    print('Body: ${response.body}');

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await saveTokens(data['access'], data['refresh']);
      return data;
    } else {
      throw Exception('Échec de la connexion: ${response.body}');
    }
  }

  Future<Map<String, dynamic>> register({
    required String email,
    required String username,
    required String password,
    required String confirmPassword,
    String? phoneNumber,
    String role = 'CITIZEN',
  }) async {
    // Afficher ce qu'on envoie dans les logs
    print('=== REGISTER REQUEST ===');
    print('Email: $email');
    print('Username: $username');
    print('Password: $password');
    print('Confirm: $confirmPassword');
    print('Phone: $phoneNumber');
    print('Role: $role');
    print('URL: ${AppConstants.baseUrl}/accounts/register/');

    final response = await http.post(
      Uri.parse('${AppConstants.baseUrl}/accounts/register/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'email': email,
        'username': username,
        'password': password,
        'confirm_password': confirmPassword,
        'phone_number': phoneNumber ?? '',
        'role': role,
      }),
    );

    print('=== REGISTER RESPONSE ===');
    print('Status: ${response.statusCode}');
    print('Body: ${response.body}');

    if (response.statusCode == 201) {
      final data = jsonDecode(response.body);
      await saveTokens(data['access'], data['refresh']);
      return data;
    } else {
      throw Exception('Échec de l\'inscription: ${response.body}');
    }
  }

  Future<void> logout() async {
    await clearTokens();
  }

  // ----- PROFIL -----

  Future<Map<String, dynamic>> getProfile() async {
    final response = await http.get(
      Uri.parse('${AppConstants.baseUrl}/accounts/profile/'),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Impossible de charger le profil');
    }
  }

  // ----- SIGNALEMENTS -----

  Future<Map<String, dynamic>> submitReport({
    required String title,
    required String description,
    required String filePath,
    required double latitude,
    required double longitude,
    String? address,
  }) async {
    var request = http.MultipartRequest(
      'POST',
      Uri.parse('${AppConstants.baseUrl}/reports/submit/'),
    );
    request.headers.addAll({
      'Authorization': 'Bearer $_accessToken',
    });
    request.fields['title'] = title;
    request.fields['description'] = description;
    request.fields['latitude'] = latitude.toString();
    request.fields['longitude'] = longitude.toString();
    if (address != null) request.fields['address'] = address;

    request.files.add(
      await http.MultipartFile.fromPath('evidence', filePath),
    );

    final response = await request.send();
    final responseBody = await response.stream.bytesToString();
    final data = jsonDecode(responseBody);

    if (response.statusCode == 201) {
      return data;
    } else {
      throw Exception('Échec de l\'envoi du signalement');
    }
  }

  Future<List<dynamic>> getMyReports() async {
    final response = await http.get(
      Uri.parse('${AppConstants.baseUrl}/reports/my-reports/'),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Impossible de charger vos signalements');
    }
  }

  Future<Map<String, dynamic>> getReportDetails(int id) async {
    final response = await http.get(
      Uri.parse('${AppConstants.baseUrl}/reports/$id/'),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Impossible de charger le signalement');
    }
  }

  // ----- ANALYSE IA -----

  Future<Map<String, dynamic>> getAIAnalysis(int reportId) async {
    final response = await http.get(
      Uri.parse('${AppConstants.baseUrl}/ai/analysis/$reportId/'),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Analyse IA non disponible');
    }
  }

  // ----- ALERTES -----

  Future<List<dynamic>> getActiveAlerts() async {
    final response = await http.get(
      Uri.parse('${AppConstants.baseUrl}/alerts/active/'),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return [];
    }
  }

  Future<List<dynamic>> getNearbyAlerts(
    double latitude,
    double longitude, {
    double radius = 5,
  }) async {
    final response = await http.get(
      Uri.parse(
        '${AppConstants.baseUrl}/alerts/nearby/?latitude=$latitude&longitude=$longitude&radius=$radius',
      ),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return [];
    }
  }

  // ----- POINTS -----

  Future<Map<String, dynamic>> getPoints() async {
    final response = await http.get(
      Uri.parse('${AppConstants.baseUrl}/accounts/points/'),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Impossible de charger vos points');
    }
  }

  // ----- NOTIFICATIONS -----

  Future<List<dynamic>> getNotifications({bool unreadOnly = false}) async {
    final url = unreadOnly
        ? '${AppConstants.baseUrl}/notifications/?unread_only=true'
        : '${AppConstants.baseUrl}/notifications/';
    final response = await http.get(
      Uri.parse(url),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      return [];
    }
  }

  Future<int> getUnreadNotificationCount() async {
    final response = await http.get(
      Uri.parse('${AppConstants.baseUrl}/notifications/unread-count/'),
      headers: _headers,
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['unread_count'] ?? 0;
    } else {
      return 0;
    }
  }

  Future<void> markNotificationRead(int id) async {
    await http.post(
      Uri.parse('${AppConstants.baseUrl}/notifications/$id/read/'),
      headers: _headers,
    );
  }

  Future<void> markAllNotificationsRead() async {
    await http.post(
      Uri.parse('${AppConstants.baseUrl}/notifications/mark-all-read/'),
      headers: _headers,
    );
  }
}