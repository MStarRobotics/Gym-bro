import 'package:flutter/material.dart';

/// Biometric Glow Design System - Color Palette
class AppColors {
  // Primary Colors
  static const Color primaryGlow = Color(0xFF00D4FF); // Electric Blue
  static const Color secondaryGlow = Color(0xFF00FF88); // Neon Green
  static const Color accentGlow = Color(0xFFFF0080); // Hot Pink
  
  // Background
  static const Color backgroundDark = Color(0xFF0A0A0F);
  static const Color surfaceDark = Color(0xFF1A1A2E);
  static const Color cardDark = Color(0xFF16213E);
  
  // Text
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFB3B3B3);
  static const Color textTertiary = Color(0xFF666666);
  
  // Status
  static const Color success = Color(0xFF00FF88);
  static const Color warning = Color(0xFFFFB800);
  static const Color error = Color(0xFFFF0055);
  
  // Gradients
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [primaryGlow, secondaryGlow],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
  
  static const LinearGradient accentGradient = LinearGradient(
    colors: [accentGlow, primaryGlow],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      primaryColor: AppColors.primaryGlow,
      scaffoldBackgroundColor: Colors.white,
      colorScheme: const ColorScheme.light(
        primary: AppColors.primaryGlow,
        secondary: AppColors.secondaryGlow,
        tertiary: AppColors.accentGlow,
        surface: Colors.white,
        background: Colors.white,
        error: AppColors.error,
      ),
    );
  }
  
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      primaryColor: AppColors.primaryGlow,
      scaffoldBackgroundColor: AppColors.backgroundDark,
      colorScheme: const ColorScheme.dark(
        primary: AppColors.primaryGlow,
        secondary: AppColors.secondaryGlow,
        tertiary: AppColors.accentGlow,
        surface: AppColors.surfaceDark,
        background: AppColors.backgroundDark,
        error: AppColors.error,
      ),
      cardTheme: CardTheme(
        color: AppColors.cardDark,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: AppColors.backgroundDark,
        elevation: 0,
        centerTitle: true,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.primaryGlow,
          foregroundColor: AppColors.textPrimary,
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
      ),
    );
  }
  
  // Glow Decoration Helper
  static BoxDecoration glowDecoration({
    Color glowColor = AppColors.primaryGlow,
    double borderRadius = 16,
  }) {
    return BoxDecoration(
      borderRadius: BorderRadius.circular(borderRadius),
      gradient: AppColors.primaryGradient,
      boxShadow: [
        BoxShadow(
          color: glowColor.withOpacity(0.5),
          blurRadius: 20,
          spreadRadius: 2,
        ),
      ],
    );
  }
}
