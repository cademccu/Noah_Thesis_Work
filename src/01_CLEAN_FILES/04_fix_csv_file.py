

# .......
# the excel spreadsheet is an absolute mess. this is just straight up swapping
# lines for what i THINK are the right matchkeys and conversation subjects so
# that they at least somewhat align with some source of truth -- the metadata, 
# the filename, something......



output_file = open("CCOT_files_and_scores_FIXED.csv", "wt")
input_file  = open("CCOT_files_and_scores.csv", "rt")

"""
def c_swap(line, search, replace):
    if line.startswith(search):
        output_file.write(replace + "\n")
    else:
        output_file.write(line)
"""        

changes = {}

def c_swap(line, key, value):
    if key not in changes:
        changes[key] = value
    else:
        print("[ERROR] what? double keys??? check this in c_swap")
    



# i did this stupidly, thought it would be iterative but now i just want to add the lines to a dict
# so the line var is a placeholder here since I have limited time to make beautiful corrections
# just imagine this is in better form

line = None

c_swap(line, 
    "Arabic,291,M,A,02292&02466_B.txt,Advertisement,B,F11wk5,1,36,2:07,3,3,3,2,2,2,2.5,2.5,2.5,7.5",
    "Arabic,291,M,A,02291&02466_B.txt,Advertisement,B,F11wk5,1,36,2:07,3,3,3,2,2,2,2.5,2.5,2.5,7.5")
c_swap(line,
    "Chinese,466,M,B,02292&02466_B.txt,Advertisement,B,F11wk5,1,36,2:07,3,3,3,2,2,2,2.5,2.5,2.5,7.5",
    "Chinese,466,M,B,02291&02466_B.txt,Advertisement,B,F11wk5,1,36,2:07,3,3,3,2,2,2,2.5,2.5,2.5,7.5")

c_swap(line,
    "Arabic,13,M,A,02013&02531_B.txt,Advertisement,B,F11wk5,1,38,1:51,4,3.5,3.75,3.5,3.5,2.75,3.5,3.5,3.5,10",
    "Arabic,13,M,A,02013&02431_B.txt,Advertisement,B,F11wk5,1,38,1:51,4,3.5,3.75,3.5,3.5,2.75,3.5,3.5,3.5,10")
c_swap(line,
    "Arabic,531,M,B,02013&02531_B.txt,Advertisement,B,F11wk5,1,38,1:51,4,3.5,3.75,3.5,3.5,2.75,3.5,3.5,3.5,10",
    "Arabic,431,M,B,02013&02431_B.txt,Advertisement,B,F11wk5,1,38,1:51,4,3.5,3.75,3.5,3.5,2.75,3.5,3.5,3.5,10")

#c_swap(line,
#    "Arabic,275,M,A,02282&02275_B.txt,Advertisement,B,F11wk5,1,19,1:26,3,3,3,3,3,2.5,3,3,3,8.5",
#    "Arabic,275,M,A,04282&04275_B.txt,Advertisement,B,F11wk5,1,19,1:26,3,3,3,3,3,2.5,3,3,3,8.5")
#c_swap(line,
#    "Arabic,282,F,B,02282&02275_B.txt,Advertisement,B,F11wk5,1,19,1:26,3,3,3,3,3,2.5,3,3,3,8.5",
#    "Arabic,282,F,B,04282&04275_B.txt,Advertisement,B,F11wk5,1,19,1:26,3,3,3,3,3,2.5,3,3,3,8.5")

c_swap(line,
    "Arabic,228,M,B,05594&05228_A.txt,Extreme Sports,S,F09wk5,1,50,1:14,4,3.5,3.75,4,3.5,3.75,3.5,3.5,3.5,11",
    "Arabic,228,M,B,04594&04228_A.txt,Extreme Sports,S,F09wk5,1,50,1:14,4,3.5,3.75,4,3.5,3.75,3.5,3.5,3.5,11")
c_swap(line,
    "Arabic,594,F,A,05594&05228_A.txt,Extreme Sports,S,F09wk5,1,50,1:14,4,3.5,3.75,4,4,4,4,3.5,3.75,11.5",
    "Arabic,594,F,A,04594&04228_A.txt,Extreme Sports,S,F09wk5,1,50,1:14,4,3.5,3.75,4,4,4,4,3.5,3.75,11.5")

c_swap(line,
    "Arabic,79,M,B,05499&05579_C.txt,Voluntary simplicity,A,F10wk10,1,104,3:14,3,3,3,2,2,2,3,3,3,8",
    "Arabic,79,M,B,05499&05079_C.txt,Voluntary simplicity,A,F10wk10,1,104,3:14,3,3,3,2,2,2,3,3,3,8")
