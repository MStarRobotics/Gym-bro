import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:trainer_app/main.dart' as app;
import 'helpers/fake_auth_provider.dart';

void main() {
  testWidgets('TrainerApp builds with a fake auth provider', (WidgetTester tester) async {
    final fake = FakeAuthProvider();
    await tester.pumpWidget(app.TrainerApp(createAuthProvider: () => fake));
    await tester.pumpAndSettle();
    expect(find.byType(MaterialApp), findsOneWidget);
    expect(find.text('GymGenius Trainer'), findsOneWidget);
  });
}
