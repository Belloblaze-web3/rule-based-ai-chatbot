from datetime import datetime
import unittest

from rule_based_ai_chatbot import RuleBasedChatbot, normalize_text
from rule_based_ai_chatbot.cli import run_chat


class NormalizeTextTests(unittest.TestCase):
    def test_lowercases_trims_and_collapses_whitespace(self):
        self.assertEqual(normalize_text("  HELLO,   there!!  "), "hello there")


class RuleBasedChatbotTests(unittest.TestCase):
    def setUp(self):
        fixed_now = datetime(2026, 10, 15, 18, 12, 8)
        self.bot = RuleBasedChatbot(now_provider=lambda: fixed_now)

    def test_greeting_is_case_and_punctuation_insensitive(self):
        reply = self.bot.respond("  GOOD MORNING!!! ")
        self.assertEqual(reply.intent, "greeting")
        self.assertIn("Hello", reply.text)
        self.assertFalse(reply.should_exit)

    def test_phrase_matching_does_not_match_inside_other_words(self):
        reply = self.bot.respond("This is a test")
        self.assertEqual(reply.intent, "fallback")

    def test_help_and_identity(self):
        self.assertEqual(self.bot.respond("help").intent, "help")
        self.assertEqual(self.bot.respond("Who are you?").intent, "identity")

    def test_joke_and_thanks(self):
        self.assertEqual(self.bot.respond("Tell me a joke").intent, "joke")
        self.assertEqual(self.bot.respond("Thank you!").intent, "thanks")

    def test_time_and_date_use_injected_clock(self):
        time_reply = self.bot.respond("What time is it?")
        date_reply = self.bot.respond("today's date")
        self.assertEqual(time_reply.intent, "time")
        self.assertIn("18:12:08", time_reply.text)
        self.assertEqual(date_reply.intent, "date")
        self.assertIn("October 15, 2026", date_reply.text)

    def test_unknown_and_empty_inputs_use_fallback(self):
        self.assertEqual(self.bot.respond("Can you fly a spaceship?").intent, "fallback")
        self.assertEqual(self.bot.respond("   ").intent, "fallback")

    def test_exit_commands_are_complete_commands(self):
        for command in ("bye", "goodbye", "exit", "quit", "stop", "see you"):
            with self.subTest(command=command):
                reply = self.bot.respond(command.upper() + "!")
                self.assertEqual(reply.intent, "farewell")
                self.assertTrue(reply.should_exit)

        # Mentioning an exit word in a sentence is not an exit command.
        self.assertFalse(self.bot.respond("please stop by later").should_exit)


class ChatLoopTests(unittest.TestCase):
    def test_continues_until_exit_command(self):
        messages = iter(["hello", "what time is it", "quit"])
        prompts = []
        output = []

        def fake_input(prompt):
            prompts.append(prompt)
            return next(messages)

        run_chat(input_fn=fake_input, output_fn=output.append,
                 chatbot=RuleBasedChatbot(now_provider=lambda: datetime(2026, 1, 2, 3, 4, 5)))

        self.assertEqual(len(prompts), 3)
        self.assertTrue(any("Hello! How can I help" in line for line in output))
        self.assertTrue(any("03:04:05" in line for line in output))
        self.assertTrue(any("Goodbye!" in line for line in output))

    def test_end_of_input_exits_gracefully(self):
        output = []

        def eof_input(_prompt):
            raise EOFError

        run_chat(input_fn=eof_input, output_fn=output.append)
        self.assertTrue(any("Input stream closed" in line for line in output))

    def test_keyboard_interrupt_exits_gracefully(self):
        output = []

        def interrupted_input(_prompt):
            raise KeyboardInterrupt

        run_chat(input_fn=interrupted_input, output_fn=output.append)
        self.assertTrue(any("Chat interrupted" in line for line in output))


if __name__ == "__main__":
    unittest.main()
