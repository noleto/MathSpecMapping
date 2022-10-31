from copy import copy
import graphviz
from IPython.display import display
from .classes import StateModificationEdge, Edge


def find_starting_entities(actions_to_map, behavioral_action_space, behavioral_action_edges):
    entities = []
    edges = []
    queue = []

    for action in actions_to_map:
        ba = behavioral_action_space[action]
        connections = ba.called_by
        entities.extend(connections)
        edges.extend([x.label, ba.label] for x in connections)
        queue.extend(behavioral_action_edges[action])

    entities = list(set(entities))
    return entities, edges, queue


def create_graph(actions_to_map, name, behavioral_action_space, all_edges):

    entities, edges, queue = find_starting_entities(actions_to_map, behavioral_action_space,
                                                    all_edges)
    seen = entities

    graph = graphviz.Digraph(name)

    graph_messages = []

    for e in entities:
        e.create_node(graph)

    for action in actions_to_map:
        ba = behavioral_action_space[action]
        ba.create_node(graph)
        seen.append(ba)

    for e in edges:
        graph.edge(e[0], e[1])

    sm_actions = []
    while len(queue) > 0:
        cur = queue.pop(0)
        if type(cur) == StateModificationEdge:
            sm_actions.append(cur)
        else:
            if cur.target not in seen:
                cur.target.create_node(graph)
                seen.append(cur.target)
                queue.extend(all_edges[cur.target.label])
            if cur.optional:
                graph.edge(cur.origin.label, cur.target.label,
                           color=cur.message.color, style="dashed")
            else:
                graph.edge(cur.origin.label, cur.target.label,
                           color=cur.message.color)
            if cur.message not in graph_messages:
                graph_messages.append(cur.message)

    for sm in sm_actions:
        entity_name2 = sm.entity.label + "_2"
        if entity_name2 not in seen:
            graph.node(entity_name2, sm.entity.label,
                       shape="cylinder", color="black")
            seen.append(entity_name2)
        var_label = "{}.{}".format(sm.entity.label, sm.variable)
        if var_label not in seen:
            graph.node(var_label, var_label)
            graph.edge(var_label, entity_name2)
            seen.append(var_label)

        graph.edge(sm.origin.label, var_label)

    print("Message Legend:")
    print()
    for g in graph_messages:
        a = copy(g.__dict__["__annotations__"])
        a.pop('color')
        print("{}: {} -> {}".format(g.color, g.__name__, a))
        print()
    display(graph)


def write_out_behavioral_functions(behavioral_action_space, action_names):
    out = "<h3>Behavioral Action Space</h3>"
    for name in action_names:
        out += behavioral_action_space[name].write_description()

    return out


def reverse_out_graph(all_edges):
    all_edges_reverse = {}
    possible_outputs = {}
    possible_inputs = {}

    for key in all_edges:
        possible_outputs[key] = set()
        for e in all_edges[key]:
            if type(e) == Edge:
                other_key = e.target.label
                message = e.message
                if other_key not in all_edges_reverse:
                    all_edges_reverse[other_key] = set()
                    possible_inputs[other_key] = set()
                all_edges_reverse[other_key].add(key)
                possible_outputs[key].add(message)
                possible_inputs[other_key].add(message)
    return all_edges_reverse, possible_outputs, possible_inputs
