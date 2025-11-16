import 'package:trainer_app/providers/auth_provider.dart';

class FakeAuthProvider extends AuthProvider {
  bool _signedIn = false;

  FakeAuthProvider() : super.noFirebase();

  @override
  bool get isAuthenticated => _signedIn;

  void signInAsTestUser() {
    _signedIn = true;
    notifyListeners();
  }

  @override
  Future<void> signOut() async {
    _signedIn = false;
    notifyListeners();
  }
}
