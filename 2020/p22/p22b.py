import sys


def run_game(p1, p2):
    configurations = []
    # Game continue until one player has no card left OR the configuration has already been encounterd
    while p1 and p2 and (p1, p2) not in configurations:
        configurations.append((p1[:], p2[:]))
        top1, top2 = p1.pop(0), p2.pop(0)
        # Play recursive game
        if top1 <= len(p1) and top2 <= len(p2):
            winner, deck = run_game(p1[:top1], p2[:top2])
            if winner == 'p1':
                p1 += [top1, top2]
            else:
                p2 += [top2, top1]
        # Simple highest-value game
        else:
            if top1 > top2:
                p1 += [top1, top2]
            else:
                p2 += [top2, top1]
    return ('p1', p1) if p1 or (p1, p2) in configurations else ('p2', p2)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing input file: python {} file.".format(sys.argv[0]))
        sys.exit()

    with open(sys.argv[1]) as f:
        lines = f.read().splitlines()

    p1_idx = lines.index('Player 1:')
    p2_idx = lines.index('Player 2:')
    p1 = [int(line) for line in lines[p1_idx + 1: p2_idx - 1]]
    p2 = [int(line) for line in lines[p2_idx + 1:]]

    winner, deck = run_game(p1, p2)
    score = sum([(i + 1) * value for i, value in enumerate(reversed(deck))])
    print(score)
