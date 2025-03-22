from src.domains.policies.validations import can_topologically_sort


def test_can_topologically_sort_returns_true_for_dag():
    adjacency_dict = {
        1: [2, 3],  # Node 1 points to Node 2 and Node 3
        2: [4, 5],  # Node 2 points to Node 4 and Node 5
        3: [6, 7],  # Node 3 points to Node 6 and Node 7
        4: [8],  # Node 4 points to Node 8
        5: [8, 9],  # Node 5 points to Node 8 and Node 9
        6: [10],  # Node 6 points to Node 10
        7: [10],  # Node 7 points to Node 10
        8: [11],  # Node 8 points to Node 11
        9: [11],  # Node 9 points to Node 11
        10: [12],  # Node 10 points to Node 12
        11: [12],  # Node 11 points to Node 12
        12: [13],  # Node 12 points to Node 13
        13: [],  # Node 13 has no outgoing edges (terminal node)
    }

    is_acyclic = can_topologically_sort(adjacency_dict)

    assert is_acyclic == True, 'It can be possible to topologically sort a DAG'


def test_can_topologically_sort_returns_false_for_graph_with_cycle():
    adjacency_dict = {
        1: [2],  # Node 1 points to Node 2
        2: [3],  # Node 2 points to Node 3
        3: [1],  # Node 3 points to Node 1 (creates a cycle)
    }

    is_acyclic = can_topologically_sort(adjacency_dict)

    assert is_acyclic == False, 'A graph with a cycle is not a valid DAG.'


def test_can_topologically_sort_returns_true_for_fully_connected_acyclic_graph():
    adjacency_dict = {
        1: [2],  # Node 1 points to Node 2
        2: [3],  # Node 2 points to Node 3
        3: [4],  # Node 3 points to Node 4
        4: [5],  # Node 4 points to Node 5
        5: [],  # Node 5 has no outgoing edges
    }

    is_acyclic = can_topologically_sort(adjacency_dict)

    assert is_acyclic == True, 'A linearly connected graph is a valid DAG.'
