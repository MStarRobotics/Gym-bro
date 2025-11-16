import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:client_app/main.dart' as app;
import 'package:client_app/testing/fake_auth_provider.dart';
import 'test_helpers.dart';
import 'package:flutter/material.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Login and Navigation Tests', () {
    testWidgets('Sign-up flow navigates to home and shows dashboard', (WidgetTester tester) async {
      await runTestWithScreenshots('client-signup', () async {
      final fake = FakeAuthProvider();
      runApp(app.MyApp(createAuthProvider: () => fake));
      await tester.pump(const Duration(milliseconds: 3100));
      await tester.pumpAndSettle();

      // Toggle sign-up
      expect(find.text('Sign Up'), findsWidgets);
      await tester.tap(find.byKey(const Key('toggleAuthModeButton')));
      await tester.pumpAndSettle();

      // Fill sign-up form: Full name, Email, Password
      await tester.enterText(find.byKey(const Key('fullNameField')), 'Test User');
      await tester.enterText(find.byKey(const Key('emailField')), 'test@example.com');
      await tester.enterText(find.byKey(const Key('passwordField')), 'password123');
      await tester.pumpAndSettle();

      await tester.tap(find.byKey(const Key('authSubmitButton')));
      await tester.pumpAndSettle();

      // After sign-up, we should be on home screen with Dashboard
      expect(find.text('Dashboard'), findsOneWidget);
      });

    testWidgets('Login flow navigates to home and bottom nav works', (WidgetTester tester) async {
      await runTestWithScreenshots('client-login', () async {
      final fake = FakeAuthProvider();
      runApp(app.MyApp(createAuthProvider: () => fake));
      await tester.pump(const Duration(milliseconds: 3100));
      await tester.pumpAndSettle();

      // Email and Password fields, then login
      await tester.enterText(find.byKey(const Key('emailField')), 'test@example.com');
      await tester.enterText(find.byKey(const Key('passwordField')), 'password123');
      await tester.pumpAndSettle();

      await tester.tap(find.byKey(const Key('authSubmitButton')));
      await tester.pumpAndSettle();

      expect(find.text('Dashboard'), findsOneWidget);

      // Tap into other tabs and assert content
      await tester.tap(find.byKey(const Key('tab_workouts')));
      await tester.pumpAndSettle();
      expect(find.byKey(const Key('workoutScreen')), findsOneWidget);

      await tester.tap(find.byKey(const Key('tab_meals')));
      await tester.pumpAndSettle();
      expect(find.byKey(const Key('nutritionScreen')), findsOneWidget);

      await tester.tap(find.byKey(const Key('tab_chat')));
      await tester.pumpAndSettle();
      expect(find.byKey(const Key('chatScreen')), findsOneWidget);
      });

    testWidgets('Sample workouts, meal plan and chat interactions (if implemented)', (WidgetTester tester) async {
      await runTestWithScreenshots('client-e2e-extensions', () async {
        final fake = FakeAuthProvider();
        runApp(app.MyApp(createAuthProvider: () => fake));
        await tester.pump(const Duration(milliseconds: 3100));
        await tester.pumpAndSettle();

        // Login quickly to reach home
        await tester.enterText(find.byKey(const Key('emailField')), 'test@example.com');
        await tester.enterText(find.byKey(const Key('passwordField')), 'password123');
        await tester.tap(find.byKey(const Key('authSubmitButton')));
        await tester.pumpAndSettle();

        // Workout - try to open create workflow if exists
        await tester.tap(find.byKey(const Key('tab_workouts')));
        await tester.pumpAndSettle();
        if (find.byKey(const Key('createWorkoutButton')).evaluate().isNotEmpty) {
          await tester.tap(find.byKey(const Key('createWorkoutButton')));
          await tester.pumpAndSettle();
          // Fill and submit workout form if visible
          if (find.byKey(const Key('workoutNameField')).evaluate().isNotEmpty) {
            await tester.enterText(find.byKey(const Key('workoutNameField')), 'Morning Routine');
            await tester.tap(find.byKey(const Key('saveWorkoutButton')));
            await tester.pumpAndSettle();
          }
          // assert that the created text shows
          expect(find.byKey(const Key('workoutCreatedText')), findsOneWidget);
        }

        // Meals - try to fetch meal plan if button exists
        await tester.tap(find.byKey(const Key('tab_meals')));
        await tester.pumpAndSettle();
        if (find.byKey(const Key('fetchMealPlanButton')).evaluate().isNotEmpty) {
          await tester.tap(find.byKey(const Key('fetchMealPlanButton')));
          await tester.pumpAndSettle();
          expect(find.byKey(const Key('mealPlanText')), findsOneWidget);
        }

        // Chat - try to send a message if chat input exists
        await tester.tap(find.byKey(const Key('tab_chat')));
        await tester.pumpAndSettle();
        if (find.byKey(const Key('chatInput')).evaluate().isNotEmpty) {
          await tester.enterText(find.byKey(const Key('chatInput')), 'Hello, coach');
          await tester.tap(find.byKey(const Key('sendChatButton')));
          await tester.pumpAndSettle();
          expect(find.text('Hello, coach'), findsOneWidget);
        }
      });
    });
  });
}
