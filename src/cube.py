"""
ルービックキューブのデータ構造と操作を定義するモジュール

このモジュールでは、3x3x3のルービックキューブを表現し、
各面の回転操作を提供します。
"""

import random
from typing import List, Optional
from copy import deepcopy


class Cube:
    """
    ルービックキューブを表現するクラス

    6面（U:上、D:下、F:前、B:後、L:左、R:右）を持ち、
    各面は3x3のグリッドで表現される。

    色の表現:
        W: 白 (White) - U面
        Y: 黄 (Yellow) - D面
        G: 緑 (Green) - F面
        B: 青 (Blue) - B面
        O: オレンジ (Orange) - L面
        R: 赤 (Red) - R面
    """

    # 面のインデックス定数
    U = 0  # 上面 (Up)
    D = 1  # 下面 (Down)
    F = 2  # 前面 (Front)
    B = 3  # 後面 (Back)
    L = 4  # 左面 (Left)
    R = 5  # 右面 (Right)

    # 色の定義
    COLORS = {
        'W': '\033[97m█\033[0m',  # 白
        'Y': '\033[93m█\033[0m',  # 黄
        'G': '\033[92m█\033[0m',  # 緑
        'B': '\033[94m█\033[0m',  # 青
        'O': '\033[38;5;208m█\033[0m',  # オレンジ
        'R': '\033[91m█\033[0m',  # 赤
    }

    # 各面の初期色
    FACE_COLORS = ['W', 'Y', 'G', 'B', 'O', 'R']

    def __init__(self):
        """
        キューブを初期状態（完成状態）で初期化する
        """
        self.faces = self._create_solved_cube()
        self.move_history: List[str] = []

    def _create_solved_cube(self) -> List[List[List[str]]]:
        """
        完成状態のキューブを作成する

        Returns:
            6面の3x3グリッドを持つリスト
        """
        faces = []
        for color in self.FACE_COLORS:
            face = [[color for _ in range(3)] for _ in range(3)]
            faces.append(face)
        return faces

    def reset(self) -> None:
        """
        キューブを初期状態にリセットする
        """
        self.faces = self._create_solved_cube()
        self.move_history = []

    def is_solved(self) -> bool:
        """
        キューブが完成状態かどうかを確認する

        Returns:
            完成状態ならTrue、そうでなければFalse
        """
        for face in self.faces:
            color = face[0][0]
            for row in face:
                for cell in row:
                    if cell != color:
                        return False
        return True

    def _rotate_face_clockwise(self, face_idx: int) -> None:
        """
        指定した面を時計回りに90度回転する

        Args:
            face_idx: 回転する面のインデックス
        """
        face = self.faces[face_idx]
        self.faces[face_idx] = [
            [face[2][0], face[1][0], face[0][0]],
            [face[2][1], face[1][1], face[0][1]],
            [face[2][2], face[1][2], face[0][2]]
        ]

    def _rotate_face_counter_clockwise(self, face_idx: int) -> None:
        """
        指定した面を反時計回りに90度回転する

        Args:
            face_idx: 回転する面のインデックス
        """
        face = self.faces[face_idx]
        self.faces[face_idx] = [
            [face[0][2], face[1][2], face[2][2]],
            [face[0][1], face[1][1], face[2][1]],
            [face[0][0], face[1][0], face[2][0]]
        ]

    def move_U(self, prime: bool = False) -> None:
        """
        U面（上面）を回転する

        Args:
            prime: Trueなら反時計回り、Falseなら時計回り
        """
        if prime:
            self._rotate_face_counter_clockwise(self.U)
            # 隣接するエッジを回転
            temp = self.faces[self.F][0][:]
            self.faces[self.F][0] = self.faces[self.R][0][:]
            self.faces[self.R][0] = self.faces[self.B][0][:]
            self.faces[self.B][0] = self.faces[self.L][0][:]
            self.faces[self.L][0] = temp
            self.move_history.append("U'")
        else:
            self._rotate_face_clockwise(self.U)
            # 隣接するエッジを回転
            temp = self.faces[self.F][0][:]
            self.faces[self.F][0] = self.faces[self.L][0][:]
            self.faces[self.L][0] = self.faces[self.B][0][:]
            self.faces[self.B][0] = self.faces[self.R][0][:]
            self.faces[self.R][0] = temp
            self.move_history.append("U")

    def move_D(self, prime: bool = False) -> None:
        """
        D面（下面）を回転する

        Args:
            prime: Trueなら反時計回り、Falseなら時計回り
        """
        if prime:
            self._rotate_face_counter_clockwise(self.D)
            temp = self.faces[self.F][2][:]
            self.faces[self.F][2] = self.faces[self.L][2][:]
            self.faces[self.L][2] = self.faces[self.B][2][:]
            self.faces[self.B][2] = self.faces[self.R][2][:]
            self.faces[self.R][2] = temp
            self.move_history.append("D'")
        else:
            self._rotate_face_clockwise(self.D)
            temp = self.faces[self.F][2][:]
            self.faces[self.F][2] = self.faces[self.R][2][:]
            self.faces[self.R][2] = self.faces[self.B][2][:]
            self.faces[self.B][2] = self.faces[self.L][2][:]
            self.faces[self.L][2] = temp
            self.move_history.append("D")

    def move_F(self, prime: bool = False) -> None:
        """
        F面（前面）を回転する

        Args:
            prime: Trueなら反時計回り、Falseなら時計回り
        """
        if prime:
            self._rotate_face_counter_clockwise(self.F)
            temp = [self.faces[self.U][2][i] for i in range(3)]
            for i in range(3):
                self.faces[self.U][2][i] = self.faces[self.R][i][0]
            for i in range(3):
                self.faces[self.R][i][0] = self.faces[self.D][0][2 - i]
            for i in range(3):
                self.faces[self.D][0][i] = self.faces[self.L][i][2]
            for i in range(3):
                self.faces[self.L][i][2] = temp[2 - i]
            self.move_history.append("F'")
        else:
            self._rotate_face_clockwise(self.F)
            temp = [self.faces[self.U][2][i] for i in range(3)]
            for i in range(3):
                self.faces[self.U][2][i] = self.faces[self.L][2 - i][2]
            for i in range(3):
                self.faces[self.L][i][2] = self.faces[self.D][0][i]
            for i in range(3):
                self.faces[self.D][0][i] = self.faces[self.R][2 - i][0]
            for i in range(3):
                self.faces[self.R][i][0] = temp[i]
            self.move_history.append("F")

    def move_B(self, prime: bool = False) -> None:
        """
        B面（後面）を回転する

        Args:
            prime: Trueなら反時計回り、Falseなら時計回り
        """
        if prime:
            self._rotate_face_counter_clockwise(self.B)
            temp = [self.faces[self.U][0][i] for i in range(3)]
            for i in range(3):
                self.faces[self.U][0][i] = self.faces[self.L][2 - i][0]
            for i in range(3):
                self.faces[self.L][i][0] = self.faces[self.D][2][i]
            for i in range(3):
                self.faces[self.D][2][i] = self.faces[self.R][2 - i][2]
            for i in range(3):
                self.faces[self.R][i][2] = temp[i]
            self.move_history.append("B'")
        else:
            self._rotate_face_clockwise(self.B)
            temp = [self.faces[self.U][0][i] for i in range(3)]
            for i in range(3):
                self.faces[self.U][0][i] = self.faces[self.R][i][2]
            for i in range(3):
                self.faces[self.R][i][2] = self.faces[self.D][2][2 - i]
            for i in range(3):
                self.faces[self.D][2][i] = self.faces[self.L][i][0]
            for i in range(3):
                self.faces[self.L][i][0] = temp[2 - i]
            self.move_history.append("B")

    def move_L(self, prime: bool = False) -> None:
        """
        L面（左面）を回転する

        Args:
            prime: Trueなら反時計回り、Falseなら時計回り
        """
        if prime:
            self._rotate_face_counter_clockwise(self.L)
            temp = [self.faces[self.U][i][0] for i in range(3)]
            for i in range(3):
                self.faces[self.U][i][0] = self.faces[self.F][i][0]
            for i in range(3):
                self.faces[self.F][i][0] = self.faces[self.D][i][0]
            for i in range(3):
                self.faces[self.D][i][0] = self.faces[self.B][2 - i][2]
            for i in range(3):
                self.faces[self.B][i][2] = temp[2 - i]
            self.move_history.append("L'")
        else:
            self._rotate_face_clockwise(self.L)
            temp = [self.faces[self.U][i][0] for i in range(3)]
            for i in range(3):
                self.faces[self.U][i][0] = self.faces[self.B][2 - i][2]
            for i in range(3):
                self.faces[self.B][i][2] = self.faces[self.D][2 - i][0]
            for i in range(3):
                self.faces[self.D][i][0] = self.faces[self.F][i][0]
            for i in range(3):
                self.faces[self.F][i][0] = temp[i]
            self.move_history.append("L")

    def move_R(self, prime: bool = False) -> None:
        """
        R面（右面）を回転する

        Args:
            prime: Trueなら反時計回り、Falseなら時計回り
        """
        if prime:
            self._rotate_face_counter_clockwise(self.R)
            temp = [self.faces[self.U][i][2] for i in range(3)]
            for i in range(3):
                self.faces[self.U][i][2] = self.faces[self.B][2 - i][0]
            for i in range(3):
                self.faces[self.B][i][0] = self.faces[self.D][2 - i][2]
            for i in range(3):
                self.faces[self.D][i][2] = self.faces[self.F][i][2]
            for i in range(3):
                self.faces[self.F][i][2] = temp[i]
            self.move_history.append("R'")
        else:
            self._rotate_face_clockwise(self.R)
            temp = [self.faces[self.U][i][2] for i in range(3)]
            for i in range(3):
                self.faces[self.U][i][2] = self.faces[self.F][i][2]
            for i in range(3):
                self.faces[self.F][i][2] = self.faces[self.D][i][2]
            for i in range(3):
                self.faces[self.D][i][2] = self.faces[self.B][2 - i][0]
            for i in range(3):
                self.faces[self.B][i][0] = temp[2 - i]
            self.move_history.append("R")

    def execute_move(self, move: str) -> None:
        """
        文字列で指定された手順を実行する

        Args:
            move: 手順を表す文字列（例: "U", "R'", "F2"）
        """
        move = move.strip()
        if not move:
            return

        # 2回転の場合
        double = move.endswith('2')
        if double:
            move = move[:-1]

        # 反時計回りの場合
        prime = move.endswith("'")
        if prime:
            move = move[:-1]

        # 手順を実行
        move_map = {
            'U': self.move_U,
            'D': self.move_D,
            'F': self.move_F,
            'B': self.move_B,
            'L': self.move_L,
            'R': self.move_R,
        }

        if move in move_map:
            if double:
                move_map[move](prime)
                move_map[move](prime)
            else:
                move_map[move](prime)

    def execute_algorithm(self, algorithm: str) -> None:
        """
        スペース区切りのアルゴリズムを実行する

        Args:
            algorithm: スペース区切りの手順（例: "R U R' U'"）
        """
        moves = algorithm.split()
        for move in moves:
            self.execute_move(move)

    def scramble(self, num_moves: int = 20) -> str:
        """
        キューブをランダムにスクランブルする

        Args:
            num_moves: スクランブルの手数

        Returns:
            実行されたスクランブル手順
        """
        moves = ['U', 'D', 'F', 'B', 'L', 'R']
        modifiers = ['', "'", '2']
        scramble_moves = []
        last_move = None

        for _ in range(num_moves):
            # 同じ面の連続を避ける
            available_moves = [m for m in moves if m != last_move]
            move = random.choice(available_moves)
            modifier = random.choice(modifiers)
            scramble_moves.append(move + modifier)
            self.execute_move(move + modifier)
            last_move = move

        return ' '.join(scramble_moves)

    def get_face(self, face_idx: int) -> List[List[str]]:
        """
        指定した面のコピーを取得する

        Args:
            face_idx: 面のインデックス

        Returns:
            面の3x3グリッド
        """
        return deepcopy(self.faces[face_idx])

    def copy(self) -> 'Cube':
        """
        キューブのディープコピーを作成する

        Returns:
            新しいCubeインスタンス
        """
        new_cube = Cube()
        new_cube.faces = deepcopy(self.faces)
        new_cube.move_history = self.move_history[:]
        return new_cube

    def __str__(self) -> str:
        """
        キューブの文字列表現を返す（展開図形式）

        Returns:
            キューブの展開図を表す文字列
        """
        lines = []
        
        # U面（上）
        for row in self.faces[self.U]:
            line = "      " + ' '.join(self.COLORS[c] for c in row)
            lines.append(line)
        
        lines.append("")
        
        # L, F, R, B面（横一列）
        for i in range(3):
            line = ""
            line += ' '.join(self.COLORS[c] for c in self.faces[self.L][i]) + " "
            line += ' '.join(self.COLORS[c] for c in self.faces[self.F][i]) + " "
            line += ' '.join(self.COLORS[c] for c in self.faces[self.R][i]) + " "
            line += ' '.join(self.COLORS[c] for c in self.faces[self.B][i])
            lines.append(line)
        
        lines.append("")
        
        # D面（下）
        for row in self.faces[self.D]:
            line = "      " + ' '.join(self.COLORS[c] for c in row)
            lines.append(line)
        
        return '\n'.join(lines)

    def display(self) -> None:
        """
        キューブを表示する
        """
        print(self)
        print()
        print(f"完成状態: {'はい' if self.is_solved() else 'いいえ'}")
        if self.move_history:
            print(f"履歴: {' '.join(self.move_history[-20:])}")
