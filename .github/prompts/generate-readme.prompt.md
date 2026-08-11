---
name: generate-readme
description: プロジェクトのREADME.mdを自動生成するためのプロンプト
tools: [vscode, execute, read, agent, ms-python.python/getPythonEnvironmentInfo, ms-python.python/getPythonExecutableCommand, ms-python.python/installPythonPackage, ms-python.python/configurePythonEnvironment, edit, search, web, browser, todo]
---

# ユーザープロンプト: Pythonプロジェクト用 README.md 自動作成指示

以下の指示に従って、本リポジトリの構成や設定ファイルを解析し、モダンで分かりやすい `README.md` を作成（または更新）してください。

---

## 🎯 目的
`uv` や `Ruff` を導入した Python プロジェクト（またはスターターテンプレート）の利用方法・開発手順・ディレクトリ構成・作者情報をまとめた `README.md` を作成する。

---

## 🔍 事前調査ステップ
コードや文書を出力する前に、まずプロジェクト環境の以下を確認してください。

1. **設定ファイル・ディレクトリ構造の解析**:
   - `pyproject.toml`（プロジェクト名、説明、Pythonバージョン、依存関係、Ruff/pytest設定など）
   - `.vscode/` や `.github/`（エディタ連携、Copilot指示書の有無）
   - `tests/` や `src/` の構造
2. **プロジェクト作成者（Author）の取得**:
   - `git config user.name` を実行し、取得されたユーザー名をプロジェクト作成者名として使用すること。

---

## 📝 `README.md` の構成案

以下の構造に従って Markdown を生成してください。

1. **タイトル & 概要**
   - プロジェクトの概要と主な特徴（例: `uv` による高速環境管理、`Ruff` によるコード整形、`pytest` 導入済など）を箇条書きで記載。
2. **🛠️ 技術スタック**
   - 使用している Python バージョン、主要ツール（`uv`, `Ruff`, `pytest` など）へのリンク付きリスト。
3. **📋 使い方 (Usage)**
   - テンプレートを利用した場合の初期設定（`pyproject.toml` 内の `name` や `description` などのプレースホルダー書き換え指示）。
   - 環境構築コマンド（`uv sync`）。
4. **💻 開発用コマンド**
   - パッケージの追加・削除 (`uv add`, `uv add --dev`, `uv remove`)
   - コードフォーマット & リンター (`uv run ruff format .`, `uv run ruff check .`, `uv run ruff check --fix .`)
   - テスト実行 (`uv run pytest`)
5. **📂 ディレクトリ構成**
   - リポジトリの主要ファイル・フォルダ構造を `text` のコードブロックツリーで表現（各要素に補足コメントを添える）。
6. **👤 Author**
   - **プロジェクト作成者**: `git config user.name` で取得したユーザー名
   - **README 作成**: 実行しているAIのモデル名（例: `Gemini 3.6 Flash`）

---

## 🎨 出力スタイル要件
- 絵文字を適度に使用し、視認性の高い見出しデザインにする。
- サンプルコードやコマンドは適切な言語ハイライト (`bash`, `toml`, `text`) のコードブロックで囲む。
