import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:trainer_app/main.dart' as app;
import 'package:trainer_app/testing/fake_auth_provider.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  testWidgets('App launches and shows MaterialApp', (WidgetTester tester) async {
    final fake = FakeAuthProvider();
    runApp(app.TrainerApp(createAuthProvider: () => fake));
    await tester.pumpAndSettle();
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
