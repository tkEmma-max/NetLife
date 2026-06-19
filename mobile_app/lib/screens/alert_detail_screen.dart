// ÉCRAN DÉTAIL D'UNE ALERTE LIFENET

import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:mobile_app/config/app_colors.dart';
import 'package:mobile_app/services/api_service.dart';

class AlertDetailScreen extends StatefulWidget {
  final int alertId;
  const AlertDetailScreen({super.key, required this.alertId});

  @override
  State<AlertDetailScreen> createState() => _AlertDetailScreenState();
}

class _AlertDetailScreenState extends State<AlertDetailScreen> {
  final ApiService _apiService = ApiService();
  Map<String, dynamic>? _alert;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadAlertDetail();
  }

  Future<void> _loadAlertDetail() async {
    setState(() => _isLoading = true);
    try {
      final alert = await _apiService.getAlertDetail(widget.alertId);
      setState(() => _alert = alert);
    } catch (e) {
      print('Erreur chargement détail alerte: $e');
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text(
          'Détail de l\'alerte',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
        ),
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: AppColors.primary))
          : _alert == null
              ? const Center(
                  child: Text(
                    'Alerte introuvable',
                    style: TextStyle(color: AppColors.textSecondary),
                  ),
                )
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Type + Gravité
                      Row(
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 14,
                              vertical: 6,
                            ),
                            decoration: BoxDecoration(
                              color: _getPriorityColor(_alert!['priority'] ?? 'MEDIUM'),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(
                              _alert!['priority_display'] ?? 'Modéré',
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 13,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Container(
                            padding: const EdgeInsets.symmetric(
                              horizontal: 14,
                              vertical: 6,
                            ),
                            decoration: BoxDecoration(
                              color: _getStatusColor(_alert!['status'] ?? 'ACTIVE'),
                              borderRadius: BorderRadius.circular(20),
                            ),
                            child: Text(
                              _alert!['status_display'] ?? _alert!['status'] ?? 'ACTIVE',
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 13,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 20),

                      // Titre
                      Text(
                        _alert!['title'] ?? 'Alerte',
                        style: const TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 8),

                      // Lieu
                      Row(
                        children: [
                          const Icon(Icons.location_on,
                              size: 18, color: AppColors.textSecondary),
                          const SizedBox(width: 6),
                          Text(
                            _alert!['address'] ?? 'Lieu inconnu',
                            style: const TextStyle(
                              fontSize: 14,
                              color: AppColors.textSecondary,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 6),

                      // Date
                      Row(
                        children: [
                          const Icon(Icons.access_time,
                              size: 18, color: AppColors.textSecondary),
                          const SizedBox(width: 6),
                          Text(
                            _formatFullDate(_alert!['created_at']),
                            style: const TextStyle(
                              fontSize: 14,
                              color: AppColors.textSecondary,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 24),

                      // Description
                      const Text(
                        'Description',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 6),
                      Text(
                        _alert!['description'] ?? 'Aucune description disponible.',
                        style: const TextStyle(
                          fontSize: 14,
                          color: AppColors.textSecondary,
                        ),
                      ),
                      const SizedBox(height: 24),

                      // Équipe assignée
                      if (_alert!['assigned_team_name'] != null) ...[
                        const Text(
                          'Équipe assignée',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: AppColors.textPrimary,
                          ),
                        ),
                        const SizedBox(height: 6),
                        Text(
                          _alert!['assigned_team_name'] ?? 'Aucune',
                          style: const TextStyle(
                            fontSize: 14,
                            color: AppColors.textSecondary,
                          ),
                        ),
                        const SizedBox(height: 24),
                      ],

                      // Statistiques de l'alerte
                      const Text(
                        'Statistiques de l\'alerte',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.w600,
                          color: AppColors.textPrimary,
                        ),
                      ),
                      const SizedBox(height: 8),

                      Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: AppColors.surface,
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: AppColors.border.withOpacity(0.15),
                            width: 1,
                          ),
                        ),
                        child: Column(
                          children: [
                            _buildStatsRow(
                              'Citoyens notifiés',
                              '${_alert!['citizens_notified'] ?? 0}',
                            ),
                            const Divider(height: 16),
                            _buildStatsRow(
                              'Citoyens confirmés',
                              '${_alert!['citizens_confirmed'] ?? 0}',
                            ),
                            const Divider(height: 16),
                            _buildStatsRow(
                              'Durée (minutes)',
                              _alert!['duration_minutes']?.toString() ?? '0',
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 24),

                      // Bouton retour
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          onPressed: () => Navigator.pop(context),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primary,
                            padding: const EdgeInsets.symmetric(vertical: 14),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          child: const Text(
                            'Retour aux alertes',
                            style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
    );
  }

  Widget _buildStatsRow(String label, String value) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(
          label,
          style: const TextStyle(
            fontSize: 14,
            color: AppColors.textSecondary,
          ),
        ),
        Text(
          value,
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w600,
            color: AppColors.textPrimary,
          ),
        ),
      ],
    );
  }

  Color _getPriorityColor(String priority) {
    switch (priority.toUpperCase()) {
      case 'CRITICAL':
        return AppColors.danger;
      case 'HIGH':
        return const Color(0xFFF97316);
      case 'MEDIUM':
        return const Color(0xFFF59E0B);
      case 'LOW':
        return AppColors.success;
      default:
        return AppColors.textSecondary;
    }
  }

  Color _getStatusColor(String status) {
    switch (status.toUpperCase()) {
      case 'ACTIVE':
      case 'IN_PROGRESS':
        return Colors.blue;
      case 'RESOLVED':
      case 'CLOSED':
        return AppColors.success;
      case 'REJECTED':
      case 'CANCELLED':
        return AppColors.error;
      default:
        return AppColors.textSecondary;
    }
  }

  String _formatFullDate(String? isoString) {
    if (isoString == null) return 'Date inconnue';
    try {
      final date = DateTime.parse(isoString);
      return DateFormat('dd MMMM yyyy à HH:mm', 'fr').format(date);
    } catch (e) {
      return 'Date inconnue';
    }
  }
}