"""
ルービックキューブシミュレーターのコマンドラインインターフェース

このモジュールは、ユーザーがコマンドラインからキューブを操作できる
インタラクティブなインターフェースを提供します。
"""

import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cube import Cube
from src.solver import Solver


def print_help() -> None:
    """
    ヘルプメッセージを表示する
    """
    help_text = """
╔══════════════════════════════════════════════════════════════════╗
║            ルービックキューブシミュレーター                       ║
╠══════════════════════════════════════════════════════════════════╣
║  コマンド一覧:                                                    ║
║                                                                   ║
║  回転操作:                                                        ║
║    U, U', U2  - 上面を回転（時計回り、反時計回り、180度）          ║
║    D, D', D2  - 下面を回転                                        ║
║    F, F', F2  - 前面を回転                                        ║
║    B, B', B2  - 後面を回転                                        ║
║    L, L', L2  - 左面を回転                                        ║
║    R, R', R2  - 右面を回転                                        ║
║                                                                   ║
║  その他のコマンド:                                                ║
║    show       - キューブを表示                                    ║
║    reset      - キューブを初期状態にリセット                      ║
║    scramble   - キューブをランダムにスクランブル                  ║
║    scramble N - N手でスクランブル（例: scramble 25）              ║
║    solve      - キューブを解く                                    ║
║    history    - 操作履歴を表示                                    ║
║    undo       - 最後の操作を取り消し                              ║
║    help       - このヘルプを表示                                  ║
║    quit       - 終了                                              ║
║                                                                   ║
║  複数の操作を一度に実行:                                          ║
║    例: R U R' U' （スペース区切りで入力）                         ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(help_text)


def undo_move(cube: Cube) -> bool:
    """
    最後の操作を取り消す

    Args:
        cube: キューブ

    Returns:
        取り消しに成功したらTrue
    """
    if not cube.move_history:
        print("取り消す操作がありません")
        return False

    last_move = cube.move_history.pop()
    
    # 逆操作を計算
    if last_move.endswith("'"):
        inverse = last_move[:-1]
    elif last_move.endswith("2"):
        inverse = last_move  # 180度回転は同じ
    else:
        inverse = last_move + "'"

    # 履歴を一時的に保存して逆操作を実行
    history_backup = cube.move_history[:]
    cube.execute_move(inverse)
    cube.move_history = history_backup  # 履歴を復元

    print(f"'{last_move}' を取り消しました")
    return True


def main() -> None:
    """
    メインのインタラクティブループ
    """
    cube = Cube()
    
    print("\n" + "=" * 50)
    print("  ルービックキューブシミュレーター")
    print("=" * 50)
    print("\n'help' でコマンド一覧を表示します")
    print("'quit' で終了します\n")
    
    cube.display()
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
            
            # コマンドを解析
            parts = user_input.lower().split()
            command = parts[0]
            
            if command in ['quit', 'exit', 'q']:
                print("終了します")
                break
            
            elif command == 'help':
                print_help()
            
            elif command == 'show':
                cube.display()
            
            elif command == 'reset':
                cube.reset()
                print("キューブをリセットしました")
                cube.display()
            
            elif command == 'scramble':
                num_moves = 20
                if len(parts) > 1:
                    try:
                        num_moves = int(parts[1])
                    except ValueError:
                        print("無効な数値です。デフォルトの20手でスクランブルします")
                
                scramble_seq = cube.scramble(num_moves)
                print(f"スクランブル: {scramble_seq}")
                cube.display()
            
            elif command == 'solve':
                print("解析中...")
                solver = Solver(cube.copy())
                solution = solver.solve()
                
                if solution == "すでに完成しています":
                    print(solution)
                elif solution == "解法が見つかりませんでした":
                    print(solution)
                else:
                    print(f"\n解法 ({len(solution.split())}手):")
                    print(solution)
                    
                    # 解法を適用するか確認
                    apply = input("\n解法を適用しますか? (y/n): ").strip().lower()
                    if apply == 'y':
                        cube.execute_algorithm(solution)
                        print("解法を適用しました")
                        cube.display()
            
            elif command == 'history':
                if cube.move_history:
                    print(f"操作履歴 ({len(cube.move_history)}手):")
                    print(' '.join(cube.move_history))
                else:
                    print("操作履歴はありません")
            
            elif command == 'undo':
                if undo_move(cube):
                    cube.display()
            
            else:
                # 回転操作として解釈
                moves = user_input.upper().split()
                valid_moves = ['U', "U'", 'U2', 'D', "D'", 'D2',
                              'F', "F'", 'F2', 'B', "B'", 'B2',
                              'L', "L'", 'L2', 'R', "R'", 'R2']
                
                all_valid = True
                for move in moves:
                    if move not in valid_moves:
                        print(f"無効なコマンド: {move}")
                        print("'help' でコマンド一覧を確認してください")
                        all_valid = False
                        break
                
                if all_valid:
                    for move in moves:
                        cube.execute_move(move)
                    cube.display()
        
        except KeyboardInterrupt:
            print("\n終了します")
            break
        except EOFError:
            print("\n終了します")
            break


if __name__ == "__main__":
    main()
