from dyslexicloglog import Autocorrector

def autocorrector(query:list, number:int=1, dictionary="test_files/20k_shun4midx.txt"):

    ac = Autocorrector(dictionary)

    input_list = query
    if number not in [1,2,3]:
        return "please choose a number between 1 to 3 inclusive"
    
    ac_results = ac.top3(input_list)

    if number == 3:
        return ac_results
    
    else:
        for key in ac_results:

            for i in range(3-number):
                ac_results[key].pop(-1)
                
        return ac_results

def prettify_autocorrector(query:str, number:int=1, dictionary="test_files/20k_shun4midx.txt", alphabetize=None):
    ac_results = autocorrector(query, number, dictionary)

    # if toggle is on, sort results by alphabetical order
    if alphabetize != None:
        ac_results = dict(sorted(ac_results.items()))

    msg = []

    for key in ac_results:
        output = []
        word_list = ac_results[key]

        for i in range(1, len(word_list)+1):
            output.append(f"{i}. {word_list[i-1]}")
        msg.append(f'{key}: {" ".join(output)}')
    return msg
