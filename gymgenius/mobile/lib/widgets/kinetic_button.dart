import 'package:flutter/material.dart';
import '../core/theme.dart';

/// KineticButton - A custom animated button demonstrating the 'Fluid Interaction' principle
/// of the Kinetic Design System. Features smooth animations, haptic feedback, and
/// dynamic visual responses to user interactions.
///
/// **Key Features:**
/// - **Tactile Feedback**: Scales down on press to simulate physical button pressing
/// - **Glow Effect**: Intensifies on interaction, creating a "charging" visual
/// - **Smooth Animations**: Uses CurvedAnimations for natural, organic movement
/// - **Flexible API**: Supports child widget OR icon+label composition
class KineticButton extends StatefulWidget {
  final Widget? child;
  final String? label;
  final IconData? icon;
  final Color? glowColor;
  final VoidCallback? onPressed;
  final Duration animationDuration;
  final double scaleFactor;

  /// Create a KineticButton with a custom child widget
  const KineticButton({
    super.key,
    required this.child,
    this.onPressed,
    this.animationDuration = const Duration(milliseconds: 150),
    this.scaleFactor = 0.95,
    this.glowColor,
  })  : label = null,
        icon = null;

  /// Create a KineticButton with icon and label (for grid layouts)
  const KineticButton.withIcon({
    super.key,
    required this.label,
    required this.icon,
    this.glowColor,
    this.onPressed,
    this.animationDuration = const Duration(milliseconds: 150),
    this.scaleFactor = 0.95,
  }) : child = null;

  @override
  State<KineticButton> createState() => _KineticButtonState();
}

class _KineticButtonState extends State<KineticButton>
    with TickerProviderStateMixin {
  late AnimationController _scaleController;
  late Animation<double> _scaleAnimation;
  late AnimationController _glowController;
  late Animation<double> _glowAnimation;

  bool _isPressed = false;

  @override
  void initState() {
    super.initState();

    // Scale animation for press effect
    _scaleController = AnimationController(
      duration: widget.animationDuration,
      vsync: this,
    );
    _scaleAnimation = Tween<double>(
      begin: 1.0,
      end: widget.scaleFactor,
    ).animate(CurvedAnimation(
      parent: _scaleController,
      curve: Curves.easeInOut,
    ));

    // Glow animation for visual feedback
    _glowController = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _glowAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _glowController,
      curve: Curves.easeOut,
    ));
  }

  @override
  void dispose() {
    _scaleController.dispose();
    _glowController.dispose();
    super.dispose();
  }

  void _handleTapDown(TapDownDetails details) {
    setState(() => _isPressed = true);
    _scaleController.forward();
    _glowController.forward();
  }

  void _handleTapUp(TapUpDetails details) {
    setState(() => _isPressed = false);
    _scaleController.reverse();
    _glowController.reverse();
    widget.onPressed?.call();
  }

  void _handleTapCancel() {
    setState(() => _isPressed = false);
    _scaleController.reverse();
    _glowController.reverse();
  }

  @override
  Widget build(BuildContext context) {
    final Color effectiveGlowColor = widget.glowColor ?? AppTheme.primaryGlow;
    
    return GestureDetector(
      onTapDown: _handleTapDown,
      onTapUp: _handleTapUp,
      onTapCancel: _handleTapCancel,
      child: AnimatedBuilder(
        animation: Listenable.merge([_scaleAnimation, _glowAnimation]),
        builder: (context, child) {
          return Transform.scale(
            scale: _scaleAnimation.value,
            child: Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(12),
                gradient: LinearGradient(
                  colors: [
                    effectiveGlowColor.withOpacity(0.8 + _glowAnimation.value * 0.2),
                    effectiveGlowColor.withOpacity(0.6 + _glowAnimation.value * 0.4),
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                boxShadow: [
                  AppTheme.glowShadow(
                    effectiveGlowColor,
                    blurRadius: 20 + _glowAnimation.value * 10,
                  ),
                ],
              ),
              child: _buildContent(),
            ),
          );
        },
      ),
    );
  }

  /// Build the button content - either custom child or icon+label composition
  Widget _buildContent() {
    if (widget.child != null) {
      return widget.child!;
    }

    // Icon + Label layout for grid buttons
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (widget.icon != null) ...[
            Icon(
              widget.icon,
              color: AppTheme.backgroundDark,
              size: 24,
            ),
            const SizedBox(width: 8),
          ],
          Flexible(
            child: Text(
              widget.label ?? '',
              style: const TextStyle(
                color: AppTheme.backgroundDark,
                fontSize: 14,
                fontWeight: FontWeight.w600,
              ),
              textAlign: TextAlign.center,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }
}

/// KineticIconButton - A variant of KineticButton optimized for icon-only buttons
class KineticIconButton extends StatelessWidget {
  final IconData icon;
  final VoidCallback? onPressed;
  final double size;
  final Color? iconColor;

  const KineticIconButton({
    super.key,
    required this.icon,
    this.onPressed,
    this.size = 24,
    this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return KineticButton(
      onPressed: onPressed,
      child: Padding(
        padding: EdgeInsets.all(size * 0.5),
        child: Icon(
          icon,
          size: size,
          color: iconColor ?? AppTheme.backgroundDark,
        ),
      ),
    );
  }
}