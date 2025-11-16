import 'package:flutter/foundation.dart';
import 'package:firebase_auth/firebase_auth.dart';

class AuthProvider with ChangeNotifier {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  User? _user;

  User? get user => _user;
  bool get isAuthenticated => _user != null;

  AuthProvider() {
    _auth.authStateChanges().listen((User? user) {
      _user = user;
      notifyListeners();
    });
  }

  /// Named constructor for test environments that should not connect to Firebase.
  AuthProvider.noFirebase();

  Future<void> signOut() async {
    await _auth.signOut();
  }

  /// Set a user for tests without requiring Firebase. This helps tests
  /// simulate authenticated state without initialising Firebase.
  @visibleForTesting
  void setTestUser(User? user) {
    _user = user;
    notifyListeners();
  }
}
