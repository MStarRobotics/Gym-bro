import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:client_app/main.dart' as app;
import 'package:client_app/testing/fake_auth_provider.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  testWidgets('App launches and shows MaterialApp', (WidgetTester tester) async {
    final fake = FakeAuthProvider();
    runApp(app.MyApp(createAuthProvider: () => fake));
    // Let splash navigate to login
    await tester.pump(const Duration(milliseconds: 3100));
    await tester.pumpAndSettle();
    expect(find.byType(MaterialApp), findsOneWidget);

    // Fill in login and submit
    await tester.enterText(find.byKey(const Key('emailField')), 'test@example.com');
    await tester.enterText(find.byKey(const Key('passwordField')), 'password123');
    await tester.tap(find.byKey(const Key('authSubmitButton')));
    await tester.pumpAndSettle();
    expect(find.text('Dashboard'), findsOneWidget);
  });
}
