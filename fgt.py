from itertools import chain, combinations
import math
import random


class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        self.is_tepid = False
        self.invocation_distance = []

    def __getitem__(self, key):
        for child in self.children:
            if child.name == key:
                return child
        raise KeyError(f"Child node '{key}' not found.")

    def __setitem__(self, key, value):
        for child in self.children:
            if child.name == key:
                child = value
                return
        new_child = value
        new_child.parent = self
        self.children.append(new_child)

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def get_nearest_tepid(self, name: frozenset):
        if len(name) == 0:
            return None
        """
        get_nearest_tepid(node)
        """
        found_nodes = self.find(name)
        tepid_found_nodes = [node for node in found_nodes if node.is_tepid]
        if tepid_found_nodes:
            return tepid_found_nodes

        else:
            # try finding paretns
            ps = get_powerset(name)
            # if len(name)==1:
            #     father = found_nodes[0].parent
            #     if father:
            #         ps.append(father.name)
            print(ps)
            sorted_powerset = sorted(ps, key=lambda x: len(x), reverse=True)

            for subset in sorted_powerset:
                fs = frozenset(subset)
                found_nodes = self.find(fs)
                tepid_found_nodes = [node for node in found_nodes if node.is_tepid]
                if tepid_found_nodes:
                    return tepid_found_nodes

            return None

    def run_on(self, function_node: frozenset, runner_node: "TreeNode"):
        """
        get_nearest_tepid(node)
        """
        distance = len(function_node) - len(runner_node.name)
        runner_node.invocation_distance.append(distance)

    def init(self, tepid_nodes) -> list:
        """
        set config
        """
        for node in tepid_nodes:
            found_nodes = self.find(node)
            for found in found_nodes:
                found.is_tepid = True

    def reconfig(self) -> list:
        tepids = self.get_tepids()
        for node in tepids:
            if len(node.invocation_distance) == 0:
                continue
            node.is_tepid = False
            real_distance = sum(node.invocation_distance) / len(
                node.invocation_distance
            )

            new_tepid_node = node
            if real_distance < 0:
                real_distance = -real_distance
                real_distance = math.ceil(real_distance)

                for _ in range(real_distance):
                    if new_tepid_node.parent:
                        new_tepid_node = new_tepid_node.parent
            else:
                real_distance = math.ceil(real_distance)
                for _ in range(real_distance):
                    if new_tepid_node.children:
                        new_tepid_node = random.choice(new_tepid_node.children)

            new_tepid_node.is_tepid = True
        new_tepids = self.get_tepids()
        return new_tepids

    def print_tree(self, num_of_space=2, tepid=True, invocation_distance=True):
        prefix = "* " if (self.is_tepid and tepid) else " "
        prefix += str(self.invocation_distance) + " " if invocation_distance else " "

        print(
            prefix
            + str(self.name).replace("frozenset", "").replace("(", "").replace(")", "")
        )
        fix_part = "├" + 4 * "─"
        for child in self.children:
            print(num_of_space * " ", end="")
            print(fix_part, end=" ")
            new_number_of_space = num_of_space + len(fix_part) + (len(str(self.name)))
            child.print_tree(new_number_of_space)

    def find(self, name):
        result = []
        if self.name == name:
            result.append(self)
            return result
        else:
            for child in self.children:
                found = child.find(name)
                result += found

            return result

    ######### Optionals #########
    def get_tepids(self):
        """
        get_tepids
        """
        tepids = []
        for child in self.children:
            tepids += child.get_tepids()
        if self.is_tepid:
            tepids.append(self)
        return tepids

    def reset(self, reset_tepids=True):
        """
        reset
        """
        if reset_tepids:
            self.is_tepid = False
        self.invocation_distance = []
        for child in self.children:
            child.reset(reset_tepids)


# this function make powerset of a given set
def get_powerset(in_set):
    # Convert the input set to a list
    in_list = list(in_set)
    # Generate all possible subsets using combinations from itertools
    subsets = chain.from_iterable(
        combinations(in_list, r) for r in range(len(in_list) + 1)
    )
    # Convert each subset to a set
    powerset = [set(subset) for subset in subsets]
    powerset.remove(in_set)

    powerset.remove(set())
    return powerset


def make_tree(data):
    root = TreeNode(frozenset({"Alpine"}))
    for k, v in data.items():
        node_k = TreeNode(k)
        root[node_k.name] = node_k

    for k, v in data.items():
        for pack in v:
            if len(pack) == 1:
                root[k][pack] = TreeNode(pack)

    for k, v in data.items():
        # v is python for example
        length = 1
        exist = True
        while exist == True:
            exist = False
            for packs in v:
                if len(packs) == length:
                    exist = True

                    powerset = get_powerset(packs)
                    for p in powerset:
                        found_list = root.find(p)

                        for found in found_list:
                            if found is not None and len(found.name) == len(packs) - 1:
                                found[packs] = TreeNode(packs)

            length += 1
    return root


if __name__ == "__main__":
    data = {
        frozenset({"python"}): [
            frozenset({"pyspark", "flask"}),
            frozenset({"numpy"}),
            frozenset({"hh"}),
            frozenset({"hh", "flask"}),
            frozenset({"pandas"}),
            frozenset({"numpy", "flask"}),
            frozenset({"numpy", "pyspark", "flask"}),
            frozenset({"numpy", "pyspark"}),
            frozenset({"pyspark"}),
            frozenset({"flask"}),
        ],
        frozenset({"nodejs"}): [frozenset({"nnn"})],
        frozenset({"java"}): [],
    }

    root = make_tree(data)
    root.print_tree()
    # root.init(
    #     [
    #         frozenset({"hh", "flask"}),
    #         frozenset({"pandas"}),
    #         frozenset({"Alpine"}),
    #         frozenset({"numpy", "flask"}),
    #     ]
    # )

    # root.print_tree()

    # nears = root.get_nearest_tepid(frozenset({"flask"}))
    # near = nears[0]
    # print("near: ", near)
