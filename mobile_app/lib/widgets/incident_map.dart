import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:mobile_app/config/app_colors.dart';
import 'package:mobile_app/widgets/custom_marker.dart';
import 'package:mobile_app/screens/alert_detail_screen.dart';
import 'package:mobile_app/widgets/custom_marker.dart';

class IncidentMap extends StatelessWidget {
  final List<Map<String, dynamic>> incidents;
  final double height;
  final double? latitude;
  final double? longitude;
  final double zoom;
  final Function(int)? onMarkerTap;

  const IncidentMap({
    super.key,
    required this.incidents,
    this.height = 200,
    this.latitude,
    this.longitude,
    this.zoom = 14,
    this.onMarkerTap,
  });

  @override
  Widget build(BuildContext context) {
    final centerLat = latitude ?? 4.0511;
    final centerLon = longitude ?? 9.7679;

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
      final type = incident['type'] as String? ?? 'other';
      final alertId = incident['id'] ?? 0;

      markers.add(
        Marker(
          point: LatLng(lat, lon),
          width: 44,
          height: 44,
          child: CustomMarker(
            dangerType: type,
            gravity: gravity,
            onTap: () {
              // Si on a un callback, on l'utilise
              if (onMarkerTap != null) {
                onMarkerTap!(alertId as int);
              } else {
                // Sinon, navigation directe
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => AlertDetailScreen(alertId: alertId as int),
                  ),
                );
              }
            },
          ),
        ),
      );
    }

    return Container(
      height: height,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppColors.border.withOpacity(0.15),
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