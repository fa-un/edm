# Hermes Agent и Codex CLI: Windows, macOS и Linux-сервер

[← Страница дисциплины](cross_cutting_technologies.html) · [Индекс материалов](cross_cutting_technologies_materials.html)

## 1. Установка

### Windows

Откройте PowerShell или Windows Terminal.

**Hermes Desktop:** [скачайте установщик Hermes-Setup.exe](https://hermes-assets.nousresearch.com/Hermes-Setup.exe?build=b4db4842723a).

**Hermes CLI:**

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

**Codex CLI:**

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

### macOS

В Terminal установите Hermes и Codex CLI:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

После установки откройте новое окно терминала.

### Linux-сервер

Ниже — проверенный вариант для Ubuntu/Debian-сервера. Устанавливайте CLI и авторизуйте их от того пользователя Linux, под которым будут храниться профиль и проект.

1. Установите системные инструменты и CLI:

   ```bash
   sudo apt-get update
   sudo apt-get install -y ca-certificates curl git tmux
   curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
   npm install -g @openai/codex@latest
   ```

   Установщик Hermes подготавливает необходимые для него компоненты. Для Codex CLI нужен Node.js с npm. Откройте новый SSH-сеанс, затем проверьте `hermes --version` и `codex --version`.

2. Получите доступ к репозиторию курса и войдите в Codex под своей учётной записью:

   ```bash
   mkdir -p ~/tools
   git clone https://github.com/fa-un/edm.git ~/tools/edm
   codex login
   codex login status
   ```

   Не копируйте на сервер чужой `~/.codex/auth.json` и не вставляйте токены в командную строку. Авторизация должна принадлежать пользователю сервера; не публикуйте её в Git и не добавляйте в скрипты.

3. Создайте отдельный профиль курса и выберите модель:

   ```bash
   hermes profile create edm
   edm config set terminal.cwd ~/tools/edm
   edm model
   ```

   В мастере выберите **OpenAI → ChatGPT or Codex Subscription** и подтвердите импорт своей текущей авторизации Codex. Затем выберите **`gpt-6-luna`**. Hermes сохраняет импортированную авторизацию для своего профиля отдельно, поэтому последующее обновление токена Codex может потребовать повторного импорта. Настройте рабочий каталог профиля на `~/tools/edm` (`terminal.cwd`) и проверьте запуск командой `cd ~/tools/edm && edm`; Hermes должен прочитать файл проекта, например `cross_cutting_technologies_windows_cli_setup.md`.

4. Если нужен Telegram-бот, запустите мастер из профиля:

   ```bash
   edm gateway setup
   ```

   Введите токен в скрытый запрос мастера и задайте список разрешённых числовых Telegram ID. Не оставляйте список пустым: это откроет бота всем пользователям. Файл `~/.hermes/profiles/edm/.env` содержит секреты; оставьте доступ только владельцу:

   ```bash
   chmod 600 ~/.hermes/profiles/edm/.env
   ```

5. Для автоматического запуска после перезагрузки установите системную службу Hermes от выделенного пользователя Linux:

   ```bash
   sudo hermes gateway install --system --run-as-user "$USER" --start-now
   systemctl status hermes-gateway
   hermes gateway list
   ```

   На сервере работает один общий gateway Hermes; он обслуживает настроенные профили. Не запускайте отдельный экземпляр gateway с тем же Telegram-токеном. Служба должна быть `active (running)`, а профиль `edm` — отображаться в списке. Для отдельного профиля используйте созданную команду `edm`, не запускайте команды Telegram из другого профиля.

6. Перед перезагрузкой убедитесь, что SSH-доступ сохранён и нужные службы включены. После перезагрузки проверьте:

   ```bash
   systemctl is-enabled hermes-gateway
   systemctl is-active hermes-gateway
   docker ps
   ```

   `docker ps` должен показывать ожидаемые контейнеры почтового сервера, если на машине установлен Mailcow. Не удаляйте Mailcow volumes и не выполняйте очистку Docker, чтобы освободить место для Hermes. Проверьте ответ бота в личном чате и запуск `edm` из `~/tools/edm`.

   При проверенной установке этого курса Codex CLI работал через импорт авторизации подписки ChatGPT, Hermes использовал `gpt-6-luna`, а профиль `edm` читал Markdown-файл из клонированного репозитория. Telegram-бот запускался через systemd gateway; Mailcow оставался в своих Docker-контейнерах. Это описание конфигурации одной установки, а не гарантия поведения на другом сервере.

### Перенос входа Nous Portal на сервер

`~/.hermes/auth.json` содержит OAuth-токен, не API-ключ. Копируйте его через `scp` только если в файле нет других авторизаций и на сервере ещё нет `auth.json`; затем задайте права `600` и проверьте `hermes portal info`. Остановите Hermes на исходной машине: один refresh-токен нельзя безопасно использовать на двух машинах одновременно. Иначе войдите на сервере командой `hermes auth add nous --type oauth`. [Подробности](hermes_nous_portal_auth_transfer.md).

## 2. Первый запуск Hermes

Выполните `codex login` и войдите под собственной учётной записью. При файловом хранении Codex сохраняет авторизацию в `%USERPROFILE%\.codex\auth.json` в Windows или `~/.codex/auth.json` в macOS. Не устанавливайте и не пересылайте `auth.json`, полученный от другого человека: в нём могут быть действующие токены доступа.

1. Запустите мастер выбора модели:

   ```text
   hermes model
   ```

2. Выберите **OpenAI → ChatGPT or Codex Subscription** и подтвердите импорт авторизации Codex, если Hermes предложит его.
3. Переключите модель на **`gpt-6-luna` (GPT-6 Luna)**. Для этой инструкции Luna обязательна. По наблюдению преподавателя, на типовых заданиях курса она расходует лимит примерно в 10 раз медленнее; фактический расход зависит от задачи, контекста, режима скорости и тарифа.
4. Проверьте провайдера, модель и вход:

   ```text
   hermes config get model.provider
   hermes config get model.default
   hermes auth status openai-codex
   ```

   Ожидаются `openai-codex`, `gpt-6-luna` и `logged in`. Запустите `hermes` и отправьте `ping`.

Если Luna нет в списке, остановитесь и обратитесь к преподавателю или администратору доступа.

## 3. Проверка Codex и лимитов

Проверьте установку:

```text
codex --version
hermes --version
```

Чтобы посмотреть лимиты, введите `/status` в чате Codex Desktop или в интерактивном сеансе Codex CLI.

## Официальные инструкции

- [Установка Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Codex CLI: быстрый старт](https://learn.chatgpt.com/docs/codex/cli)
- [Авторизация и хранение токенов Codex](https://learn.chatgpt.com/docs/auth?surface=cli)
- [Модели Codex](https://learn.chatgpt.com/docs/models)
- [Лимиты Codex](https://learn.chatgpt.com/docs/pricing)
- [Hermes: профили и запуск gateway](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways)
- [Hermes: настройка Telegram и ограничения доступа](https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram)
