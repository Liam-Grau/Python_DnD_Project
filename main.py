import os
import subprocess
import sys
import importlib


def set_up(modules):
    os.system('color')
    imported_modules = {}
    for module_name in modules:
        try:
            module = importlib.import_module(module_name)
            imported_modules[module_name] = module
            print(f"Module '{module_name}' importé avec succès.")
        except ImportError:
            print(f"Module '{module_name}' introuvable. Installation en cours...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
                module = importlib.import_module(module_name)
                imported_modules[module_name] = module
                print(f"Module '{module_name}' installé et importé avec succès.")
            except Exception as e:
                print(f"Erreur lors de l'installation du module '{module_name}': {e}")

    print("\n\n")
    return imported_modules


def main():
    GameModule = importlib.import_module("src.Game")
    g = GameModule.Game()
    g.begin_game()
    g.game_round()


if __name__ == "__main__":
    set_up(["numpy", "keyboard"])
    main()
