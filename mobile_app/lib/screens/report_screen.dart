import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:mobile_app/config/app_colors.dart';

class ReportScreen extends StatefulWidget {
  const ReportScreen({super.key});

  @override
  State<ReportScreen> createState() => _ReportScreenState();
}

class _ReportScreenState extends State<ReportScreen> {
  File? _selectedImage;
  Position? _currentPosition;
  bool _isLoading = false;
  bool _isGettingLocation = false;
  final ImagePicker _picker = ImagePicker();

  Future<void> _takePhoto() async {
    final XFile? photo = await _picker.pickImage(
      source: ImageSource.camera,
      imageQuality: 80,
    );
    if (photo != null) {
      setState(() => _selectedImage = File(photo.path));
      await _getLocation();
    }
  }

  Future<void> _pickFromGallery() async {
    final XFile? photo = await _picker.pickImage(
      source: ImageSource.gallery,
      imageQuality: 80,
    );
    if (photo != null) {
      setState(() => _selectedImage = File(photo.path));
      await _getLocation();
    }
  }

  Future<void> _getLocation() async {
    setState(() => _isGettingLocation = true);

    final status = await Permission.location.request();
    if (!status.isGranted) {
      setState(() => _isGettingLocation = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Permission de localisation refusée'),
          backgroundColor: AppColors.danger,
        ),
      );
      return;
    }

    final enabled = await Geolocator.isLocationServiceEnabled();
    if (!enabled) {
      setState(() => _isGettingLocation = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Veuillez activer le GPS'),
          backgroundColor: AppColors.warning,
        ),
      );
      return;
    }

    try {
      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
      );
      setState(() => _currentPosition = position);
    } catch (e) {
      print('Erreur GPS: $e');
    }

    setState(() => _isGettingLocation = false);
  }

  Future<void> _submitReport() async {
    if (_selectedImage == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Veuillez prendre une photo'),
          backgroundColor: AppColors.warning,
        ),
      );
      return;
    }

    if (_currentPosition == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Position GPS non disponible'),
          backgroundColor: AppColors.warning,
        ),
      );
      return;
    }

    setState(() => _isLoading = true);
    await Future.delayed(const Duration(seconds: 2));

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Signalement envoyé avec succès !'),
          backgroundColor: AppColors.success,
        ),
      );
      Navigator.pop(context);
    }

    setState(() => _isLoading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Nouveau signalement'),
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Photo du danger',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 8),
            Text(
              'Prenez une photo du feu, déchet ou inondation',
              style: Theme.of(context).textTheme.bodyMedium,
            ),
            const SizedBox(height: 16),
            GestureDetector(
              onTap: () => _showImageSourceDialog(),
              child: Container(
                width: double.infinity,
                height: 250,
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppColors.secondaryLight, width: 2),
                ),
                child: _selectedImage != null
                    ? ClipRRect(
                        borderRadius: BorderRadius.circular(20),
                        child: Image.file(
                          _selectedImage!,
                          width: double.infinity,
                          height: 250,
                          fit: BoxFit.cover,
                        ),
                      )
                    : Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.camera_alt,
                            size: 64,
                            color: AppColors.primary.withOpacity(0.5),
                          ),
                          const SizedBox(height: 12),
                          Text(
                            'Appuyez pour prendre une photo',
                            style: TextStyle(color: AppColors.textSecondary),
                          ),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 24),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.surface,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Row(
                children: [
                  Icon(
                    _currentPosition != null
                        ? Icons.location_on
                        : Icons.location_off,
                    color: _currentPosition != null
                        ? AppColors.success
                        : AppColors.warning,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Position GPS',
                          style: TextStyle(
                            fontWeight: FontWeight.w600,
                            color: AppColors.textPrimary,
                          ),
                        ),
                        Text(
                          _isGettingLocation
                              ? 'Récupération en cours...'
                              : (_currentPosition != null
                                  ? '${_currentPosition!.latitude.toStringAsFixed(6)}, ${_currentPosition!.longitude.toStringAsFixed(6)}'
                                  : 'Position non disponible'),
                          style: TextStyle(
                            fontSize: 12,
                            color: AppColors.textSecondary,
                          ),
                        ),
                      ],
                    ),
                  ),
                  if (_currentPosition == null && !_isGettingLocation)
                    TextButton(
                      onPressed: _getLocation,
                      child: const Text('Réessayer'),
                    ),
                ],
              ),
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: _isLoading ? null : _submitReport,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.danger,
                ),
                child: _isLoading
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: Colors.white,
                        ),
                      )
                    : const Text('Envoyer le signalement'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showImageSourceDialog() {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt),
              title: const Text('Appareil photo'),
              onTap: () {
                Navigator.pop(context);
                _takePhoto();
              },
            ),
            ListTile(
              leading: const Icon(Icons.photo_library),
              title: const Text('Galerie'),
              onTap: () {
                Navigator.pop(context);
                _pickFromGallery();
              },
            ),
          ],
        ),
      ),
    );
  }
}