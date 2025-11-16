import 'package:flutter/foundation.dart';

class WorkoutProvider with ChangeNotifier {
  // Placeholder for workout state management
  bool _isLoading = false;

  bool get isLoading => _isLoading;

  Future<void> fetchWorkouts() async {
    _isLoading = true;
    notifyListeners();
    
    // TODO: Implement API call
    await Future.delayed(const Duration(seconds: 1));
    
    _isLoading = false;
    notifyListeners();
  }
}
