import 'package:flutter/material.dart';
import 'package:mobile_app/config/app_colors.dart';

class AvatarWidget extends StatelessWidget {
  final String name;
  final double size;

  const AvatarWidget({
    super.key,
    required this.name,
    this.size = 40,
  });

  @override
  Widget build(BuildContext context) {
    // Récupérer les initiales
    String initials = '';
    if (name.isNotEmpty) {
      final parts = name.trim().split(' ');
      if (parts.length >= 2) {
        initials = parts[0][0].toUpperCase() + parts[1][0].toUpperCase();
      } else {
        initials = parts[0][0].toUpperCase();
      }
    }

    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: AppColors.primary.withOpacity(0.15),
        shape: BoxShape.circle,
        border: Border.all(
          color: AppColors.primary.withOpacity(0.3),
          width: 1.5,
        ),
      ),
      child: Center(
        child: Text(
          initials,
          style: TextStyle(
            fontSize: size * 0.45,
            fontWeight: FontWeight.w600,
            color: AppColors.primary,
          ),
        ),
      ),
    );
  }
}