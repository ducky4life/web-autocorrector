from dyslexicloglog import Autocorrector

ac = Autocorrector()

def autocorrector(query:str, number:int=1):
    input_list = query.split(",")
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

def prettify_autocorrector(query:str, number:int=1):
    ac_results = autocorrector(query, number)
    msg = ""
    for key in ac_results:
        output = []
        word_list = ac_results[key.lower()]

        for i in range(1, len(word_list)+1):
            output.append(f"{i}. {word_list[i-1]}")
        msg += f'{key}: {" ".join(output)}'
    return msg