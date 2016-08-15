#!/usr/bin/python

import os
import sys
import time
import difflib
import argparse
import pickle
import get_trivia as gt

################ Description ##################
# Script to call a trivia API and ask the user questions

USAGE = """
----------------------------------------------------------
python block_head.py

<OR>

python block_head.py -hs
----------------------------------------------------------
"""

CURRENT_SCORE = 0

def create_args():
    '''Creates the Args at run time.'''
    parser = argparse.ArgumentParser(description='Simple trivia script, that uses a remote API.', usage=USAGE)
    parser.add_argument('-s', '--scores', help='- Flag to Show Past Player Scores.', action='store_true')
    args = parser.parse_args()
    return (args, parser)


def save_scores(player_name):
    '''Saves all scores, and updates current players'''
    if os.path.isfile('scores.pk'):
        current_dict = pickle.load(open("scores.pk", "rb"))
    else:# If its the first run time, it saves the first data.
        base_data = {player_name : CURRENT_SCORE}
        pickle.dump(base_data, open("scores.pk", "wb"))
        return
    if not os.path.isfile('scores.pk'):
        print 'Missing the Scores file, have you played the game?'
        return
    if current_dict.get(player_name):
        last_score = current_dict.get(player_name)
        if CURRENT_SCORE > last_score:
            print '%s, NEW HIGH SCORE --> %s' % (player_name, CURRENT_SCORE)
            current_dict[player_name] = CURRENT_SCORE
            pickle.dump(current_dict, open("scores.pk", "wb"))
    else:
        current_dict[player_name] = CURRENT_SCORE
        pickle.dump(current_dict, open("scores.pk", "wb"))
    print 'Saved Score Data for: %s --> %s' % (player_name, CURRENT_SCORE)


def print_scores():
    ''' prints past Player Scores.'''
    os.system('clear')
    print '#'*15 + ' High Scores (Top-5)' + '#'*15 + '\n'
    if os.path.isfile('scores.pk'):
        current_dict = pickle.load(open("scores.pk", "rb"))
    else:
        print 'Missing the Scores file, have you played the game?'
        return
    d_view = [(v, k) for k, v in current_dict.iteritems()]
    d_view.sort(reverse=True) # natively sort tuples by first element
    count = 0
    for value, key in d_view:
        print "\t%s\t\t--\t\t%d" % (key, value)
        count += 1
        if count >= 5:
            break
    print '\n' + '#'*50


def get_player_name():
    ''' Simple way to ask for the player name. '''
    return raw_input('Please Enter Player Name: ')


def calc_score(value, question_status):
    '''Figures out the current Score.'''
    global CURRENT_SCORE
    if not value:
        value = 100
    if question_status:
        CURRENT_SCORE += value
    else:
        CURRENT_SCORE -= value


def display_question(question, category, value):
    ''' Formats and displays the question to the user.'''
    os.system('clear')
    border_count = len(question)
    print '#' * border_count
    print 'Please Enter: Your Answer, Exit/Quit, or Pass' + '\n'
    print 'User Current Score: %s' % CURRENT_SCORE
    print 'Category: %s' % category
    print 'Question Value: %s' % value
    print '\t==> Question: %s' % question + '\n'
    print '#' * border_count + '\n'


def main():
    '''Main Calling function.'''
    args, parser = create_args()
    if args.scores:
        print_scores()
        sys.exit()
    player_name = get_player_name()
    try:
        while True:
            answer_status = False
            response = gt.trivia_caller()[0]
            question = response.get('question')
            answer = response.get('answer')
            answer_list_letters = list(answer)
            value = response.get('value')
            tmp_dict = response['category']
            category = tmp_dict.get('title')
            display_question(question, category, value)
            user_answer = raw_input('Please Enter an Answer: ')
            u_answer_list_letters = list(user_answer)
            if 'exit' in user_answer.lower() or 'quit' in user_answer.lower():
                break
            sm = difflib.SequenceMatcher(None,answer_list_letters, u_answer_list_letters)
            if sm.ratio() >= 0.5 and user_answer:
                answer_status = True
                print 'Correct! ==> Answer is:[%s], Points: %s, Answer Ratio: %s' % (answer, value, sm.ratio())
            else:
                print 'Incorrect/Passing, the answer is: %s' % answer

            if user_answer.lower() != 'pass':
                calc_score(value, answer_status)
            time.sleep(3)
    except KeyboardInterrupt:
        pass
    save_scores(player_name)

if __name__ == "__main__":
    sys.exit(main())
