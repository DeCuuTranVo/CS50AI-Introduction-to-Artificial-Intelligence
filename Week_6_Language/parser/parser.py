import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP
NP -> N | Det N | Det Adj N | Det Adj Adj N | Det Adj Adj Adj N | N P N | Adj N | N N | Adj NP | NP P NP 
VP -> V |V NP | V Adv | V P NP | Adv VP | VP Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    from nltk.tokenize import word_tokenize
    # split sentence to words
    token_list = word_tokenize(sentence) 
    
    # converting all characters to lowercase
    lowercase_list = [x.lower() for x in token_list]

    # removing any word that does not contain at least one alphabetic character.
    alphabet_list = [] 
    for item in lowercase_list:
        if item.isalpha():
            alphabet_list.append(item)
    
    return alphabet_list


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Create a return list    
    subtree_list = []
    
    # Generate subtrees with label "NP" from the sentence tree
    for subtree in tree.subtrees(filter=lambda t: t.label() == "NP"):   
        # All direct subtree of this subtree should not have the "NP" label
        # Direct subtree means subtree with one layer shallower from the current subtree
        NP_flag = True
        for subsubtree in subtree.subtrees(filter=lambda t: t.height() == subtree.height()-1):
            if subsubtree.label() == "NP":
                NP_flag = False
                
        if NP_flag == True:
            subtree_list.append(subtree)
            
    # Return the return list
    return subtree_list


if __name__ == "__main__":
    main()
