import 'package:flutter/foundation.dart';

class ChatProvider with ChangeNotifier {
  // Placeholder for chat state management
  bool _isLoading = false;

  bool get isLoading => _isLoading;

  Future<void> sendMessage(String message) async {
    _isLoading = true;
    notifyListeners();
    
    // TODO: Implement Socket.io integration
    await Future.delayed(const Duration(seconds: 1));
    
    _isLoading = false;
    notifyListeners();
  }
}
