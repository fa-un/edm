# Hermes Agent и Codex CLI: Windows и macOS

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
