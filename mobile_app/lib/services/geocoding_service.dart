import 'package:geocoding/geocoding.dart';
import 'package:geolocator/geolocator.dart';

class GeocodingService {
  // Convertir des coordonnées GPS en adresse
  static Future<String> getAddressFromCoordinates(
    double latitude,
    double longitude,
  ) async {
    try {
      final placemarks = await placemarkFromCoordinates(
        latitude,
        longitude,
      );
      if (placemarks.isNotEmpty) {
        final place = placemarks.first;
        // Construire une adresse lisible
        List<String> parts = [];
        if (place.street != null && place.street!.isNotEmpty) {
          parts.add(place.street!);
        }
        if (place.subLocality != null && place.subLocality!.isNotEmpty) {
          parts.add(place.subLocality!);
        }
        if (place.locality != null && place.locality!.isNotEmpty) {
          parts.add(place.locality!);
        }
        if (parts.isEmpty) {
          // Si on n'a pas d'adresse précise
          return '${place.administrativeArea ?? ''} ${place.country ?? ''}'.trim();
        }
        return parts.join(', ');
      }
      return 'Position: $latitude, $longitude';
    } catch (e) {
      print('Erreur geocoding: $e');
      return 'Position: ${latitude.toStringAsFixed(4)}, ${longitude.toStringAsFixed(4)}';
    }
  }
}