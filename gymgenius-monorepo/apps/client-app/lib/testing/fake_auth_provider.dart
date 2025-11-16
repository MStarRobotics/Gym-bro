import 'package:client_app/providers/auth_provider.dart';

/// FakeAuthProvider is a lightweight test implementation of AuthProvider
/// that avoids contacting Firebase. Tests can use this to simulate
/// signing in/out flows without initializing Firebase.
class FakeAuthProvider extends AuthProvider {
  bool _signedIn = false;

  FakeAuthProvider() : super.noFirebase();

  @override
  bool get isAuthenticated => _signedIn;

  @override
  Future<bool> signInWithEmailPassword(String email, String password) async {
    _signedIn = true;
    notifyListeners();
    return true;
  }

  @override
  Future<bool> signUpWithEmailPassword(String email, String password, String fullName) async {
    _signedIn = true;
    notifyListeners();
    return true;
  }

  @override
  Future<void> signOut() async {
    _signedIn = false;
    notifyListeners();
  }
}
