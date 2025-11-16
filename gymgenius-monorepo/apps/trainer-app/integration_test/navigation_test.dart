import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'test_helpers.dart';
import 'package:trainer_app/main.dart' as app;
import 'package:trainer_app/testing/fake_auth_provider.dart';
import 'package:flutter/material.dart';
import 'package:trainer_app/screens/client_management_screen.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('Splash is shown and Client Management screen renders', (WidgetTester tester) async {
    await runTestWithScreenshots('trainer-clientmanagement', () async {
    final fake = FakeAuthProvider();
    runApp(app.TrainerApp(createAuthProvider: () => fake));
    await tester.pumpAndSettle();

    expect(find.text('GymGenius Trainer'), findsOneWidget);

    // Directly pump the ClientManagementScreen (simulate navigation)
    await tester.pumpWidget(const MaterialApp(home: ClientManagementScreen()));
    await tester.pumpAndSettle();
    expect(find.byKey(const Key('clientManagementScreen')), findsOneWidget);
    });
}
