from utils.naive_levenshtein import get_probs, get_count, get_suggestions


# def suggestion_adequacy_ns(test_set: str, verbose: bool = False):
#     """
#         For the naive levenshtein model
#         Number of correct suggestions for invalid words for all the invalid words
#         Also print the speed to do all the suggestions
#         Parameters
#         ----------
#             test_set: List[str]
#                 File used to test systems
#             verbose: bool
#                 Display or not correction for each word
#         Returns
#         ----------
#             Prints reports
#         """
#
#     dataset = pairing(test_set)
#
#     probs = get_probs(get_count(vocab))
#
#     good, unknown = 0, 0
#     unknown_words = set()
#
#     n = len(dataset)
#
#     start = time.time()
#
#     for right, wrong in dataset:
#         suggestion = (get_suggestions(wrong, probs, vocab))[0][0]
#         good += (suggestion == right)
#         if suggestion != right:
#             if right not in vocab:
#                 unknown_words.add(right)
#                 unknown += 1
#             if verbose:
#                 print('autocorrection({}) => {}; expected {}'.format(wrong, suggestion, right))
#
#     dt = time.time() - start
#
#     print('Naive Levenshtein Suggestion Adequacy: {:.2%} ({}) of {} invalid words successfully corrected '
#           '({:.2%} unknown valid words) in {:.0f} second'.format(good / n, good, n, unknown / n, n / dt))
#     if unknown_words:
#         print('List of valid words not in the lexicon: ', unknown_words)

