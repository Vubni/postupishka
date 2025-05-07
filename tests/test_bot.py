
# # Используйте библиотеку pytest-telegram для моков
# def test_start_command(bot):
#     message = MockMessage(text="/start")
#     response = bot.handle_message(message)
#     assert "Добро пожаловать!" in response.text
    
# from unittest.mock import patch

# @patch("telegram.Bot.send_message")
# def test_send_welcome(mock_send_message):
#     send_welcome(123, "Hello")
#     mock_send_message.assert_called_with(chat_id=123, text="Hello")
    
# def test_payment_flow(bot):
#     # Симулируем оплату
#     bot.handle_message(MockMessage(text="/pay"))
#     # Проверяем ответ и статус
#     assert bot.payment_status == "success"