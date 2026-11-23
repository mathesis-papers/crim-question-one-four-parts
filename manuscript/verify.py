import argparse
from collections import Counter
from functools import cache
from itertools import combinations_with_replacement
import json


APPENDIX_A = (
    (4, 2, 2, 2), (6, 2, 2, 2), (6, 4, 1, 1), (6, 3, 2, 2),
    (6, 4, 2, 1), (4, 4, 3, 3), (6, 4, 2, 2), (6, 6, 1, 1),
    (8, 2, 2, 2), (8, 4, 1, 1), (6, 4, 3, 2), (6, 5, 3, 1),
    (5, 4, 2, 2, 1), (5, 3, 3, 2, 2), (5, 3, 2, 2, 2), (5, 3, 3, 2, 1),
    (8, 3, 2, 2), (8, 4, 2, 1), (8, 6, 1, 1), (10, 2, 2, 2),
    (6, 4, 3, 3), (6, 4, 4, 2), (8, 4, 2, 2), (8, 5, 2, 1),
    (7, 3, 2, 2, 2), (7, 3, 3, 2, 1), (7, 4, 2, 2, 1), (7, 4, 3, 1, 1),
    (6, 3, 2, 2, 1, 1), (6, 2, 2, 2, 2, 2), (6, 3, 2, 2, 2, 1),
    (6, 4, 2, 2, 1, 1), (6, 2, 2, 2, 1, 1), (8, 2, 2, 2, 1, 1),
    (8, 4, 1, 1, 1, 1), (7, 5, 2, 1, 1), (5, 5, 2, 2, 2), (10, 4, 1, 1))


def conjugate(position):
    return tuple(sum(part >= column for part in position)
                 for column in range(1, max(position, default=0) + 1))


def source_moves(position):
    rows = {position[:index] + position[index + 1:]
            for index in range(len(position))}
    dual = conjugate(position)
    columns = {conjugate(dual[:index] + dual[index + 1:])
               for index in range(len(dual))}
    return rows | columns


def height_moves(position):
    followers = {position[:index] + position[index + 1:]
                 for index in range(len(position))}
    for height in range(1, len(position) + 1):
        next_part = position[height] if height < len(position) else 0
        if position[height - 1] > next_part:
            followers.add(tuple(part - (index < height)
                                for index, part in enumerate(position)
                                if part - (index < height) > 0))
    return followers


@cache
def grundy(position):
    values = {grundy(follower) for follower in source_moves(position)}
    candidate = 0
    while candidate in values:
        candidate += 1
    return candidate


def four_original(first, second, third, fourth):
    return first % 2 == 0 and (
        (fourth >= 2 and not (second % 2 == third % 2 == 1))
        or (fourth == third == 1 and (second % 2 == 0 or second == 1))
        or (fourth == 1 and third >= 2 and second % 2 == 1)
        or (fourth == 1 and third == 2 and (second >= 3 or first == 2)))


def mehat_four(first, second, third, fourth):
    if first % 2:
        return False
    if second % 2 == 0:
        if third % 2 == 0:
            return (fourth % 2 == 0 or fourth >= 3
                    or (third == fourth + 1 and (second > third or first == second)))
        return fourth % 2 == 0 or third == fourth or fourth >= 3
    if third % 2 == 0:
        return True
    return fourth == 1 and (third >= 3 or second == third == 1)


def classified_losing(position):
    if not position:
        return True
    first = position[0]
    if len(position) == 1:
        return False
    second = position[1]
    if len(position) == 2:
        return first % 2 == 0
    third = position[2]
    if len(position) == 3:
        return (first > 1 and first % 2 == second % 2 == 1
                and (third > 1 or second == 1))
    fourth = position[3]
    if first % 2:
        return False
    if fourth >= 2:
        return not (second % 2 == third % 2 == 1)
    if third == 1:
        return second == 1 or second % 2 == 0
    if third == 2:
        return second >= 3 or first == 2
    return second % 2 == 1


def winning_move(position):
    first, second, third, fourth = position
    if first % 2 == 0:
        if fourth > 1:
            return 1, (second, third, fourth)
        if third == 1:
            return 2, (second, 1, 1)
        return 3, tuple(part - 1 for part in position if part > 1)
    if first == 1:
        return 4, ()
    if third == 1:
        if second == 1:
            return 5, (first - 1, 1, 1, 1)
        return 6, (first, 1, 1)
    if second % 2:
        return 7, (first, second, third)
    if fourth > 1:
        if third % 2:
            return 8, (first, third, fourth)
        return 9, (first - 1, second, third, fourth)
    if third % 2:
        return 10, (first - 1, second - 1, third, 1)
    if third >= 4:
        return 11, (first - 1, second - 1, third - 1, 1)
    if second == 2:
        return 12, (first - 1, 1, 1, 1)
    return 13, (first - 1, second, 2, 1)


