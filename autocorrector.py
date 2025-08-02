from dyslexicloglog import Autocorrector

def autocorrector(query:list, number:int=1, dictionary="test_files/20k_shun4midx.txt", alphabetize=None, keyboard_layout="qwerty"):
    print(keyboard_layout)
    ac = Autocorrector(dictionary_list=dictionary, keyboard=keyboard_layout)

    input_list = query
    if number not in [1,2,3]:
        return "please choose a number between 1 to 3 inclusive"
    
    ac_results = ac.top3(input_list)
    ac_dict = ac_results.suggestions

    if number != 3:
        for key in ac_dict:

            for i in range(3-number):
                ac_dict[key].pop(-1)
                
    # if toggle is on, sort results by alphabetical order
    if alphabetize != None:
        ac_dict = dict(sorted(ac_dict.items()))

    return ac_dict


def prettify_autocorrector(query:str, number:int=1, dictionary="test_files/20k_shun4midx.txt", alphabetize=None, keyboard_layout="qwerty"):
    ac_dict = autocorrector(query, number, dictionary, alphabetize, keyboard_layout)

    msg = []

    for key in ac_dict:
        output = []
        word_list = ac_dict[key]

        for i in range(1, len(word_list)+1):
            output.append(f"{i}. {word_list[i-1]}")
        msg.append(f'{key}: {" ".join(output)}')
    return msg
