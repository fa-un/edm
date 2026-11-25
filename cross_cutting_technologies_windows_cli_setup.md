# PowerShell, Hermes Agent и Codex CLI в Windows

[← Страница дисциплины](cross_cutting_technologies.html) · [Индекс материалов](cross_cutting_technologies_materials.html)

## 1. Откройте PowerShell

В Windows обычно уже установлен **Windows PowerShell**. Откройте меню «Пуск» и найдите PowerShell или Windows Terminal.

Чтобы установить современный **PowerShell 7**, выполните эту команду в Windows PowerShell, командной строке или Terminal:

```powershell
winget install --id Microsoft.PowerShell --source winget
```

Затем откройте **PowerShell 7** из меню «Пуск».

## 2. Установите Hermes Agent

В PowerShell запустите официальный установщик:

```powershell
iex (irm https://hermes-agent.nousresearch.com/install.ps1)
```

Откройте новый терминал и запустите Hermes. При первом запуске следуйте настройке модели и провайдера:

```powershell
hermes
```

Позже выбрать или изменить модель можно командой `hermes model`.

## 3. Установите Codex CLI

В PowerShell запустите официальный установщик:

```powershell
powershell -ExecutionPolicy Bypass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

Откройте новый терминал, запустите Codex и войдите через ChatGPT:

```powershell
codex
```

## AI-инструменты бизнес-аналитика

В соседнем курсе «Управление данными предприятия» есть [обзор AI-инструментов аналитика](https://fa-un.github.io/edm/ai_analyst_tools.html): там показано, как проверять выводы AI по источнику и использовать инструменты для перехода от интервью к проверяемому требованию.

## Официальные инструкции

- [Установка PowerShell 7 в Windows](https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows)
- [Установка Hermes Agent](https://hermes-agent.nousresearch.com/docs/getting-started/installation)
- [Codex CLI: быстрый старт](https://github.com/openai/codex#quickstart)
