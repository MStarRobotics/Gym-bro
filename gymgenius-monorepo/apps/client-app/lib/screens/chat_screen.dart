import 'package:flutter/material.dart';
import '../testing/test_mode.dart';

/// Chat Screen - AI-powered fitness coaching conversations
/// TODO: Implement feature logic here.
///
/// Required Features:
/// - Real-time chat interface with AI coach
/// - Message history with scroll-to-load-more
/// - Voice input support
/// - Quick action buttons (workout suggestions, meal plans, etc.)
/// - Contextual responses based on user's current plan and progress
class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final List<String> _messages = [];
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: const Key('chatScreen'),
      appBar: AppBar(title: const Text('AI Coach')),
      body: Column(
        children: [
          Expanded(
            child: ListView(
              children: _messages.map((m) => ListTile(title: Text(m))).toList(),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    key: const Key('chatInput'),
                    controller: _controller,
                    decoration: const InputDecoration(labelText: 'Message'),
                  ),
                ),
                if (isTestMode)
                  IconButton(
                    key: const Key('sendChatButton'),
                    onPressed: () {
                      final text = _controller.text.trim();
                      if (text.isNotEmpty) {
                        setState(() {
                          _messages.add(text);
                          _controller.clear();
                        });
                      }
                    },
                    icon: const Icon(Icons.send),
                  )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
