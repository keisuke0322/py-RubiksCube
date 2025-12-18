# ルービックキューブシミュレーター

Python で実装されたルービックキューブシミュレーターです。コマンドラインインターフェースを通じて、キューブの操作、スクランブル、自動ソルブなどの機能を利用できます。

## 機能

- 🎲 **キューブの可視化**: カラー表示による展開図形式での表示
- 🔄 **回転操作**: 標準的なキューブ記法（U, D, F, B, L, R）に対応
- 🎰 **スクランブル**: ランダムな手順でキューブをスクランブル
- 🧩 **自動ソルブ**: レイヤーバイレイヤー法による解法生成
- 📝 **操作履歴**: 全操作の履歴を記録・表示
- ↩️ **取り消し機能**: 直前の操作を取り消し

## インストール

```bash
git clone https://github.com/yourusername/py-RubiksCube.git
cd py-RubiksCube
```

## 使用方法

### CLI の起動

```bash
python -m src.cli
```

または

```bash
python src/cli.py
```

### コマンド一覧

| コマンド        | 説明                                       |
| --------------- | ------------------------------------------ |
| `U`, `U'`, `U2` | 上面を回転（時計回り、反時計回り、180 度） |
| `D`, `D'`, `D2` | 下面を回転                                 |
| `F`, `F'`, `F2` | 前面を回転                                 |
| `B`, `B'`, `B2` | 後面を回転                                 |
| `L`, `L'`, `L2` | 左面を回転                                 |
| `R`, `R'`, `R2` | 右面を回転                                 |
| `show`          | キューブを表示                             |
| `reset`         | キューブを初期状態にリセット               |
| `scramble [N]`  | N 手でスクランブル（デフォルト: 20 手）    |
| `solve`         | キューブを解く                             |
| `history`       | 操作履歴を表示                             |
| `undo`          | 最後の操作を取り消し                       |
| `help`          | ヘルプを表示                               |
| `quit`          | 終了                                       |

### 使用例

```
> scramble 15
スクランブル: R' B2 L F U' B L2 D R2 F' U B' D2 L' U2

> R U R' U'
（キューブが表示される）

> solve
解析中...
解法 (45手):
U R U' R' ...

解法を適用しますか? (y/n): y
```

## プロジェクト構成

```
py-RubiksCube/
├── src/
│   ├── __init__.py    # パッケージ初期化
│   ├── cube.py        # Cubeクラス（データ構造と操作）
│   ├── solver.py      # Solverクラス（解法アルゴリズム）
│   └── cli.py         # コマンドラインインターフェース
├── tests/
│   ├── __init__.py    # テストパッケージ
│   └── test_cube.py   # ユニットテスト
└── README.md
```

## Python モジュールとしての使用

```python
from src.cube import Cube
from src.solver import Solver

# キューブを作成
cube = Cube()

# 回転操作
cube.move_R()           # R回転
cube.move_U(prime=True) # U'回転

# アルゴリズムを実行
cube.execute_algorithm("R U R' U'")

# スクランブル
scramble_seq = cube.scramble(20)
print(f"スクランブル: {scramble_seq}")

# キューブを表示
cube.display()

# 解く
solver = Solver(cube)
solution = solver.solve()
print(f"解法: {solution}")
```

## キューブの色配置

```
      W W W           (U面: 白)
      W W W
      W W W

O O O G G G R R R B B B   (L:オレンジ, F:緑, R:赤, B:青)
O O O G G G R R R B B B
O O O G G G R R R B B B

      Y Y Y           (D面: 黄)
      Y Y Y
      Y Y Y
```

## 回転記法について

- **U (Up)**: 上面を時計回りに 90 度回転
- **D (Down)**: 下面を時計回りに 90 度回転
- **F (Front)**: 前面を時計回りに 90 度回転
- **B (Back)**: 後面を時計回りに 90 度回転
- **L (Left)**: 左面を時計回りに 90 度回転
- **R (Right)**: 右面を時計回りに 90 度回転

### 修飾子

- `'` (プライム): 反時計回りに回転（例: `R'`）
- `2`: 180 度回転（例: `R2`）

## テストの実行

```bash
python -m unittest tests.test_cube -v
```

## 技術詳細

### データ構造

キューブは 6 面の 3×3 グリッドとして表現されます。各面は 2 次元リストで、セルには色を表す文字（W, Y, G, B, O, R）が格納されます。

### ソルバーアルゴリズム

レイヤーバイレイヤー法（LBL 法）を使用しています：

1. **白十字**: 上面に白のエッジを配置
2. **第 1 層コーナー**: 白の角を正しい位置に配置
3. **第 2 層エッジ**: 中段のエッジを配置
4. **黄色十字**: 下面に黄色の十字を作成
5. **黄色面**: 下面を全て黄色に
6. **最終層コーナー位置**: コーナーを正しい位置に
7. **最終層エッジ**: エッジを正しい位置に

## ライセンス

MIT License

## 貢献

Issue や Pull Request は歓迎します！
