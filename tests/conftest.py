import sys
from pathlib import Path

# プロジェクトルートのパスを取得
root_dir = Path(__file__).parent

# PYTHONPATHにbackendディレクトリを追加
sys.path.insert(0, str(root_dir))
