// Скопируйте этот файл в api/config.js и впишите значения.
// api/config.js не попадает в GitHub (он в .gitignore), но уходит в Vercel при `vercel deploy`.
export default {
  // Токен бота от @BotFather, вида 123456789:AAH...
  TELEGRAM_BOT_TOKEN: '',
  // ID чата или группы, куда бот пишет заявки. У групп ID отрицательный, минус сохранить.
  TELEGRAM_CHAT_ID: '',
  // Необязательно: токен для реестра eGov на странице проверки.
  YUME_API_TOKEN: '',
};
