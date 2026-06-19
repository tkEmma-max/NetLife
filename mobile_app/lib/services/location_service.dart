import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';

class LocationService {
  // Vérifier si la localisation est activée
  static Future<bool> isLocationEnabled() async {
    return await Geolocator.isLocationServiceEnabled();
  }

  // Demander les permissions
  static Future<bool> requestPermission() async {
    final status = await Permission.location.request();
    return status.isGranted;
  }

  // Récupérer la position actuelle
  static Future<Position?> getCurrentLocation() async {
    // Vérifier si la localisation est activée
    final enabled = await isLocationEnabled();
    if (!enabled) {
      return null;
    }

    // Vérifier les permissions
    final permission = await Permission.location.status;
    if (!permission.isGranted) {
      final granted = await requestPermission();
      if (!granted) return null;
    }

    // Récupérer la position
    try {
      return await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
    } catch (e) {
      print('Erreur de géolocalisation : $e');
      return null;
    }
  }

  // Formater la position en texte
  static String formatPosition(Position position) {
    return '${position.latitude.toStringAsFixed(6)}, ${position.longitude.toStringAsFixed(6)}';
  }
}