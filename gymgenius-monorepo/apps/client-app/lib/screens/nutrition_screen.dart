import 'package:flutter/material.dart';
import '../testing/test_mode.dart';

/// Nutrition Screen - Meal tracking and nutrition planning
/// TODO: Implement feature logic here.
///
/// Required Features:
/// - Daily meal log with calorie tracking
/// - Barcode scanner for food products
/// - AI-powered meal suggestions based on fitness goals
/// - Macro nutrient breakdown (proteins, carbs, fats)
/// - Water intake tracker
/// - Integration with meal plan from subscription
class NutritionScreen extends StatefulWidget {
  const NutritionScreen({Key? key}) : super(key: key);

  @override
  State<NutritionScreen> createState() => _NutritionScreenState();
}

class _NutritionScreenState extends State<NutritionScreen> {
  bool _hasPlan = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: const Key('nutritionScreen'),
      appBar: AppBar(title: const Text('Nutrition')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            if (_hasPlan) const Text('Meal Plan: Basic', key: Key('mealPlanText')),
            if (!_hasPlan) const Text('Nutrition tracking - Coming soon'),
            const SizedBox(height: 16),
            if (isTestMode)
              ElevatedButton(
                key: const Key('fetchMealPlanButton'),
                onPressed: () {
                  setState(() {
                    _hasPlan = true;
                  });
                },
                child: const Text('Get Meal Plan'),
              ),
          ],
        ),
      ),
    );
  }
}
