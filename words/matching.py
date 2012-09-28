'''
Created on 28-09-2012

@author: pawel
'''

import difflib

def match_answers(student_answer, answer):
    matcher = difflib.SequenceMatcher(lambda x: x == " ", student_answer, answer)
    ratio = int(matcher.ratio() * 100)
    opcodes = matcher.get_opcodes()
    
    ret = [ratio]
    
    for opcode in opcodes:
        if opcode[0] == 'replace':
            ret.append(['deleted', student_answer[opcode[1]:opcode[2]]])
            ret.append(['inserted', answer[opcode[3]:opcode[4]]])
        elif opcode[0] == 'equal':
            ret.append(['left', student_answer[opcode[1]:opcode[2]]])
        elif opcode[0] == 'insert':
            ret.append(['inserted', answer[opcode[3]:opcode[4]]])
        elif opcode[0] == 'delete':
            ret.append(['deleted', student_answer[opcode[1]:opcode[2]]])
            
    return ret

if __name__ == '__main__':
    #completely diffirent strings
    student_answer = 'b'
    answer = 'a'
    
    result = match_answers(student_answer, answer)
    
    print result
    print (result == [0, ['deleted', 'b'], ['inserted', 'a']])
    
    #not finished answer
    student_answer = 'ab'
    answer = 'abc'
    
    result = match_answers(student_answer, answer)
    
    print result
    print (result == [80, ['left', 'ab'], ['inserted', 'c']])
    
    #not started answer
    student_answer = 'bc'
    answer = 'abc'
    
    result = match_answers(student_answer, answer)
    
    print result
    print (result == [80, ['inserted', 'a'], ['left', 'bc']])
    
    #lach of chars in the middle
    student_answer = 'ac'
    answer = 'abbc'
    
    result = match_answers(student_answer, answer)
    
    print result
    print (result == [66, ['left', 'a'], ['inserted', 'bb'], ['left', 'c']])
    
    #to many chars in the beginning
    student_answer = 'preabc'
    answer = 'abc'
    
    result = match_answers(student_answer, answer)
    
    print result
    print (result == [66, ['deleted', 'pre'], ['left', 'abc']])
    
    #to many chars in the end
    student_answer = 'abcpost'
    answer = 'abc'
    
    result = match_answers(student_answer, answer)
    
    print result
    print (result == [60, ['left', 'abc'], ['deleted', 'post']])
    
    #to many chars in the midle
    student_answer = 'abmiddlec'
    answer = 'abc'
    
    result = match_answers(student_answer, answer)
    
    print result
    print (result == [50, ['left', 'ab'], ['deleted', 'middle'], ['left', 'c']])
    