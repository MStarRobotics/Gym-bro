import 'package:flutter/material.dart';

import '../../core/theme/app_theme.dart';

class KineticButton extends StatefulWidget {
  final VoidCallback? onPressed;
  final Widget child;
  final double width;
  final double height;

  const KineticButton({
    Key? key,
    required this.onPressed,
    required this.child,
    this.width = double.infinity,
    this.height = 56,
  }) : super(key: key);

  @override
  State<KineticButton> createState() => _KineticButtonState();
}

class _KineticButtonState extends State<KineticButton>
    with TickerProviderStateMixin {
  late AnimationController _scaleController;
  late AnimationController _glowController;
  late Animation<double> _scaleAnimation;
  late Animation<double> _glowAnimation;

  @override
  void initState() {
    super.initState();

    _scaleController = AnimationController(
      duration: const Duration(milliseconds: 150),
      vsync: this,
    );

    _glowController = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(begin: 1.0, end: 0.95).animate(
      CurvedAnimation(parent: _scaleController, curve: Curves.easeInOut),
    );

    _glowAnimation = Tween<double>(begin: 0.5, end: 1.0).animate(
      CurvedAnimation(parent: _glowController, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _scaleController.dispose();
    _glowController.dispose();
    super.dispose();
  }

  void _onTapDown(TapDownDetails details) {
    _scaleController.forward();
    _glowController.forward();
  }

  void _onTapUp(TapUpDetails details) {
    _scaleController.reverse();
    _glowController.reverse();
  }

  void _onTapCancel() {
    _scaleController.reverse();
    _glowController.reverse();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: widget.onPressed != null ? _onTapDown : null,
      onTapUp: widget.onPressed != null ? _onTapUp : null,
      onTapCancel: widget.onPressed != null ? _onTapCancel : null,
      onTap: widget.onPressed,
      child: AnimatedBuilder(
        animation: Listenable.merge([_scaleController, _glowController]),
        builder: (context, child) {
          return Transform.scale(
            scale: _scaleAnimation.value,
            child: Container(
              width: widget.width,
              height: widget.height,
              decoration: BoxDecoration(
                gradient: widget.onPressed != null
                    ? LinearGradient(
                        colors: [
                          AppColors.primaryGlow
                              .withOpacity(_glowAnimation.value),
                          AppColors.secondaryGlow
                              .withOpacity(_glowAnimation.value),
                        ],
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                      )
                    : null,
                color: widget.onPressed != null
                    ? null
                    : AppColors.textTertiary,
                borderRadius: BorderRadius.circular(12),
                boxShadow: widget.onPressed != null
                    ? [
                        BoxShadow(
                          color: AppColors.primaryGlow
                              .withOpacity(0.5 * _glowAnimation.value),
                          blurRadius: 20,
                          spreadRadius: 2,
                        ),
                      ]
                    : null,
              ),
              child: Center(child: child),
            ),
          );
        },
        child: widget.child,
      ),
    );
  }
}
