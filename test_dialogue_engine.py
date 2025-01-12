from src.DialogueEngine import *
from src.Map import *
from src.Character import *
from src.Player import *

dEngine = DialogueEngine()

dEngine.load_dialogues("data/Introduction_Dialogue.json")

player = Player()
npc = Character("Maitre du jeu")

game_map = Map()

funcs = { "s_world_width" : game_map.s_width,
		  "s_world_length" : game_map.s_height,
		  "s_player_name" : player.s_name,
		  "choose_stats" : player.choose_stats,
		  "rand_stats" : player.random_stats,
		  "s_strength" : player.s_strength,
		  "s_resistance" : player.s_resistance,
		  "s_initiative" : player.s_initiative,
		  "s_dexterity" : player.s_dexterity,
		  "start" : dEngine.start,
		  "leave" : dEngine.leave,
		  "continue_dialogue" : player.continue_dialogue
		 }

dEngine.set_mapped_functions(funcs)

dEngine.start_new_dialogue("presentation_dialogue", player, npc)