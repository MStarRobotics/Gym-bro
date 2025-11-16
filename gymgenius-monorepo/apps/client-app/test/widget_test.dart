import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:client_app/main.dart' as app;
import 'helpers/fake_auth_provider.dart';

void main() {
  testWidgets('MyApp loads and lets user login, navigates to Home', (WidgetTester tester) async {
    final fakeAuth = FakeAuthProvider();
    await tester.pumpWidget(app.MyApp(createAuthProvider: () => fakeAuth));
    // Let SplashScreen navigate to login
    await tester.pump(const Duration(milliseconds: 3100));
    await tester.pumpAndSettle();

    expect(find.byType(MaterialApp), findsOneWidget);
    expect(find.text('Welcome Back'), findsOneWidget);

    // Enter email and password
    await tester.enterText(find.byKey(const Key('emailField')), 'test@example.com');
    await tester.enterText(find.byKey(const Key('passwordField')), 'password123');
    await tester.pump();

    // Tap the login button
    await tester.tap(find.byKey(const Key('authSubmitButton')));
    await tester.pumpAndSettle();

    // The fake provider will simulate login success and navigation to home should occur
    expect(find.text('Dashboard'), findsOneWidget);
  });
}
