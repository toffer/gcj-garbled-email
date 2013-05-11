#!/usr/bin/env python

import datrie
import os
import string
import sys

EMAIL_DICT_FILE = 'garbled_email_dictionary.txt'
WILDCARDS_FILE = 'wildcards_dictionary.txt'


def read(filename):
    """Yield a "test" chunk of lines from filename."""
    with open(filename, 'r') as f:
        num_tests = int(f.readline())
        for t in range(num_tests):
            yield f.readline()

def munge(test_chunks):
    """Output list of vars that are used as input to solve()."""
    for chunk in test_chunks:
        yield [chunk.strip()]

def format(index, result):
    """Format output properly."""
    return "Case #%s: %s" % (index, result)

def word_variations(word):
    variations = [word]
    for i in range(len(word)):
        tmp = list(word)
        tmp[i] = u'*'
        variations.append(''.join(tmp))
    if len(word) > 5:
        for i in range(len(word) - 5):
            tmp = list(word)
            tmp[i] = u'*'
            tmp[i + 5] = '*'
            variations.append(''.join(tmp))
    if len(word) > 10:
        for i in range(len(word) - 10):
            tmp = list(word)
            tmp[i] = u'*'
            tmp[i + 5] = '*'
            tmp[i + 10] = '*'
            variations.append(''.join(tmp))
    return variations

def make_trie(filename):
    valid_chars = string.ascii_lowercase + '*'
    trie = datrie.BaseTrie(valid_chars)
    with open(filename) as f:
        for line in f:
            word = line.strip().decode('utf-8')
            trie[word] = 0
    return trie

def indexed_variations(word, wildcards_trie):
    """
    Build data structure of matching words from trie.

    Return array of arrays:
        d[index][list of matching words in wildcards_trie]

    """
    wlist = list(word)
    data = [[] for x in range(len(wlist))]
    for i in range(len(wlist)):
        data[i] = []
        search_deeper = True
        j = i + 1
        while search_deeper:
            segment = ''.join(wlist[i:j]).decode('utf-8')
            segments = word_variations(segment)
            search_deeper_count = len(segments)
            for s in segments:
                if s in wildcards_trie:
                    data[i].append(s)
                if j >= len(wlist) or not wildcards_trie.has_keys_with_prefix(s):
                    search_deeper_count -= 1

                if search_deeper_count > 0:
                    search_deeper = True
                else:
                    search_deeper = False
            j += 1
    return data

def is_valid(candidate):
    """Do all wildcards have at least 5 char separation?"""
    indexes = [i for i in range(len(candidate)) if candidate.startswith('*', i)]
    if len(indexes) < 2:
        return True

    last = indexes.pop()
    while indexes:
        prev = indexes.pop()
        if last - prev < 5:
            return False
        last = prev
    return True

def add_valid(candidate, best_list):
    c_index = candidate.find('*')
    if 0 <= c_index <= 4:
        match_list = [x for x in best_list if x.find('*') == c_index]
    else:
        match_list = [x for x in best_list if x.find('*') == -1 or x.find('*') > 4]

    if match_list:
        match = match_list[0]
        if candidate.count('*') < match.count('*'):
            best_list.remove(match)
            best_list.append(candidate)
    else:
        best_list.append(candidate)
    return best_list

def find_best(candidates, solutions):
    word_length = len(solutions) + 1
    best = []
    best_score = word_length
    if not solutions:
        best = [u'*']
        for c in candidates:
            if c.count('*') < best.count('*'):
                best = [c]
    else:
        for c in candidates:
            c_len = len(c)
            if c_len == word_length:
                # Don't have to combine with solutions if c_len == word_length
                if c.count('*') == 0:
                    best = [c]
                    break
                else:
                    best = add_valid(c, best)
            else:
                index = len(solutions) - c_len
                for s in solutions[index]:
                    new_candidate = c + s 
                    if is_valid(new_candidate):
                        best = add_valid(new_candidate, best)
    return best

def solve(word, trie):
    variations = indexed_variations(word, trie)

    solutions = []
    while variations:
        last = variations.pop()
        best = find_best(last, solutions)
        solutions.append(best)
    finals = solutions[-1]
    # print sorted(finals, key=lambda x: x.count('*'))[0]
    return min([x.count('*') for x in finals])

def main(argv=None):
    if argv == None:
        argv = sys.argv

    if len(argv) != 2:
        sys.stderr.write("Usage: %s <input_file>" % argv[0])
        return 2

    # Generate "wildcards_dictionary.txt" just one time.
    if not os.path.isfile(WILDCARDS_FILE):
        with open(EMAIL_DICT_FILE) as f:
            deduped = set()
            for line in f:
                for v in word_variations(line.strip()):
                    deduped.add(v)
        with open(WILDCARDS_FILE, 'w') as wild:
            # Adding to trie is more efficient with sorted input.
            sorted_deduped = sorted(list(deduped))
            for word in sorted_deduped:
                wild.write(word + '\n')


    trie = make_trie(WILDCARDS_FILE)

    infile = argv[1]
    raw = read(infile)
    munged = munge(raw)

    for index, test in enumerate(munged):
        test.append(trie)
        print format(index + 1, solve(*test))

if __name__ == '__main__':
    main()