c_swap(line,
    "Arabic,499,M,A,05499&05579_C.txt,Voluntary simplicity,A,F10wk10,1,104,3:14,3,3,3,2,2,2,3,3,3,8",
    "Arabic,499,M,A,05499&05079_C.txt,Voluntary simplicity,A,F10wk10,1,104,3:14,3,3,3,2,2,2,3,3,3,8")

c_swap(line,
    "Arabic,206,M,B,05212&05206_C.txt,Voluntary simplicity,A,F10wk10,1,99,2:38,3,3,3,2,2,2,3,3,3,8",
    "Arabic,206,M,B,07212&07206_C.txt,Voluntary simplicity,A,F10wk10,1,99,2:38,3,3,3,2,2,2,3,3,3,8")
c_swap(line,
    "Arabic,212,M,A,05212&05206_C.txt,Voluntary simplicity,A,F10wk10,1,99,2:38,3,3,3,2,2,2,3,3,3,8",
    "Arabic,212,M,A,07212&07206_C.txt,Voluntary simplicity,A,F10wk10,1,99,2:38,3,3,3,2,2,2,3,3,3,8")

c_swap(line,
    "Arabic,322,M,B,08556&08332_S.txt,Choosing a patient,A,F10wk5,2,13,2:59,3,3,3,2,3,2.5,2,3,2.5,8",
    "Arabic,322,M,B,08556&08322_S.txt,Choosing a patient,A,F10wk5,2,13,2:59,3,3,3,2,3,2.5,2,3,2.5,8")
c_swap(line,
    "Chinese,556,M,A,08556&08332_S.txt,Choosing a patient,A,F10wk5,2,13,2:59,3,3,3,2,2,2,2,3,2.5,7.5",
    "Chinese,556,M,A,08556&08322_S.txt,Choosing a patient,A,F10wk5,2,13,2:59,3,3,3,2,2,2,2,3,2.5,7.5")

c_swap(line,
    "Arabic,30,M,A,09303&09471_S.txt,Choosing a patient,B,F11wk10,2,12,1:59,4,4,4,4,3,3.5,3,3,3,10.5",
    "Arabic,30,M,A,09030&09471_S.txt,Choosing a patient,B,F11wk10,2,12,1:59,4,4,4,4,3,3.5,3,3,3,10.5")
c_swap(line,
    "Arabic,471,M,B,09303&09471_S.txt,Choosing a patient,B,F11wk10,2,12,1:59,4,4,4,3,4,3.5,3,3,3,10.5",
    "Arabic,471,M,B,09030&09471_S.txt,Choosing a patient,B,F11wk10,2,12,1:59,4,4,4,3,4,3.5,3,3,3,10.5")

c_swap(line,
    "Chinese,354,M,A,09354&09543_S.txt,Choosing a patient,B,F11wk10,2,6,2:06,4,3,3.5,4,4,4,4,4,4,11.5",
    "Chinese,354,M,A,09354&09453_S.txt,Choosing a patient,B,F11wk10,2,6,2:06,4,3,3.5,4,4,4,4,4,4,11.5")
c_swap(line, 
    "Chinese,453,F,B,09354&09543_S.txt,Choosing a patient,B,F11wk10,2,6,2:06,4,3,3.5,4,4,4,4,4,4,11.5",
    "Chinese,453,F,B,09354&09453_S.txt,Choosing a patient,B,F11wk10,2,6,2:06,4,3,3.5,4,4,4,4,4,4,11.5")

c_swap(line,
    "Arabic,171,M,B,16068&16172_S.txt,Investing-Science Funding,A,F10wk15,2,25,2:33,4,4,4,3,3.5,3.25,3,3.5,3.25,10.5",
    "Arabic,171,M,B,16068&16171_S.txt,Investing-Science Funding,A,F10wk15,2,25,2:33,4,4,4,3,3.5,3.25,3,3.5,3.25,10.5")
# only one wrong

c_swap(line,
    "Arabic,137,F,B,16103&16138_S.txt,Investing-Science Funding,A,F10wk15,2,23,2:31,3,3,3,3,3,3,3,3.5,3.25,9.25",
    "Arabic,137,F,B,16103&16137_S.txt,Investing-Science Funding,A,F10wk15,2,23,2:31,3,3,3,3,3,3,3,3.5,3.25,9.25")
# only one wrong

