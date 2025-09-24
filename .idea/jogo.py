import sys

class MazeCreator:
    __instance = None

    @staticmethod
    def get_instance():
        if MazeCreator.__instance is None:
            MazeCreator()
        return MazeCreator.__instance

    def __init__(self):
        if MazeCreator.__instance is not None:
            raise Exception("A classe MazeCreator já existe! Use get_instance().")
        else:
            MazeCreator.__instance = self
            self.maps = [
                [
                    ["E", "_", "_", "#", "_"],
                    ["#", "#", "_", "#", "#"],
                    ["_", "_", "_", "_", "#"],
                    ["#", "_", "#", "_", "_"],
                    ["#", "_", "_", "_", "S"],
                ],
                [
                    ["E", "_", "#", "_", "_"],
                    ["#", "_", "#", "_", "#"],
                    ["#", "_", "_", "_", "#"],
                    ["#", "#", "#", "_", "#"],
                    ["S", "_", "_", "_", "#"],
                ],
            ]

class Game:
    __instance = None

    @staticmethod
    def get_instance():
        if Game.__instance is None:
            Game()
        return Game.__instance

    def __init__(self):
        if Game.__instance is not None:
            raise Exception("Este jogo já existe! Use get_instance().")
        else:
            Game.__instance = self
            self.current_map_index = 0
            self.maze_creator = MazeCreator.get_instance()
            self.maps = self.maze_creator.maps
            self.total_maps = len(self.maps)
            self.position = self.find_entry()
            self.choose_theme()

    def choose_theme(self):
        print("Escolha seu personagem e estilo de caminho:")
        print("1 - 🐍 Cobra (caminho 🍎)")
        print("2 - 🚶 Pessoa andando (caminho 💰)")
        choice = ""
        while choice not in ["1", "2"]:
            choice = input("Digite 1 ou 2: ")
        if choice == "1":
            self.player_emoji = "🐍"
            self.path_emoji = "🍎"
        else:
            self.player_emoji = "🚶"
            self.path_emoji = "💰"

    def find_entry(self):
        for i, row in enumerate(self.maps[self.current_map_index]):
            for j, col in enumerate(row):
                if col == "E":
                    return (i, j)

    def print_map(self):
        game_map = self.maps[self.current_map_index]
        for i, row in enumerate(game_map):
            row_str = ""
            for j, col in enumerate(row):
                if (i, j) == self.position:
                    row_str += self.player_emoji
                elif col == "#":
                    row_str += "🧱"
                elif col == "E":
                    row_str += "🚪"
                elif col == "S":
                    row_str += "🎯"
                elif col == "_":
                    row_str += self.path_emoji
                elif col == "V":  # Visitado
                    row_str += "⬜"
            print(row_str)
        print()

    def move(self, direction):
        i, j = self.position
        if direction == "norte":
            new_pos = (i - 1, j)
        elif direction == "sul":
            new_pos = (i + 1, j)
        elif direction == "leste":
            new_pos = (i, j + 1)
        elif direction == "oeste":
            new_pos = (i, j - 1)
        else:
            print("Movimento inválido!")
            return

        if self.valid_move(new_pos):
            # Marcar caminho anterior como visitado
            if self.maps[self.current_map_index][i][j] == "_":
                self.maps[self.current_map_index][i][j] = "V"
            self.position = new_pos
            if self.is_exit(new_pos):
                self.next_map()
        else:
            print("Movimento bloqueado!")

    def valid_move(self, pos):
        i, j = pos
        game_map = self.maps[self.current_map_index]
        if 0 <= i < len(game_map) and 0 <= j < len(game_map[0]):
            return game_map[i][j] != "#"
        return False

    def is_exit(self, pos):
        i, j = pos
        return self.maps[self.current_map_index][i][j] == "S"

    def next_map(self):
        print("Você encontrou a saída! Avançando para o próximo mapa...")
        self.current_map_index += 1
        if self.current_map_index >= self.total_maps:
            print("🎉 Parabéns! Você venceu o jogo! 🎉")
            sys.exit()
        else:
            self.position = self.find_entry()


# ---- Roda o jogo ----
if __name__ == "__main__":
    jogo = Game.get_instance()

    while True:
        jogo.print_map()
        move = input("Mover (norte/sul/leste/oeste): ").lower()
        jogo.move(move)
