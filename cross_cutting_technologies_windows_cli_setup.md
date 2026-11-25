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

Откройте новый терминал, запустите Codex и войдите через ChatGPT:

```powershell
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

Откройте новое окно Terminal, запустите Codex и войдите через ChatGPT:

```bash
codex
```

## AI-инструменты бизнес-аналитика

В соседнем курсе «Управление данными предприятия» есть [обзор AI-инструментов аналитика](https://fa-un.github.io/edm/ai_analyst_tools.html): там показано, как проверять выводы AI по источнику и использовать инструменты для перехода от интервью к проверяемому требованию.

## Официальные инструкции

- [Установка PowerShell 7 в Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows)
- [Установка Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Поддержка платформ Hermes](https://hermes-agent.nousresearch.com/docs/getting-started/platform-support)
- [Codex CLI: быстрый старт](https://learn.chatgpt.com/docs/codex/cli)

## Проверка установки

В новом окне PowerShell или Terminal проверьте, что обе команды доступны и выводят версии:

```text
codex --version
hermes --version
```