c_swap(line,
    "Arabic,340,M,A,16161&16341_S.txt,Investing-Famous Entrepreneur,S,F11wk15,2,21,2:31,4,4,4,4,4,4,4,4,4,12",
    "Arabic,340,M,A,16161&16340_S.txt,Investing-Famous Entrepreneur,S,F11wk15,2,21,2:31,4,4,4,4,4,4,4,4,4,12")
# only one wrong

c_swap(line,
    "Arabic,182,M,A,16182&16085_S.txt,Investing-Science Funding,A,F10wk15,2,27,2:15,3,3,3,4,3.5,3.75,4,4,4,10.75",
    "Arabic,182,M,A,16182&16084_S.txt,Investing-Science Funding,A,F10wk15,2,27,2:15,3,3,3,4,3.5,3.75,4,4,4,10.75")
# only one wrong

c_swap(line,
    "Chinese,466,M,B,16185&16467_S.txt,Investing-Famous Entrepreneur,S,F11wk15,2,20,2:33,3.5,3.5,3.5,4,4,4,4,3.5,3.75,11.25",
    "Chinese,466,M,B,16185&16466_S.txt,Investing-Famous Entrepreneur,S,F11wk15,2,20,2:33,3.5,3.5,3.5,4,4,4,4,3.5,3.75,11.25")

c_swap(line,
    "Arabic,483,M,A,16314&16484_S.txt,Investing-Science Funding,A,F10wk15,2,26,2:26,4,3.5,3.75,4,4,4,3.5,4,3.75,11.5",
    "Arabic,483,M,A,16314&16483_S.txt,Investing-Science Funding,A,F10wk15,2,26,2:26,4,3.5,3.75,4,4,4,3.5,4,3.75,11.5")

c_swap(line,
    "Arabic,320,M,B,16320&16236_S.txt,Investing-Science Funding,A,F10wk15,2,24,2:29,4,4,4,4,4,4,4,4,4,12",
    "Arabic,320,M,B,16320&16235_S.txt,Investing-Science Funding,A,F10wk15,2,24,2:29,4,4,4,4,4,4,4,4,4,12")

c_swap(line,
    "Chinese,399,M,B,20571&20399_A.txt,PSWOT-Barbershop,S,F10wk10,2,5,2:55,3,3,3,3,3,3,2,2,2,8",
    "Chinese,399,M,B,20573&20399_A.txt,PSWOT-Barbershop,S,F10wk10,2,5,2:55,3,3,3,3,3,3,2,2,2,8")
c_swap(line,
    "Chinese,573,F,A,20571&20399_A.txt,PSWOT-Barbershop,S,F10wk10,2,5,2:55,3,3,3,3,3,3,2,2,2,8",
    "Chinese,573,F,A,20573&20399_A.txt,PSWOT-Barbershop,S,F10wk10,2,5,2:55,3,3,3,3,3,3,2,2,2,8")

c_swap(line,
    "Arabic,230,F,B,22230&22219_S.txt,SWOT-Selecting a Store to Open,S,Sum12wk10,2,40,2:44,4,4,4,3.5,3.5,3.5,4,4,4,11.5",
    "Arabic,230,F,B,22230&22229_S.txt,SWOT-Selecting a Store to Open,S,Sum12wk10,2,40,2:44,4,4,4,3.5,3.5,3.5,4,4,4,11.5")

c_swap(line,
    "Arabic,71,M,A,2298&22071_S.txt,SWOT-Selecting a Store to Open,S,F12wk14,2,5,2:58,3.5,3,3.25,3,2.5,2.75,3,2.5,2.75,8.75",
    "Arabic,71,M,A,22298&22071_S.txt,SWOT-Selecting a Store to Open,S,F12wk14,2,5,2:58,3.5,3,3.25,3,2.5,2.75,3,2.5,2.75,8.75")
c_swap(line,
    "Arabic,298,M,B,2298&22071_S.txt,SWOT-Selecting a Store to Open,S,F12wk14,2,5,2:58,3.5,3,3.25,3,2.5,2.75,3,2.5,2.75,8.75",
    "Arabic,298,M,B,22298&22071_S.txt,SWOT-Selecting a Store to Open,S,F12wk14,2,5,2:58,3.5,3,3.25,3,2.5,2.75,3,2.5,2.75,8.75")

