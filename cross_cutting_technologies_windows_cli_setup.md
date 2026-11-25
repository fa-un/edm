# PowerShell, Hermes Agent и Codex CLI: Windows и macOS

[← Страница дисциплины](cross_cutting_technologies.html) · [Индекс материалов](cross_cutting_technologies_materials.html)

## Windows

### 1. Откройте PowerShell

Откройте **Windows PowerShell** из меню «Пуск» или **Windows Terminal**. PowerShell 7 для этих команд устанавливать необязательно; если хотите использовать его, выполните:

```powershell
winget install --id Microsoft.PowerShell --source winget
```

После установки PowerShell 7 откройте его из меню «Пуск».

### 2. Установите Hermes Agent

Чтобы установить Hermes Desktop для Windows, скачайте [установщик Hermes-Setup.exe](https://hermes-assets.nousresearch.com/Hermes-Setup.exe?build=b4db4842723a).

В PowerShell запустите официальный установщик:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Откройте новое окно PowerShell, чтобы обновить PATH. Если установщик не запустил мастер или настройка не завершилась, выполните `hermes setup`. Затем запустите Hermes:

```powershell
hermes
```

Позже выбрать или изменить модель можно командой `hermes model`.

### 3. Установите Codex CLI

В PowerShell запустите официальный установщик:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Откройте новый терминал и войдите в Codex под своей учётной записью:

```powershell
codex login
codex
```

## macOS

Откройте приложение **Terminal** через Launchpad или папку «Программы → Утилиты».

### 1. Установите Hermes Agent

В Terminal запустите официальный установщик CLI:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

Откройте новое окно Terminal, чтобы обновить PATH. Если установщик не запустил мастер или настройка не завершилась, выполните `hermes setup`. Затем запустите агента:

```bash
hermes
```

На используемом Intel Mac работают и Hermes CLI, и Desktop. При этом Nous не включает Intel macOS в список поддерживаемых платформ, а официальные macOS Desktop-сборки заявлены для Apple Silicon. Поэтому этот опыт подтверждает работу на конкретном Mac, но не гарантирует её на всех Intel Mac.

### 2. Установите Codex CLI

В Terminal запустите официальный установщик:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

Откройте новое окно Terminal и войдите в Codex под своей учётной записью:

```bash
codex login
codex
```

## AI-инструменты бизнес-аналитика

В соседнем курсе «Управление данными предприятия» есть [обзор AI-инструментов аналитика](https://fa-un.github.io/edm/ai_analyst_tools.html): там показано, как проверять выводы AI по источнику и использовать инструменты для перехода от интервью к проверяемому требованию.

## Официальные инструкции

- [Установка PowerShell 7 в Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows)
- [Установка Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Поддержка платформ Hermes](https://hermes-agent.nousresearch.com/docs/getting-started/platform-support)
- [Codex CLI: быстрый старт](https://learn.chatgpt.com/docs/codex/cli)
- [Модели и доступность Codex](https://learn.chatgpt.com/docs/models)
- [Авторизация Codex и хранение токенов](https://learn.chatgpt.com/docs/auth?surface=cli)
- [Слеш-команды Codex, включая `/status`](https://learn.chatgpt.com/docs/reference/slash-commands)
- [Лимиты и расход Codex](https://learn.chatgpt.com/docs/pricing)

## Проверка установки

В новом окне PowerShell или Terminal проверьте, что обе команды доступны и выводят версии:

```text
codex --version
hermes --version
```

## Авторизация Codex и файл `auth.json`

После `codex login` Codex сохраняет авторизацию локально. Не устанавливайте файл `auth.json`, полученный от другого человека: он может содержать действующие токены доступа. При файловом хранении путь — `%USERPROFILE%\.codex\auth.json` в Windows и `~/.codex/auth.json` в macOS; если выбрано системное хранилище учётных данных, отдельного файла может не быть.

## Подключение существующей авторизации Codex к Hermes

Если Codex CLI уже вошёл в нужную учётную запись, Hermes может импортировать эту авторизацию без нового входа через браузер:

1. Убедитесь, что Codex CLI вошёл именно в нужную учётную запись. Не открывайте и не отправляйте содержимое `auth.json`.
2. В Terminal или PowerShell запустите мастер выбора модели:

   ```text
   hermes model
   ```

3. Выберите **OpenAI**, затем **ChatGPT or Codex Subscription**.
4. Если Hermes предложит импортировать найденные учётные данные Codex из `auth.json`, подтвердите импорт (`y`). Если в Hermes уже сохранён другой вход, проверьте, что выбираете импорт текущей учётной записи Codex.
5. Переключите модель на `gpt-6-luna` (GPT-6 Luna). Для этой инструкции выбор Luna обязателен: по наблюдению преподавателя, на типовых заданиях курса она расходует лимит примерно в 10 раз медленнее. Фактический расход зависит от задачи, объёма контекста, режима скорости и тарифа. Если Luna нет в списке, остановитесь и обратитесь к преподавателю или администратору доступа: доступность зависит от тарифа и настроек рабочего пространства.

Hermes ищет `auth.json` в каталоге `CODEX_HOME`, если эта переменная задана (`%CODEX_HOME%\auth.json` в Windows, `$CODEX_HOME/auth.json` в macOS), иначе — в `%USERPROFILE%\.codex\auth.json` в Windows или `~/.codex/auth.json` в macOS. В файле должны быть действующие токен доступа и токен обновления. Если предложения импорта нет или файл не найден, остановитесь и проверьте путь и способ хранения входа Codex. При системном хранилище учётных данных этот способ может быть недоступен; без явного запроса владельца не начинайте новую OAuth-авторизацию.

Для импорта через мастер не нужно менять `auth.adopt_external_logins`: эта настройка отвечает за автоматическое восстановление входа после ошибки обновления токена.

Проверьте, какой провайдер и модель выбраны в Hermes, и что авторизация сохранена:

```text
hermes config get model.provider
hermes config get model.default
hermes auth status openai-codex
```

Ожидаемые значения — `openai-codex`, выбранная модель и `logged in`. Затем откройте Hermes, отправьте `ping` и убедитесь, что получен ответ. Статус входа проверяет наличие сохранённых учётных данных, а успешный ответ — работу запроса. Ответ самой модели с названием модели не подтверждает провайдера; сверяйте также настройки Hermes.

Hermes сохраняет импортированные учётные данные у себя. Codex CLI и Hermes используют скопированную пару токенов; если одно приложение обновит refresh-токен, вход в другом может потребовать повторного восстановления. Не публикуйте `auth.json`, не вставляйте его содержимое в чат и не добавляйте файл в репозиторий.

Подробности: [официальная документация Hermes о провайдерах](https://hermes-agent.nousresearch.com/docs/integrations/providers), [документация о хранилище учётных данных](https://hermes-agent.nousresearch.com/docs/user-guide/features/credential-pools), [код импорта Codex CLI в Hermes](https://github.com/NousResearch/hermes-agent/blob/8fc0374447313e276f6b9a2764bfc750190c966a/hermes_cli/auth_codex.py#L587-L610).

## Просмотр лимитов Codex

- **Codex Desktop:** в поле ввода сообщения наберите `/status` и отправьте команду. В ответе отображаются использование контекста и текущие лимиты.
- **Codex CLI:** запустите `codex`, затем в интерактивном терминале наберите `/status`. Команда показывает состояние текущего сеанса, использование контекста и доступные лимиты.

`/status` показывает текущее состояние; лимиты и способы входа зависят от учётной записи и выбранного способа авторизации.
