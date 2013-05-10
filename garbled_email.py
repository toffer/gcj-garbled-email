#!/usr/bin/env python

import datrie
import os
import string
import sys

from pprint import pprint

EMAIL_DICT_FILE = 'garbled_email_dictionary.txt'
WILDCARDS_FILE = 'wildcards_dictionary.txt'


def read(filename):
    """Yield a "test" chunk of lines from filename."""
    with open(filename, 'r') as f:
        num_tests = int(f.readline())
        for t in range(num_tests):
            yield f.readline()

def munge(test_chunks):
    """Output vars that are used as input to solve()."""
    for chunk in test_chunks:
        yield chunk.strip()

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

def add_if_best(word, data_list):
    w_len = len(word)
    for d in data_list:
        d_len = len(d)
        if w_len == d_len:
            if word.count('*') < d.count('*'):
                data_list.remove(d)
                data_list.append(word)
            return data_list
    data_list.append(word)
    return data_list


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
        # if i == len(wlist) - 1:
        #     continue
        search_deeper = True
        j = i + 1
        # print '=== %s ===' % i
        while search_deeper:
            segment = ''.join(wlist[i:j]).decode('utf-8')
            segments = word_variations(segment)
            # print segment
            # print segments
            search_deeper_count = len(segments)
            for s in segments:
                # print s
                if s in wildcards_trie:
                    # print 's in trie'
                    data[i].append(s)
                    # data[i] = add_if_best(s, data[i])
                # if j >= len(wlist):
                #     print 'j > len(wlist)'
                #     # search_deeper = False
                #     search_deeper_count -= 1
                # if (search_deeper and 
                #     not wildcards_trie.has_keys_with_prefix(s)):
                #     print 's is not prefix'
                #     search_deeper = False
                if j >= len(wlist) or not wildcards_trie.has_keys_with_prefix(s):
                    # print 's is not >= len(wlist) or not prefix'
                    search_deeper_count -= 1
                if search_deeper_count > 0:
                    search_deeper = True
                else:
                    search_deeper = False
                # print '---'
            j += 1

    # Now, prune data so we only have best candidate of each length....
    # No sense checking 'p*', if 'pr' is a better option.
    # for i in range(len(data)):

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
    # print candidate, best_list
    c_index = candidate.find('*')
    if 0 <= c_index <= 4:
        match_list = [x for x in best_list if x.find('*') == c_index]
        if match_list:
            match = match_list[0]
            if candidate.count('*') < match.count('*'):
                best_list.remove(match)
                best_list.append(candidate)
        else:
            best_list.append(candidate)
    else:
        match_list = [x for x in best_list if x.find('*') == -1 or x.find('*') > 4]
        if match_list:
            match = match_list[0]
            if candidate.count('*') < match.count('*'):
                best_list.remove(match)
                best_list.append(candidate)
        else:
            best_list.append(candidate)
    # print best_list
    # print "---"
    return best_list

    # if len(best_list) == 1 and best_possible(best_list[0]):
    #     pass
    # elif not best_list or best_possible(candidate):
    #     best_list = [candidate]
    # else:
    #     c_index = candidate.find('*')
    #     b_indexes = [x.find('*') for x in best_list]
    #     if c_index not in b_indexes:
    #         best_list.append(candidate)
    # print best_list
    # print "---"
    # return best_list

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
        # best = '* | ' + solutions[-1]
        # best = '*' + solutions[-1]
        # best_score = best.count('*')
        # for c in candidates:
        #     c_len = len(c)
        #     if c_len == word_length:
        #         c_score = c.count('*')
        #         if c_score < best_score:
        #             best_score = c_score
        #             best = c
        #     else:
        #         index = len(solutions) - c_len 
        #         # new_candidate = c + ' | ' + solutions[index]
        #         new_candidate = c + solutions[index]
        #         new_candidate_score = new_candidate.count('*')
        #         if new_candidate_score < best_score:
        #             best_score = new_candidate_score
        #             best = new_candidate
        for c in candidates:
            c_len = len(c)
            if c_len == word_length:
                # Don't have to combine with solutions if c_len == word_length
                if c.count('*') == 0:
                    best = [c]
                    break
                else:
                    best = add_valid(c, best)
                # c_score = c.count('*')
                # FIXME: best_score is bullshit!
                # compare to best score in best list
                # if c_score < best_score:
                #     best_score = c_score
                #     best = [c]
            else:
                index = len(solutions) - c_len
                for s in solutions[index]:
                    new_candidate = c + s 
                    if is_valid(new_candidate):
                        best = add_valid(new_candidate, best)

    return best

def solve2(word, trie):
    variations = indexed_variations(word, trie)
    # pprint(variations)

    solutions = []
    while variations:
        last = variations.pop()
        # print "last", last
        best = find_best(last, solutions)
        solutions.append(best)
        # print best
        # print "solutions", solutions
    # print solutions[-1]
    finals = solutions[-1]
    # print sorted(finals, key=lambda x: x.count('*'))[0]
    return min([x.count('*') for x in finals])
    # return solutions[-1].count('*')




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
        print format(index + 1, solve2(test, trie))

if __name__ == '__main__':
    main()