c_swap(line,
    "Arabic,42,M,B,23042&23082_A.txt,Music & Vocabulary,S,F09wk15,3,58,1:31,2,2,2,3,2,2.5,3,3,3,7.5",
    "Arabic,42,M,B,23042&23482_A.txt,Music & Vocabulary,S,F09wk15,3,58,1:31,2,2,2,3,2,2.5,3,3,3,7.5")
c_swap(line,
    "Arabic,482,M,A,23042&23082_A.txt,Music & Vocabulary,S,F09wk15,3,58,1:31,3,2,2.5,2,2,2,3,3,3,7.5",
    "Arabic,482,M,A,23042&23482_A.txt,Music & Vocabulary,S,F09wk15,3,58,1:31,3,2,2.5,2,2,2,3,3,3,7.5")

c_swap(line,
    "Arabic,152,M,B,23319&23512_B.txt,Nonverbal Communication,S,F10wk15,3,72,2:52,4,4,4,4,4,4,4,4,4,12",
    "Arabic,152,M,B,23319&23152_B.txt,Nonverbal Communication,S,F10wk15,3,72,2:52,4,4,4,4,4,4,4,4,4,12")
c_swap(line,
    "Arabic,319,M,A,23319&23512_B.txt,Nonverbal Communication,S,F10wk15,3,72,2:52,4,4,4,4,4,4,4,4,4,12",
    "Arabic,319,M,A,23319&23152_B.txt,Nonverbal Communication,S,F10wk15,3,72,2:52,4,4,4,4,4,4,4,4,4,12")

c_swap(line,
    "Japanese,585,F,A,24585&24585_S.txt,Workplace Monitoring,S,SU10wk10,3,13,3:13,4,4,4,3,3,3,3,3,3,10",
    "Japanese,585,F,A,24585&24555_S.txt,Workplace Monitoring,S,SU10wk10,3,13,3:13,4,4,4,3,3,3,3,3,3,10")
c_swap(line,
    "Chinese,555,M,B,24585&24585_S.txt,Workplace Monitoring,S,SU10wk11,3,13,3:13,4,4,4,3,3,3,3,3,3,10",
    "Chinese,555,M,B,24585&24555_S.txt,Workplace Monitoring,S,SU10wk11,3,13,3:13,4,4,4,3,3,3,3,3,3,10")
    
# now for the multiples... ??? 

c_swap(line,
    "Chinese,376,F,A,18380&18376_S.txt,Presentation-Immigration,S,F09wk15,2,47,2:19,1,1,1,1,1,1,2,2,2,4",
    "Chinese,376,F,A,19380&19376_S.txt,Presentation-Immigration,S,F09wk15,2,47,2:19,1,1,1,1,1,1,2,2,2,4")
c_swap(line,
    "Chinese,380,M,B,18380&18376_S.txt,Presentation-Immigration,S,F09wk15,2,47,2:19,1,1,1,1,1,1,2,2,2,4",
    "Chinese,380,M,B,19380&19376_S.txt,Presentation-Immigration,S,F09wk15,2,47,2:19,1,1,1,1,1,1,2,2,2,4")


# batch 2 .... for some reason....
c_swap(line,
    "Arabic,269,M,B,23296&23540_B.txt,Crime & economy,S,Sp10wk9,3,27,2:15,3.5,3.5,3.5,3.5,3.5,3.5,3,3.5,3.25,10.25",
    "Arabic,296,M,B,23296&23540_B.txt,Crime & economy,S,Sp10wk9,3,27,2:15,3.5,3.5,3.5,3.5,3.5,3.5,3,3.5,3.25,10.25")


c_swap(line,
    "Arabic,230,F,A,16230&16230_S.txt,Investing-Science Funding,A,F10wk15,2,22,2:36,3.5,3.5,3.5,3.5,4,3.75,4,4,4,11.25",
    "Arabic,230,F,A,16230&16229_S.txt,Investing-Science Funding,A,F10wk15,2,22,2:36,3.5,3.5,3.5,3.5,4,3.75,4,4,4,11.25")


c_swap(line,
    "Arabic,304,M,B,23374&23304_C.txt,Nonverbal Communication,S,F10wk15,3,66,3:06,5,5,5,4,5,4.5,5,4,4.5,14",
    "Arabic,304,M,B,23374&23304_B.txt,Nonverbal Communication,S,F10wk15,3,66,3:06,5,5,5,4,5,4.5,5,4,4.5,14")


line = input_file.readline()

while line:
    found = False # not pretty,,,, but
    for key, value in changes.items():
        if line.startswith(key):
            output_file.write(value + "\n")
            found = True
            break
    if not found:
        output_file.write(line)
        

    line = input_file.readline()


