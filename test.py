big_dict = {
    "a":":regional_indicator_a:",
    "b":":regional_indicator_b:",
    "c":":regional_indicator_c:",
    "d":":regional_indicator_d:",
    "e":":regional_indicator_e:",
    "f":":regional_indicator_f:",
    "g":":regional_indicator_g:",
    "h":":regional_indicator_h:",
    "i":":regional_indicator_i:",
    "j":":regional_indicator_j:",
    "k":":regional_indicator_k:",
    "l":":regional_indicator_l:",
    "m":":regional_indicator_m:",
    "n":":regional_indicator_n:",
    "o":":regional_indicator_o:",
    "p":":regional_indicator_p:",
    "q":":regional_indicator_q:",
    "r":":regional_indicator_r:",
    "s":":regional_indicator_s:",
    "t":":regional_indicator_t:",
    "u":":regional_indicator_u:",
    "v":":regional_indicator_v:",
    "w":":regional_indicator_w:",
    "x":":regional_indicator_x:",
    "y":":regional_indicator_y:",
    "z":":regional_indicator_z:"
}

def big(words):
    output = []
    for word in words.split(" "):
        for letter in word:
            output.append(big_dict[letter])
        output.append(" ")
    return output

print(" ".join(big("sam likes dick")))
