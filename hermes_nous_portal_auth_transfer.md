# Перенос авторизации Hermes в Nous Portal

[← Основная инструкция установки](cross_cutting_technologies_windows_cli_setup.md)

Nous Portal использует OAuth refresh-токен, а не API-ключ. Hermes хранит его в `~/.hermes/auth.json`; файл содержит секреты и может включать авторизации других провайдеров. Передавайте его только между своими компьютерами и не помещайте в Git, сообщения или командную историю.

## Перенос существующего входа

Команды выполняйте от Linux-пользователя, под которым запускаются Hermes и его gateway.

1. Остановите Hermes и gateway на исходном компьютере. Один Nous refresh-токен нельзя безопасно использовать на двух машинах: при обновлении токена старое значение становится недействительным.
2. На исходном компьютере выполните `hermes status`: он показывает названия провайдеров, но не значения токенов. Копируйте файл целиком только если используется лишь Nous-вход. Если есть другие авторизации или вы не уверены, войдите отдельно на сервере командой `hermes auth add nous --type oauth`.
3. На сервере создайте закрытый каталог и убедитесь, что `~/.hermes/auth.json` ещё не существует; затем с Mac скопируйте файл:

   ```bash
   # На сервере
   install -d -m 700 ~/.hermes
   test ! -e ~/.hermes/auth.json || { echo 'auth.json уже существует; остановитесь и используйте отдельный вход'; exit 1; }

   # На Mac
   scp ~/.hermes/auth.json USER@SERVER:~/.hermes/auth.json
   ```

4. На сервере ограничьте права и проверьте вход, не выводя содержимое файла:

   ```bash
   chmod 700 ~/.hermes
   chmod 600 ~/.hermes/auth.json
   hermes portal info
   ```

   Ожидается `Auth: logged in`. Только после проверки включайте Hermes на сервере. Если после переноса Hermes сообщает об истёкшем или недействительном входе, авторизуйтесь на сервере заново: `hermes auth add nous --type oauth`.

## Особенности профилей и архивов

- Обычные именованные профили Hermes используют вход Nous из корневого `~/.hermes/auth.json`. Для отдельного входа в профиле выполните `hermes -p ИМЯ_ПРОФИЛЯ auth add nous --type oauth`; не копируйте общий refresh-токен в две независимые установки.
- Если `auth.json` содержит другие входы, копирование перенесёт их тоже. Для переноса только Nous-входа безопаснее пройти OAuth на сервере командой выше.
- `hermes profile export` намеренно исключает авторизации. `hermes backup` переносит всё Hermes-хранилище — профили, историю, настройки и секреты; не используйте полный архив только ради Nous-входа.

## Официальная документация

- [Nous Portal: место хранения и обновление токена](https://hermes-agent.nousresearch.com/docs/integrations/nous-portal)
- [Вход в Portal на сервере через SSH или device code](https://hermes-agent.nousresearch.com/docs/guides/run-hermes-with-nous-portal)
- [Профили Hermes и общая OAuth-авторизация](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Экспорт профиля и полный backup](https://hermes-agent.nousresearch.com/docs/user-guide/backup-and-transfer)
- [Исходник Hermes: refresh-токен Nous является одноразовым](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/auth_oauth_grants.py#L1830-L1841)
