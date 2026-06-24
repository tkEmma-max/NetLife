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

        // Liste des parties d'adresse disponibles
        List<String> parts = [];

        // 1. Quartier / sous-localité (ex: Bonamoussadi)
        if (place.subLocality != null && place.subLocality!.isNotEmpty) {
          parts.add(place.subLocality!);
        }

        // 2. Ville / localité (ex: Douala)
        if (place.locality != null && place.locality!.isNotEmpty) {
          parts.add(place.locality!);
        }

        // 3. Si on a des parties, on les combine
        if (parts.isNotEmpty) {
          return parts.join(', ');
        }

        // 4. Si on a une rue + numéro (plus précis)
        if (place.street != null && place.street!.isNotEmpty) {
          String address = place.street!;
          if (place.subLocality != null && place.subLocality!.isNotEmpty) {
            address += ', ${place.subLocality}';
          }
          return address;
        }

        // 5. Fallback : région + pays
        List<String> fallbackParts = [];
        if (place.administrativeArea != null && place.administrativeArea!.isNotEmpty) {
          fallbackParts.add(place.administrativeArea!);
        }
        if (place.country != null && place.country!.isNotEmpty) {
          fallbackParts.add(place.country!);
        }
        if (fallbackParts.isNotEmpty) {
          return fallbackParts.join(', ');
        }

        return 'Position inconnue';
      }
      return 'Position inconnue';
    } catch (e) {
      print('Erreur geocoding: $e');
      return 'Position non disponible';
    }
  }
}