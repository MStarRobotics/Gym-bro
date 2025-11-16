import 'package:flutter/foundation.dart';

class ClientProvider with ChangeNotifier {
  // Client management state
  bool _isLoading = false;

  bool get isLoading => _isLoading;

  Future<void> fetchClients() async {
    _isLoading = true;
    notifyListeners();
    
    // TODO: Implement API call
    await Future.delayed(const Duration(seconds: 1));
    
    _isLoading = false;
    notifyListeners();
  }
}