def verify(max_part):
    counts = Counter()
    branches = Counter()
    for length in range(5):
        for increasing in combinations_with_replacement(range(1, max_part + 1), length):
            position = tuple(reversed(increasing))
            moves = source_moves(position)
            assert conjugate(conjugate(position)) == position, position
            assert moves == height_moves(position), position
            assert all(sum(follower) < sum(position) for follower in moves), position
            expected = classified_losing(position)
            assert (grundy(position) == 0) == expected, position
            assert expected == all(not classified_losing(follower) for follower in moves), position
            counts[f'positions_{length}_parts'] += 1
            if length == 4:
                assert expected == four_original(*position), position
                assert expected == mehat_four(*position), position
                if expected:
                    counts['losing_four_part_positions'] += 1
                else:
                    branch, follower = winning_move(position)
                    assert follower in moves and classified_losing(follower), (position, branch)
                    branches[str(branch)] += 1
            if expected:
                assert (first_rank := abs(length - max(position, default=0))) % 2 == 0, (position, first_rank)
            elif position and (max(position) - length) % 2 == 0:
                top_row = position[1:]
                first_column = tuple(part - 1 for part in position if part > 1)
                assert classified_losing(top_row) or classified_losing(first_column), position
                row_gap = position[0] - (position[1] if length > 1 else 0)
                dual = conjugate(position)
                column_gap = dual[0] - (dual[1] if len(dual) > 1 else 0)
                assert row_gap % 2 or column_gap % 2, position
            if length == 2:
                first, second = position
                padded = (first, first, first, second)
                appended = (first, second, 1, 1)
                assert classified_losing(padded) == (first % 2 == 0 and (second >= 2 or first == 2))
                assert classified_losing(appended) == (first % 2 == 0 and (second == 1 or second % 2 == 0))
    assert len(branches) == 13
    sibling_counts = Counter()
    for first in range(1, max_part + 1):
        one_part_answer = first > 1 and first % 2 == 1
        assert (grundy((first, first, first)) == 0) == one_part_answer
        assert (grundy((first, 1, 1)) == 0) == one_part_answer
        assert grundy((first,)) != 0
        sibling_counts['one_part_inputs'] += 1
    for rows in range(2, 5):
        for columns in range(2, max_part + 1):
            if rows % 2 != columns % 2:
                continue
            for inner_rows in range(rows):
                for increasing in combinations_with_replacement(range(1, columns), inner_rows):
                    inner = tuple(reversed(increasing))
                    if grundy(inner) != 0:
                        continue
                    stacked = ((columns,) + tuple(part + 1 for part in inner)
                               + (1,) * (rows - inner_rows - 1))
                    assert grundy(stacked) == 0, (rows, columns, inner)
                    assert grundy(conjugate(stacked)) == 0, stacked
                    sibling_counts['hook_stack_instances'] += 1
                    if inner:
                        sibling_counts[f'hook_stack_{rows}_{inner_rows}'] += 1
    for columns in range(3, max_part + 1, 2):
        position = (columns, 2, 1)
        assert grundy(position) != 0 and grundy(position[1:]) == 0
        sibling_counts['odd_hook_stacks_ending_in_one'] += 1
    assert grundy((1,)) == grundy((3, 2, 1)) == 1
    assert {grundy(follower) for follower in source_moves((3, 2, 1))} == {0, 3}
    appendix_four_rows = []
    for index, position in enumerate(APPENDIX_A, 1):
        assert grundy(position) == 0, ('Appendix A', index, position)
        if len(position) == 4:
            assert classified_losing(position)
            appendix_four_rows.append(index)
    assert appendix_four_rows == list(range(1, 13)) + list(range(17, 25)) + [38]
    examples = {str(position): grundy(position) for position in
                [(), (1, 1, 1), (2, 2, 2, 1), (4, 2, 2, 1), (4, 3, 3, 2), (6, 4, 3, 2)]}
    return {'max_part': max_part, 'max_rows': 4, 'counts': dict(sorted(counts.items())),
            'sibling_counts': dict(sorted(sibling_counts.items())),
            'appendix_a': {'positions': len(APPENDIX_A),
                           'four_row_diagram_numbers': appendix_four_rows,
                           'other_finite_losing_positions': 17},
            'strategy_case_counts': dict(sorted(branches.items(), key=lambda item: int(item[0]))),
            'examples_grundy': examples, 'checks': [
                'source moves equal row/height moves', 'conjugation is involutive',
                'every move decreases cell count', 'classification equals exact mex outcome',
                'classification satisfies both transition conditions',
                'all thirteen winning-move cases have legal losing followers',
                'disjoint table equals the four-clause formula',
                'classification agrees with Mehat Theorem 4 parity table',
                'even-rank and first-row/first-column consequences',
                'two-part padding and appending formulas',
                'one-part padding and appending formulas',
                'losing-hook stacking with at most four rows and conjugates',
                'odd-hook stacks ending in one with at most four rows',
                'Conjecture 2 boundary has Grundy value one',
                '2022 staircase conjecture has boundary exceptions at one and three',
                'all 38 Appendix A diagrams have Grundy value zero'], 'status': 'ALL_CHECKS_OK'}


def main():
    parser = argparse.ArgumentParser(description='Exact finite checks for four-part CRIM.')
    parser.add_argument('--max-part', type=int, default=30)
    arguments = parser.parse_args()
    if not 6 <= arguments.max_part <= 40:
        parser.error('--max-part must be between 6 and 40')
    print(json.dumps(verify(arguments.max_part), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
