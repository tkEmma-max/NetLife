// CARTE INTERACTIVE LIFENET
// Affiche les incidents sur une carte OpenStreetMap

import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:mobile_app/config/app_colors.dart';

class IncidentMap extends StatelessWidget {
  final List<Map<String, dynamic>> incidents;
  final double height;
  final double? latitude;
  final double? longitude;

  const IncidentMap({
    super.key,
    required this.incidents,
    this.height = 200,
    this.latitude,
    this.longitude,
  });

  @override
  Widget build(BuildContext context) {
    // Position par défaut : Douala, Cameroun
    final centerLat = latitude ?? 4.0511;
    final centerLon = longitude ?? 9.7679;

    // Points pour la carte
    final markers = incidents.map((incident) {
      return Marker(
        point: LatLng(
          incident['lat'] ?? centerLat,
          incident['lon'] ?? centerLon,
        ),
        width: 40,
        height: 40,
        child: _buildMarker(incident),
      );
    }).toList();

    // Ajouter un marqueur pour la position de l'utilisateur
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
          initialZoom: 12,
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

  Widget _buildMarker(Map<String, dynamic> incident) {
    final gravity = incident['gravity'] ?? 3;
    Color markerColor;

    if (gravity >= 4) {
      markerColor = AppColors.danger;
    } else if (gravity >= 3) {
      markerColor = AppColors.warning;
    } else {
      markerColor = AppColors.success;
    }

    return Container(
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
          incident['type']?.substring(0, 1).toUpperCase() ?? '?',
          style: const TextStyle(
            color: Colors.white,
            fontSize: 12,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}