import 'package:flutter/foundation.dart';

class MealProvider with ChangeNotifier {
  // Placeholder for meal state management
  bool _isLoading = false;

  bool get isLoading => _isLoading;

  Future<void> fetchMeals() async {
    _isLoading = true;
    notifyListeners();
    
    // TODO: Implement API call
    await Future.delayed(const Duration(seconds: 1));
    
    _isLoading = false;
    notifyListeners();
  }
}
