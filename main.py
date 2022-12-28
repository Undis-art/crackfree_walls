# Project Euler, problem 215: Crack-free Walls

MAX_LENGTH = 32
DEPTH = 10

def main():

    all_rows = find_all_rows(MAX_LENGTH)
    matching_rows = find_matching_rows(all_rows)

    n_possibles_per_depth = {}

    for i in range(2, DEPTH+1):
        compute_n_possible_walls(
            i,
            len(all_rows),
            matching_rows,
            n_possibles_per_depth
        )

    n_layouts = sum(n_possibles_per_depth[DEPTH])

    print("n_layouts for depth " + str(DEPTH) +
            " and length " + str(MAX_LENGTH) +
            ": " + str(n_layouts))


def find_all_rows(max_length):
    """
    Find all tile rows of length max_length.
    Tiles are of length 2 or 3 each.

    VALUE
    list of lists. Each inner list is a list of growing
    integers and represents a tile row. Each number
    represents the location of tile-end.
    """

    def _finish_rows(row, max_length, ready_rows):
        if row[-1] in (max_length - 3, max_length - 2):
            # 2 or 3 length units to end: row is ready!
            ready_rows.append(row)
        elif row[-1] == max_length - 4:
            # 4 length units to end: must add tile 2,
            # then row is ready.
            row.append(row[-1] + 2)
            ready_rows.append(row)
        else:
            # recursion
            subrow1 = row.copy()
            subrow1.append(row[-1] + 2)
            subrow2 = row.copy()
            subrow2.append(row[-1] + 3)
            _finish_rows(subrow1, max_length, ready_rows)
            _finish_rows(subrow2, max_length, ready_rows)

    all_rows = []
    seed1 = [2]
    seed2 = [3]
    _finish_rows(seed1, max_length, all_rows);
    _finish_rows(seed2, max_length, all_rows);

    return all_rows
    
def find_matching_rows(all_rows):
    """
    Per each row, list indices of rows that can be placed next to it.

    VALUE
    list of lists. List at index i holds indices of the rows that can
    be placed next to row i.
    """
    matching_rows = []

    for i in range(len(all_rows)):
        matches_for_i = []
        for j in range(len(all_rows)):
            intersection = [r for r in all_rows[i] if r in all_rows[j]]
            if not intersection:
                # No common locations of tile ends! Ok to place next to
                # each other.
                matches_for_i.append(j)
        matching_rows.append(matches_for_i)

    return matching_rows


def compute_n_possible_walls(
    depth,
    n_rows,
    matching_rows,
    n_possibles_per_depth
    ):
    """
    Holds the number of possible walls that have given depth
    (key) and are started out with a given row.

    ARGUMENTS
    n_rows -- int. Number of rows in all_rows
    depth -- int >= 2. depth (number of tile rows) for which to compute.
    matching_rows -- list of lists, as returned by matching_rows()
    n_possibles_per_depth -- dict. See INFO.

    INFO
    Modifies given dictionary n_possibles_per_depth.

    n_possibles_per_depth:
    key -- int. depth.
    value -- list of integers, as long as all_rows.
        Holds the number of possible walls that have given depth
        (key) and are started out with a given row.
    """
    if depth == 2:
        n_possibles = [
            len(matching_rows[i])
            for i in range(n_rows)
            ]
        n_possibles_per_depth[2] = n_possibles
        print("Precalculated for depth 2")
    elif not n_possibles_per_depth.get(depth):
        n_possibles = []
        for i in range(n_rows):
            possibles_for_i = 0
            for match in matching_rows[i]:
                possibles_for_i += n_possibles_per_depth[depth-1][match]
            n_possibles.append(possibles_for_i)
        n_possibles_per_depth[depth] = n_possibles # store for this depth
        print("Precalculated for depth " + str(depth))


if __name__ == "__main__":
    main()
