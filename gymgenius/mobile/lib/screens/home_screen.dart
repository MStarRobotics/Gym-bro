import 'package:flutter/material.dart';
import '../core/theme.dart';
import '../widgets/kinetic_button.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen>
    with TickerProviderStateMixin {
  late AnimationController _fadeController;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    // Kinetic Design System: Smooth fade-in animation for initial load
    _fadeController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _fadeController, curve: Curves.easeOut),
    );
    _fadeController.forward();
  }

  @override
  void dispose() {
    _fadeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundDark,
      appBar: AppBar(
        title: Text(
          'GymGenius',
          style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                color: AppTheme.primaryGlow,
                fontWeight: FontWeight.bold,
              ),
        ),
        backgroundColor: AppTheme.surfaceDark,
        elevation: 0,
        actions: [
          // Kinetic Design System: Animated settings icon
          IconButton(
            icon: Icon(Icons.settings, color: AppTheme.textPrimary),
            onPressed: () {
              // TODO: Navigate to settings
            },
          ),
        ],
      ),
      body: FadeTransition(
        opacity: _fadeAnimation,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Welcome Section with Biometric Glow
              Container(
                padding: const EdgeInsets.all(24),
                decoration: AppTheme.glowDecoration(AppTheme.primaryGlow),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Welcome to GymGenius',
                      style: Theme.of(context).textTheme.headlineLarge,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Your AI-powered fitness companion',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: AppTheme.textSecondary,
                          ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 24),

              // Feature Grid - Kinetic Design System: Grid layout with hover effects
              Expanded(
                child: GridView.count(
                  crossAxisCount: 2,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                  children: [
                    _buildFeatureCard(
                      context,
                      'Workout Plans',
                      Icons.fitness_center,
                      AppTheme.primaryGlow,
                      () {
                        // TODO: Navigate to workout plans
                      },
                    ),
                    _buildFeatureCard(
                      context,
                      'Meal Tracking',
                      Icons.restaurant,
                      AppTheme.secondaryGlow,
                      () {
                        // TODO: Navigate to meal tracking
                      },
                    ),
                    _buildFeatureCard(
                      context,
                      'Progress Analytics',
                      Icons.analytics,
                      AppTheme.accentGlow,
                      () {
                        // TODO: Navigate to analytics
                      },
                    ),
                    _buildFeatureCard(
                      context,
                      'AI Coach',
                      Icons.smart_toy,
                      AppTheme.primaryGlow,
                      () {
                        // TODO: Navigate to AI chat
                      },
                    ),
                  ],
                ),
              ),

              // Kinetic Button - Core component demonstrating Fluid Interaction
              const SizedBox(height: 24),
              Center(
                child: KineticButton(
                  onPressed: () {
                    // Kinetic Design System: Haptic feedback on interaction
                    // TODO: Start quick workout
                  },
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 32, vertical: 16),
                    child: Text(
                      'Start Quick Workout',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: AppTheme.backgroundDark,
                            fontWeight: FontWeight.w600,
                          ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // Kinetic Design System: Animated feature cards with glow effects
  Widget _buildFeatureCard(BuildContext context, String title, IconData icon,
      Color glowColor, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: AppTheme.surfaceDark,
          borderRadius: BorderRadius.circular(16),
          boxShadow: [AppTheme.glowShadow(glowColor, blurRadius: 10)],
          border: Border.all(
            color: glowColor.withOpacity(0.3),
            width: 1,
          ),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 48,
              color: glowColor,
            ),
            const SizedBox(height: 12),
            Text(
              title,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    color: AppTheme.textPrimary,
                    fontWeight: FontWeight.w600,
                  ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}