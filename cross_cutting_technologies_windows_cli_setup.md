# PowerShell, Hermes Agent и Codex CLI: Windows и macOS

[← Страница дисциплины](cross_cutting_technologies.html) · [Индекс материалов](cross_cutting_technologies_materials.html)

## Windows

### 1. Откройте PowerShell

В Windows обычно уже установлен **Windows PowerShell**. Откройте меню «Пуск» и найдите PowerShell или Windows Terminal.

Чтобы установить современный **PowerShell 7**, выполните эту команду в Windows PowerShell, командной строке или Terminal:

```powershell
winget install --id Microsoft.PowerShell --source winget
```

Затем откройте **PowerShell 7** из меню «Пуск».

### 2. Установите Hermes Agent

В PowerShell запустите официальный установщик:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Откройте новый терминал и запустите Hermes. При первом запуске следуйте настройке модели и провайдера:

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

Откройте новое окно Terminal, настройте провайдера, затем запустите агента:

```bash
hermes setup
hermes
```

Основной поддерживаемый вариант Hermes для macOS — Apple Silicon. На Intel Mac можно установить CLI; Desktop-пакет для Intel не выпускается.

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
