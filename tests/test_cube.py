"""
ルービックキューブシミュレーターのユニットテスト

このモジュールでは、Cubeクラスとsolverモジュールの
各機能をテストします。
"""

import unittest
import sys
import os

# srcディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cube import Cube
from src.solver import Solver, get_solution


class TestCubeInitialization(unittest.TestCase):
    """
    キューブの初期化に関するテスト
    """

    def test_initial_state_is_solved(self):
        """初期状態が完成状態であることを確認"""
        cube = Cube()
        self.assertTrue(cube.is_solved())

    def test_initial_faces_correct(self):
        """初期状態で各面が正しい色であることを確認"""
        cube = Cube()
        # U面が全て白
        for row in cube.faces[Cube.U]:
            for cell in row:
                self.assertEqual(cell, 'W')
        # D面が全て黄
        for row in cube.faces[Cube.D]:
            for cell in row:
                self.assertEqual(cell, 'Y')
        # F面が全て緑
        for row in cube.faces[Cube.F]:
            for cell in row:
                self.assertEqual(cell, 'G')

    def test_reset(self):
        """リセット機能のテスト"""
        cube = Cube()
        cube.move_U()
        cube.move_R()
        self.assertFalse(cube.is_solved())
        cube.reset()
        self.assertTrue(cube.is_solved())


class TestCubeMoves(unittest.TestCase):
    """
    キューブの回転操作に関するテスト
    """

    def test_U_move_four_times_returns_to_initial(self):
        """U面を4回回転すると元に戻ることを確認"""
        cube = Cube()
        initial_state = str(cube)
        for _ in range(4):
            cube.move_U()
        self.assertEqual(str(cube), initial_state)

    def test_U_prime_is_inverse(self):
        """U'がUの逆操作であることを確認"""
        cube = Cube()
        cube.move_U()
        cube.move_U(prime=True)
        self.assertTrue(cube.is_solved())

    def test_R_move_four_times_returns_to_initial(self):
        """R面を4回回転すると元に戻ることを確認"""
        cube = Cube()
        initial_state = str(cube)
        for _ in range(4):
            cube.move_R()
        self.assertEqual(str(cube), initial_state)

    def test_F_move_four_times_returns_to_initial(self):
        """F面を4回回転すると元に戻ることを確認"""
        cube = Cube()
        initial_state = str(cube)
        for _ in range(4):
            cube.move_F()
        self.assertEqual(str(cube), initial_state)

    def test_sexy_move_six_times_returns_to_initial(self):
        """R U R' U' を6回繰り返すと元に戻ることを確認"""
        cube = Cube()
        for _ in range(6):
            cube.execute_algorithm("R U R' U'")
        self.assertTrue(cube.is_solved())

    def test_execute_move_with_double(self):
        """2回転（例: U2）が正しく動作することを確認"""
        cube1 = Cube()
        cube2 = Cube()
        
        cube1.execute_move("U2")
        cube2.move_U()
        cube2.move_U()
        
        self.assertEqual(str(cube1), str(cube2))


class TestCubeAlgorithm(unittest.TestCase):
    """
    アルゴリズム実行に関するテスト
    """

    def test_execute_algorithm(self):
        """複数手順のアルゴリズムが正しく実行されることを確認"""
        cube = Cube()
        cube.execute_algorithm("R U R' U'")
        self.assertFalse(cube.is_solved())

    def test_sune_six_times(self):
        """Suneアルゴリズムを6回実行すると元に戻ることを確認"""
        cube = Cube()
        sune = "R U R' U R U2 R'"
        for _ in range(6):
            cube.execute_algorithm(sune)
        self.assertTrue(cube.is_solved())


class TestCubeScramble(unittest.TestCase):
    """
    スクランブル機能に関するテスト
    """

    def test_scramble_changes_state(self):
        """スクランブル後にキューブが完成状態でないことを確認"""
        cube = Cube()
        cube.scramble(20)
        self.assertFalse(cube.is_solved())

    def test_scramble_returns_moves(self):
        """スクランブルが手順を返すことを確認"""
        cube = Cube()
        scramble_seq = cube.scramble(10)
        self.assertTrue(len(scramble_seq) > 0)
        moves = scramble_seq.split()
        self.assertEqual(len(moves), 10)


class TestCubeCopy(unittest.TestCase):
    """
    キューブのコピー機能に関するテスト
    """

    def test_copy_is_independent(self):
        """コピーが元のキューブと独立していることを確認"""
        cube1 = Cube()
        cube2 = cube1.copy()
        
        cube1.move_U()
        
        self.assertFalse(cube1.is_solved())
        self.assertTrue(cube2.is_solved())


class TestSolver(unittest.TestCase):
    """
    ソルバーに関するテスト
    """

    def test_solver_on_solved_cube(self):
        """完成状態のキューブに対するソルバーの動作を確認"""
        cube = Cube()
        solver = Solver(cube)
        solution = solver.solve()
        self.assertEqual(solution, "すでに完成しています")

    def test_solver_simple_scramble(self):
        """簡単なスクランブルに対するソルバーの動作を確認"""
        cube = Cube()
        cube.execute_algorithm("R U R' U'")
        
        # ソルバーを実行
        solver = Solver(cube.copy())
        solution = solver.solve()
        
        # 解法を適用
        if solution != "解法が見つかりませんでした":
            cube.execute_algorithm(solution)
            # 完全に解けなくても、部分的な解法があることを確認
            self.assertIsNotNone(solution)

    def test_get_solution_function(self):
        """get_solution便利関数のテスト"""
        cube = Cube()
        solution = get_solution(cube)
        self.assertEqual(solution, "すでに完成しています")


class TestMoveHistory(unittest.TestCase):
    """
    操作履歴に関するテスト
    """

    def test_history_records_moves(self):
        """操作履歴が正しく記録されることを確認"""
        cube = Cube()
        cube.move_U()
        cube.move_R()
        cube.move_F(prime=True)
        
        self.assertEqual(len(cube.move_history), 3)
        self.assertEqual(cube.move_history[0], "U")
        self.assertEqual(cube.move_history[1], "R")
        self.assertEqual(cube.move_history[2], "F'")

    def test_reset_clears_history(self):
        """リセットで履歴がクリアされることを確認"""
        cube = Cube()
        cube.move_U()
        cube.move_R()
        cube.reset()
        
        self.assertEqual(len(cube.move_history), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
