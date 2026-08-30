# VLM BBox Annotator (`vlm-bbox-annotator`)

Vision-Language Model (VLM) を活用して、画像内の物体検出用バウンディングボックス（BBox）のアノテーション作業を自動・半自動で補助するツールです。  
Google Gemini やローカル環境の Ollama に対応し、検出結果を標準的な Pascal VOC 形式（XML）で出力します。

---

## 🚀 主な特徴

- 🎯 **VLM による BBox アノテーション補助**: クラス名と説明文をもとに対象物を自動検出し、正規化座標のバウンディングボックスを生成
- 🔄 **マルチモデル対応**: Google Gemini（API経由）および Ollama（ローカル環境）の VLM を切り替え可能
- 📄 **Pascal VOC 形式 (XML) 出力**: 物体検出データセットで広く用いられる Pascal VOC 形式に対応
- 📊 **アノテーション結果の可視化**: Matplotlib によるバウンディングボックスの描画・プレビュー機能
- ⚡ **高速なパッケージ管理**: `uv` による依存関係解決と仮想環境の即時構築
- 🧹 **コード品質の維持**: `Ruff` による高速なリント & コードフォーマット
- 🧪 **テスト自動化**: `pytest` によるテスト環境構築済み
- 🤖 **AI 支援開発**: VS Code 設定 & GitHub Copilot 開発ガイド (`.github/copilot-instructions.md`) 同梱

---

## 🛠️ 技術スタック

- **Language**: Python `>= 3.13`
- **Package Manager / Environment**: [uv](https://github.com/astral-sh/uv)
- **VLM / LLM Integration**: [LangChain](https://github.com/langchain-ai/langchain) ([langchain-google-genai](https://pypi.org/project/langchain-google-genai/), [langchain-ollama](https://pypi.org/project/langchain-ollama/))
- **Schema & Validation**: [Pydantic](https://docs.pydantic.dev/)
- **Image Processing & Visualization**: [Pillow](https://python-pillow.org/), [Matplotlib](https://matplotlib.org/)
- **Linter & Formatter**: [Ruff](https://github.com/astral-sh/ruff)
- **Testing**: [pytest](https://docs.pytest.org/)

---

## 📋 使い方 (Usage)

### 1. 環境構築

`uv` を使用して依存関係を同期し、仮想環境を自動生成します。

```bash
uv sync
```

### 2. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、使用するモデルや API キーを設定します。

```bash
cp .env.example .env
```

`.env` の設定例:

```env
# Gemini を利用する場合
MODEL_TYPE="Gemini"
MODEL_NAME="gemini-3.5-flash-lite"
GOOGLE_API_KEY="your_api_key_here"

# Ollama (ローカル VLM) を利用する場合
# MODEL_TYPE="Ollama"
# MODEL_NAME="hf.co/LiquidAI/LFM2.5-VL-3B-GGUF:BF16"
```

### 3. アノテーション対象クラスの定義

`classes_info.json` にアノテーション対象のクラス名と、VLM に渡す説明文（プロンプト用補足）を定義します。

```json
{
    "human": "画像内の人、人間",
    "car": "画像内の自動車",
    "bicycle": "画像内の自転車"
}
```

### 4. アノテーションの実行

アノテーション対象の画像（`.jpg`, `.png`, `.jpeg`, `.bmp`）を `data/` フォルダ（または任意のディレクトリ）に配置し、実行します。

```bash
# 基本実行 (デフォルトで ./data フォルダを処理)
uv run python main.py

# 検出結果の可視化プレビューを表示する場合
uv run python main.py --visualize

# 対象データディレクトリを指定する場合
uv run python main.py --data ./path/to/images --visualize
```

実行後、画像と同じディレクトリに Pascal VOC 形式の XML ファイル（例: `image_name.xml`）が出力されます。

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
│   ├── prompts/
│   │   └── generate-readme.prompt.md # README 自動生成用プロンプト
│   └── copilot-instructions.md       # Copilot 用の開発指示書
├── .vscode/
│   ├── extensions.json               # VS Code 推奨拡張機能
│   └── settings.json                 # VS Code 保存時自動フォーマット設定
├── data/                             # アノテーション対象の画像配置ディレクトリ
├── modules/                          # アノテーション処理モジュール群
│   ├── __init__.py
│   ├── annotator.py                  # VLM アノテーション補助クラス
│   ├── models.py                     # Pydantic スキーマ & LLM/VLM モデル初期化
│   ├── prompt.py                     # VLM 用プロンプト定義
│   ├── visualize.py                  # 検出結果の画像描画・可視化
│   └── voc_format.py                 # Pascal VOC 形式 (XML) の生成・保存
├── tests/                            # テストコード
│   ├── conftest.py                   # pytest 共通設定
│   └── test_visualize.py             # 描画機能のテスト
├── .env.example                      # 環境変数設定サンプル
├── .gitignore
├── .python-version                   # Python バージョン指定 (3.13)
├── classes_info.json                 # アノテーション対象クラスの定義ファイル
├── main.py                           # メイン実行エントリーポイント
├── pyproject.toml                    # プロジェクト定義 & Ruff / pytest 設定
├── README.md                         # 本ドキュメント
└── uv.lock                           # uv ロックファイル
```

---

## 👤 Author

- **プロジェクト作成者**: muetaek0321
- **README 作成**: Gemini 3.7 Flash
