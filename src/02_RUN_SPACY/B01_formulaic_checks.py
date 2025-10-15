
import re

"""
 This file is for constants of formulaic lists. Lists are tuples of
   (pattern, compare_function)
where the pattern is the string to compare, and the function is how it
is to be compared. this is to allow multiple comparison methods for one
list so they can all be grouped under a single formulaic type.

"""

#============================================================================#
# compare functions
#============================================================================#
def _string_match(pattern, chunk):
    """
    simple string compare. done for polymorphism of matching
    
    Args:
        pattern (str): a raw or escaped regular expression
        chunk (str): the chunk of text to be searched

    Returns:
        (boolean) whether there was a match or not
    """

    return chunk.strip().lower() == pattern

def _regex_match(pattern, chunk):
    """
    matches the regular expression pattern to the chunk of text using fullmatch,
    so the match has to be exact to the string.

    Args:
        pattern (str): a raw or escaped regular expression
        chunk (str): the chunk of text to be searched

    Returns:
        (re.Match object|None) whether the match was true or not (boolean)
    """

    return re.fullmatch(pattern, chunk.strip().lower())


#============================================================================#
# lists of formulaics as contstants
#============================================================================#

FORMULAIC_greetings = [
    ("thank you", _string_match),
    ("good morning", _string_match),
    ("good night", _string_match),
    ("of course", _string_match)
]

FORMULAIC_two_word_patterns = [
    (r"^(hello|um|oh|uh)\,?\s[a-z]+$", _regex_match)
]


#============================================================================#
# functions
#============================================================================#

def _check_formulaic_list(flist, chunk):
    """
    checks a list of formulaic patterns and functions against a chunk. if any
    match, return True, else False

    Args:
        flist (list<tup<str,func>>): list of pattern, compare_function tups
        chunk (str): the string to test
    Returns 
        (boolean): True if any of flist match
    """
    for p_tup in flist:
        if p_tup[1](p_tup[0], chunk):
            return True
    return False


def is_formulaic(chunk):
    """
    checks if a chunk is formulaic.

    Args:
        chunk (str): the chunk to test 

    Returns:
        (boolean): returns whether or not the chunk is consider formulaic
    """
            
    # new criteria is just word length [1, 2]
    if len(chunk.strip().split()) <= 2:
        return True
    return False


def is_formulaic_OLD(chunk):
    """
    checks if a chunk is formulaic.
    THIS IS NOT BEING USED CURRENTLY -- NOAH ONLY WANTS A LONG LIST NOW

    Args:
        chunk (str): the chunk to test 

    Returns:
        (tup<boolean,(str|None)>): True if formulaic, with str descriptor for type of
                            formulaic, False and None otherwise
    """
            
    # first, do one word tests
    if len(chunk.strip().split()) == 1:
        return True, "one_word_only"

    # call the various constant lists of patterns to check and return if they
    # match anything.
    if _check_formulaic_list(FORMULAIC_greetings, chunk):
        return True, "greetings/goodbyes"
    elif _check_formulaic_list(FORMULAIC_two_word_patterns, chunk):
        return True, "two_word_patterns"
    else:
        # no match found
        return False, None
    

