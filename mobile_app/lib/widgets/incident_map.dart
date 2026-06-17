// CARTE INTERACTIVE LIFENET
// S'adapte à la position de l'utilisateur

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:mobile_app/config/app_colors.dart';

class IncidentMap extends StatelessWidget {
  final List<Map<String, dynamic>> incidents;
  final double height;
  final double? latitude;
  final double? longitude;
  final double zoom;

  const IncidentMap({
    super.key,
    required this.incidents,
    this.height = 200,
    this.latitude,
    this.longitude,
    this.zoom = 14,
  });

  @override
  Widget build(BuildContext context) {
    // Si on a la position de l'utilisateur, on centre sur elle
    // Sinon, on centre sur Douala (fallback)
    final centerLat = latitude ?? 4.0511;
    final centerLon = longitude ?? 9.7679;

    // Construire les marqueurs des incidents
    final markers = <Marker>[];

    // Marqueur pour la position de l'utilisateur
    if (latitude != null && longitude != null) {
      markers.add(
        Marker(
          point: LatLng(latitude!, longitude!),
          width: 30,
          height: 30,
          child: Container(
            decoration: const BoxDecoration(
              color: AppColors.primary,
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: AppColors.primary,
                  blurRadius: 12,
                  spreadRadius: 4,
                ),
              ],
            ),
            child: const Icon(
              Icons.my_location,
              color: Colors.white,
              size: 16,
            ),
          ),
        ),
      );
    }

    // Marqueurs pour les incidents
    for (var incident in incidents) {
      final lat = incident['lat'] as double?;
      final lon = incident['lon'] as double?;
      if (lat == null || lon == null) continue;

      final gravity = incident['gravity'] ?? 3;
      Color markerColor;

      if (gravity >= 4) {
        markerColor = AppColors.danger;
      } else if (gravity >= 3) {
        markerColor = AppColors.warning;
      } else {
        markerColor = AppColors.success;
      }

      final type = incident['type'] as String? ?? '?';
      final label = type.isNotEmpty ? type.substring(0, 1).toUpperCase() : '?';

      markers.add(
        Marker(
          point: LatLng(lat, lon),
          width: 32,
          height: 32,
          child: Container(
            width: 32,
            height: 32,
            decoration: BoxDecoration(
              color: markerColor.withOpacity(0.9),
              shape: BoxShape.circle,
              border: Border.all(color: Colors.white, width: 2),
              boxShadow: [
                BoxShadow(
                  color: markerColor.withOpacity(0.4),
                  blurRadius: 12,
                  spreadRadius: 2,
                ),
              ],
            ),
            child: Center(
              child: Text(
                label,
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
        ),
      );
    }

    return Container(
      height: height,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppColors.textTertiary.withOpacity(0.15),
          width: 1,
        ),
      ),
      clipBehavior: Clip.hardEdge,
      child: FlutterMap(
        options: MapOptions(
          initialCenter: LatLng(centerLat, centerLon),
          initialZoom: zoom,
          interactionOptions: const InteractionOptions(
            flags: InteractiveFlag.all,
          ),
        ),
        children: [
          TileLayer(
            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            userAgentPackageName: 'com.lifenet.app',
          ),
          MarkerLayer(markers: markers),
        ],
      ),
    );
  }
}