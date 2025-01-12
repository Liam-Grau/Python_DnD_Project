import json
import time
import src.Character

from src.Color import *

def fstr(variable):
    context = {"self": DialogueEngine}
    return eval(f'f"""{variable}"""', {}, context)

class DialogueEngine:
    def __init__(self):
        self.__current_dialogues_data = None
        self.__active_dialogue = None
        self.__curent_line = 0
        DialogueEngine.player = None
        DialogueEngine.__npc = None
        self.__mapped_functions = {}
        self.__dialogue_wait_list = []

    # Loads a json file that contains dialogues
    def load_dialogues(self, path):
        with open(path, 'r') as f:
             self.__current_dialogues = json.load(f)
    
    # Sets the mapped functions
    def set_mapped_functions(self, mapped_functions):
        self.__mapped_functions = mapped_functions

    # Starts a specific dialogue specified by name
    def start_new_dialogue(self, dialogue_name, player, npc):

        DialogueEngine.player = player
        DialogueEngine.npc = npc

        self.start_dialogue(dialogue_name)

    # Starts a specific dialogue specified by name without a new player or a new npc
    def start_dialogue(self, dialogue_name):

        if self.__active_dialogue != None:
            self.__dialogue_wait_list.append(dialogue_name)
            return

        self.__try_start_dialogue(dialogue_name)

        while len(self.__dialogue_wait_list) > 0:
            self.__try_start_dialogue(self.__dialogue_wait_list[0])
            self.__dialogue_wait_list.remove(self.__dialogue_wait_list[0])

    # Checks if the dialogue exists and start it if exists
    def __try_start_dialogue(self, dialogue_name):

        index = 0

        for dialogue in self.__current_dialogues:
            if dialogue_name == dialogue["dialogue_name"]:
                self.__active_dialogue = dialogue
                self.__print_dialogue(dialogue["dialogue_lines"])
                break

            index += 1

        if index == len(self.__current_dialogues):
            raise ValueError(f"Dialogue Engine cannot find {dialogue_name} in the current dialogues data !")

    # Prints all the dialogue
    def __print_dialogue(self, dialogue_lines):

        for line_data in dialogue_lines:

            self.__print_line(line_data)

            self.__curent_line += 1

        self.__active_dialogue = None
        self.__curent_line = 0

    # Prints one line of the dialogue
    def __print_line(self, line_data):

        print(f"< [{colored_str(DialogueEngine.npc.name, Color.LIGHT_BLUE)}]: " + fstr(line_data['line']))
        time.sleep(line_data["time"])

        if len(line_data["answers"]) <= 0:
            return

        # Each first element of the answers is the type of answer
        # 0 is a free type answer where the user specifies anything
        # 1 is a precises answer type specified by the dialogue file

        if line_data["answers"][0]["type"] == 0:
            self.__get_free_answer(line_data["answers"][1]["function"])
            return

        if line_data["answers"][0]["type"] == 1:
            self.__show_answers(line_data["answers"][1:])
            return

    # Print the last printed line
    def __re_print_line(self):

        self.__print_line(self.__active_dialogue["dialogue_lines"][self.__curent_line])

    # Clears the last printed line
    def __clear_last_line(self):
        print(f"\033[A", end='') # Moves cursor one the line above it
        print(f"\033[K", end='') # Clears the line data

    # Prints the player answer
    def __print_answer(self, answer):
        print(f"> [{colored_str(DialogueEngine.player.name, Color.LIGHT_GREEN)}]: " + answer)

    # Shows the possibles answers of a line
    def __show_answers(self, answers_data):
       
        index = 1
        for answer_data in answers_data:
            index_txt = colored_str(str(index), Color.LIGHT_RED)
            print(f"     [{index_txt}] - " + answer_data["answer"])
            index += 1

        result = self.__get_answer_input(answers_data)

        for i in range(len(answers_data) + 1):
            self.__clear_last_line()

        self.__print_answer(answers_data[result - 1]["answer"])

    # Get input answer of free choice functions
    def __get_free_answer(self, function_name):


        is_correct = False

        while not is_correct:

            result_data = input()
            self.__clear_last_line()

            if not function_name in self.__mapped_functions:
                raise ValueError(f"Dialogue Engine cannot find {function_name} in the current mapped functions !")
            else:
                if function_name[0:2] == "s_":
                    is_correct = self.__mapped_functions[function_name](result_data)
                else:
                    is_correct = self.__mapped_functions[function_name](self, result_data)

        self.__print_answer(result_data)

        return result_data

    # Get input answer of multiple choice functions
    def __get_answer_input(self, answers_data):

        is_valid = False

        while not is_valid:
            # If the value can't be converted to an int
            # we just reprint the line
            try:
                result_data = int(input())

                # If the input is above or below the number of answers
                # Simply reprint the line
                if result_data < 1 or result_data > len(answers_data):
                    self.__clear_last_line()
                    continue

                is_valid = True

                function_name = answers_data[result_data - 1]["function"]

                if not function_name in self.__mapped_functions:
                    raise ValueError(f"Dialogue Engine cannot find {function_name} in the current mapped functions !")
                else:
                    if function_name[0:2] == "s_":
                        self.__mapped_functions[function_name](result_data)
                    else:
                        self.__mapped_functions[function_name](self, result_data)

                # Call function
                return result_data
            except ValueError:
                is_valid = False
                self.__clear_last_line()
                continue

    # Simple function callback
    def start(self, dialogue_engine, result):
	    dialogue_engine.start_dialogue("play_dialogue")