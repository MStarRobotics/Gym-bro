import 'package:flutter/material.dart';

class AppTheme {
  // Biometric Glow Color Palette
  static const Color primaryGlow = Color(0xFF00D4FF); // Electric Blue
  static const Color secondaryGlow = Color(0xFF00FF88); // Neon Green
  static const Color accentGlow = Color(0xFFFF0080); // Hot Pink
  static const Color backgroundDark = Color(0xFF0A0A0A); // Deep Black
  static const Color surfaceDark = Color(0xFF1A1A1A); // Dark Gray
  static const Color textPrimary = Color(0xFFFFFFFF); // White
  static const Color textSecondary = Color(0xFFB0B0B0); // Light Gray

  static ThemeData get darkTheme {
    return ThemeData(
      brightness: Brightness.dark,
      primaryColor: primaryGlow,
      scaffoldBackgroundColor: backgroundDark,
      appBarTheme: AppBarTheme(
        backgroundColor: surfaceDark,
        foregroundColor: textPrimary,
        elevation: 0,
      ),
      cardTheme: CardTheme(
        color: surfaceDark,
        elevation: 8,
        shadowColor: primaryGlow.withOpacity(0.3),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
      ),
      textTheme: TextTheme(
        headlineLarge: TextStyle(
          fontSize: 32,
          fontWeight: FontWeight.bold,
          color: textPrimary,
          fontFamily: 'Roboto',
          letterSpacing: -0.5,
        ),
        headlineMedium: TextStyle(
          fontSize: 28,
          fontWeight: FontWeight.w600,
          color: textPrimary,
          fontFamily: 'Roboto',
          letterSpacing: -0.25,
        ),
        bodyLarge: TextStyle(
          fontSize: 16,
          fontWeight: FontWeight.normal,
          color: textPrimary,
          fontFamily: 'Roboto',
        ),
        bodyMedium: TextStyle(
          fontSize: 14,
          fontWeight: FontWeight.normal,
          color: textSecondary,
          fontFamily: 'Roboto',
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryGlow,
          foregroundColor: backgroundDark,
          padding: EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
          ),
          textStyle: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            fontFamily: 'Roboto',
          ),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surfaceDark,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: primaryGlow),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: BorderSide(color: primaryGlow, width: 2),
        ),
        labelStyle: TextStyle(color: textSecondary),
      ),
    );
  }

  // Glow Effects
  static BoxShadow glowShadow(Color color, {double blurRadius = 20}) {
    return BoxShadow(
      color: color.withOpacity(0.5),
      blurRadius: blurRadius,
      spreadRadius: 2,
    );
  }

  static BoxDecoration glowDecoration(Color color) {
    return BoxDecoration(
      borderRadius: BorderRadius.circular(16),
      boxShadow: [glowShadow(color)],
      gradient: LinearGradient(
        colors: [color.withOpacity(0.1), color.withOpacity(0.05)],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
    );
  }
}