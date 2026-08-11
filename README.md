# VLM BBox Annotator (`vlm-bbox-annotator`)

Vision-Language Model (VLM) を活用して物体検出用バウンディングボックス（BBox）のアノテーション作業を補助するツールです。

## 🚀 特徴

- **高速なパッケージ管理**: `uv` による高速な依存関係解決とバーチャル環境管理
- **高速なリンター & フォーマッタ**: `Ruff` による統一されたコードスタイルと品質チェック
- **テスト自動化**: `pytest` 設定済み
- **VS Code 連携**: 保存時の Ruff 自動フォーマット & インポート整理が設定済み
- **GitHub Copilot 指示書**: AI 支援開発のためのガイドライン (`.github/copilot-instructions.md`) 同梱

## 🛠️ 技術スタック

- Python `>= 3.13`
- [uv](https://github.com/astral-sh/uv) (パッケージ・環境管理)
- [Ruff](https://github.com/astral-sh/ruff) (リンター / フォーマッタ)
- [pytest](https://docs.pytest.org/) (テストフレームワーク)

---

## 📋 使い方

### 1. テンプレートから新規プロジェクトを作成

このテンプレートからプロジェクトを作成したら、まず `pyproject.toml` 内のプレースホルダーを実際のプロジェクト情報に書き換えてください。

`pyproject.toml`:

```toml
[project]
name = "your-project-name"        # {{PROJECT_NAME}} を書き換え
version = "0.1.0"
description = "Your description"  # {{PROJECT_DESCRIPTION}} を書き換え
```

### 2. 環境構築

`uv` を使用して依存関係を同期し、仮想環境を自動生成します。

```bash
uv sync
```

---

## 💻 開発用コマンド

### パッケージの追加・削除

```bash
# 通常の依存関係を追加
uv add <package_name>

# 開発用依存関係を追加
uv add --dev <package_name>

# パッケージの削除
uv remove <package_name>
```

### リンター & フォーマッタ (Ruff)

```bash
# コードフォーマット
uv run ruff format .

# リンターチェック
uv run ruff check .

# リンターの自動修正
uv run ruff check --fix .
```

### テストの実行 (pytest)

```bash
uv run pytest
```

---

## 📂 ディレクトリ構成

```text
.
├── .github/
│   └── copilot-instructions.md  # Copilot用の開発指示書
├── .vscode/
│   ├── extensions.json          # VS Code 推奨拡張機能
│   └── settings.json            # VS Code 保存時自動フォーマット設定
├── tests/
│   └── conftest.py              # pytest 用共通設定
├── .gitignore
├── .python-version              # Python バージョン指定 (3.13)
├── pyproject.toml               # プロジェクト定義 & Ruff / pytest 設定
├── README.md                    # 本ドキュメント
└── uv.lock                      # uv ロックファイル
```

---

## 👤 Author

- **プロジェクト作成者**: muetaek0321
- **README 作成**: Gemini 3.6 Flash
