"""
ルービックキューブのソルバーモジュール

操作履歴から逆手順を計算して解法を生成します。
"""

from typing import List
from .cube import Cube


class Solver:
    """
    ルービックキューブを解くソルバークラス

    操作履歴を使用して逆手順を計算します。
    """

    def __init__(self, cube: Cube):
        """
        ソルバーを初期化する

        Args:
            cube: 解くキューブ
        """
        self.cube = cube
        self.solution: List[str] = []

    def _get_inverse_move(self, move: str) -> str:
        """
        手順の逆手順を取得する

        Args:
            move: 手順

        Returns:
            逆手順
        """
        move = move.strip()
        if move.endswith("2"):
            # 180度回転は同じ
            return move
        elif move.endswith("'"):
            # 反時計回り → 時計回り
            return move[:-1]
        else:
            # 時計回り → 反時計回り
            return move + "'"

    def solve(self) -> str:
        """
        キューブを解く（履歴の逆手順を使用）

        Returns:
            解法の手順を表す文字列
        """
        if self.cube.is_solved():
            return "すでに完成しています"

        # 操作履歴がある場合は逆手順を計算
        if self.cube.move_history:
            # 履歴を逆順にして各手順の逆を取る
            inverse_moves = []
            for move in reversed(self.cube.move_history):
                inverse_moves.append(self._get_inverse_move(move))
            
            self.solution = inverse_moves
            return ' '.join(inverse_moves)
        else:
            return "解法が見つかりませんでした（操作履歴がありません。resetしてscrambleで崩してから試してください）"

    def solve_and_apply(self) -> str:
        """
        キューブを解いて解法を適用する

        Returns:
            解法の手順を表す文字列
        """
        solution = self.solve()
        
        if solution.startswith("すでに") or solution.startswith("解法が"):
            return solution
        
        # 解法を適用
        self.cube.execute_algorithm(solution)
        
        return solution


def get_solution(cube: Cube) -> str:
    """
    キューブの解法を取得する便利関数

    Args:
        cube: 解くキューブ

    Returns:
        解法の手順
    """
    solver = Solver(cube)
    return solver.solve()
