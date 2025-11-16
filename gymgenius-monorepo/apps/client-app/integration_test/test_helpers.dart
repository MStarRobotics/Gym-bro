import 'dart:io';
import 'package:flutter/widgets.dart';
import 'package:integration_test/integration_test.dart';

Future<void> runTestWithScreenshots(String name, Future<void> Function() body) async {
  final binding = IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  try {
    await body();
  } catch (e) {
    try {
      final bytes = await binding.takeScreenshot(name);
      final dir = Directory('/tmp/integration-logs')..createSync(recursive: true);
      final file = File('${dir.path}/$name.png');
      await file.writeAsBytes(bytes);
    } catch (inner) {
      // ignore screenshot failure
    }
    rethrow;
  }
}
