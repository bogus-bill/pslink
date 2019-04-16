from enum import Enum

import pslink.symap as symap


class RelationType(Enum):
    """
    An enumeration of the types a relation between a source and target node
    can have.

    * `same`: the source and target node are exactly the same thing (the
              target node is a synonym of the source node).
    * `broader`: the target node has a broader meaning than the source node (the
                 target is a hyponym of the source node).
    * `narrower`: the target node has a narrower meaning that the source node.
    * `derived`: the source node is derived from the target node.
    """

    same = 0
    broader = 1
    narrower = 2
    derived = 3


class Relation(object):
    """ A directed relation from a source node to a target node. """

    def __init__(self, source: str, target: str, rtype: RelationType):
        self.source = source
        self.target = target
        self.rtype = rtype

    def factor(self) -> float:
        if self.rtype == RelationType.same:
            return 1.0
        if self.rtype == RelationType.narrower:
            return 0.75
        if self.rtype == RelationType.broader:
            return 0.75
        if self.rtype == RelationType.derived:
            return 0.5
        return 0.0

    def semapl(self) -> str:
        """ Returns a semapl representation of this relation. """
        if self.rtype == RelationType.same:
            return '"%s" , "%s"=' % (self.source, self.target)
        if self.rtype == RelationType.broader:
            return '"%s" , "%s"^' % (self.source, self.target)
        if self.rtype == RelationType.narrower:
            return '"%s" , "%s"^' % (self.target, self.source)
        if self.rtype == RelationType.derived:
            return '"%s" , "%s"<' % (self.source, self.target)
        return '"%s" , "%s"?' % (self.source, self.target)


class ProductInfo(object):

    def __init__(self):
        self.process_uuid = ''
        self.process_name = ''
        self.product_uuid = ''
        self.product_name = ''
        self.product_unit = ''


class Graph(object):
    """ A simple graph model for searching semantic relations between products. """

    def __init__(self):
        self.nodes = set()
        self.edges = {}
        self.product_infos = {}

    def add_product_info(self, node: str, info: ProductInfo):
        """ Tag the given node with the given product information. """
        self.product_infos[node] = info

    def add_relation(self, rel: Relation):
        """ Add the given relation to this graph. If the relation is a same-as,
            broader, or narrower relation it will also add the inverse of that
            relation to the graph.
            """
        if rel.source is None or rel.target is None or rel.rtype is None:
            return

        self.nodes.add(rel.source)
        self.nodes.add(rel.target)
        rels = self.edges.get(rel.source)
        if rels is None:
            rels = []
            self.edges[rel.source] = rels

        # skip if it is a duplicate
        for r in rels:  # type: Relation
            if r.target == rel.target:
                return
        rels.append(rel)

        # add the inverse relation
        if rel.rtype != RelationType.derived:
            trels = self.edges.get(rel.target)
            if trels is None:
                trels = []
                self.edges[rel.target] = trels
            if rel.rtype == RelationType.same:
                trels.append(Relation(
                    rel.target, rel.source, RelationType.same))
            elif rel.rtype == RelationType.broader:
                trels.append(Relation(
                    rel.target, rel.source, RelationType.narrower))
            elif rel.rtype == RelationType.narrower:
                trels.append(Relation(
                    rel.target, rel.source, RelationType.broader))

    def relations_of(self, source_node: str) -> list:
        """ Get all direct relations where the given node is the source node.
            This method does not follow same-as relations transitively. """
        r = self.edges.get(source_node)
        return [] if r is None else r

    def broader_of(self, node: str) -> set:
        """ Get all target nodes that are in a direct broader relation to the
            given source node. This method also collects the broader relations
            from the nodes that have a `same as` relation with the given node
            (it is a transitive search).
        """
        broader = set()
        handled = set()
        queue = [node]
        while len(queue) > 0:
            n = queue.pop()
            handled.add(n)
            for rel in self.relations_of(n):  # type: Relation
                if rel.rtype == RelationType.broader:
                    broader.add(rel.target)
                elif rel.rtype == RelationType.same:
                    nn = rel.target
                    if nn not in handled and nn not in queue:
                        queue.append(nn)
        return broader

    def same_of(self, node) -> set:
        """ Get a list of all nodes that are transitively in a `same-as`
            relation to the given node including the node itself. """
        nodes = set()
        queue = [node]
        while len(queue) > 0:
            n = queue.pop()
            nodes.add(n)
            for rel in self.relations_of(n):  # type: Relation
                if rel.rtype == RelationType.same:
                    nn = rel.target
                    if nn not in nodes and nn not in queue:
                        queue.append(nn)
        return nodes

    def closest_broader(self, a: str, b: str) -> tuple:

        nodes_a = [(n, 0) for n in self.same_of(a)]
        nodes_b = [(n, 0) for n in self.same_of(b)]

        if len(nodes_a) == 0 or len(nodes_b) == 0:
            return ()

        level = 0
        while True:

            na = None
            nb = None

            for node_a in nodes_a:
                if na is None and node_a[1] == level:
                    na = node_a[0]
                for node_b in nodes_b:
                    if nb is None and node_b[1] == level:
                        nb = node_b[0]
                    if node_a[0] == node_b[0]:
                        return node_a[0], node_a[1], node_b[1]

            # no match found: fetch the next level
            level += 1
            has_more = False
            if na is not None:
                broader_a = self.broader_of(na)
                if len(broader_a) > 0:
                    has_more = True
                    nodes_a.extend([(b, level) for b in broader_a])
            if nb is not None:
                broader_b = self.broader_of(nb)
                if len(broader_b) > 0:
                    has_more = True
                    nodes_b.extend([(b, level) for b in broader_b])

            if not has_more:
                break
        return ()

    def find_node(self, name: str, matcher) -> tuple:
        """Find a node for the given name and matcher function. For each node
           we pass the node label as first argument and the given name as
           second argument into the matcher function. This function call
           should return a score between 0 and 1. We return a tuple
           (score:float, node:str) for the highest scoring node. If there
           is no node with score > 0 in the graph we return the empty tuple. """
        node = None
        score = 0.0
        for n in self.nodes:
            s = matcher(n, name)
            if not isinstance(s, (int, float)):
                continue
            if s > score:
                node = n
                score = float(s)
        return () if score == 0.0 else (score, node)

    def link_products(self, infos: list, matcher=symap.compare_with_lci_name):
        """ Links a list with product information (see ProductInfo) to the
            nodes in this graph using a syntactical matcher function. When
            multiple products map to the same node only the nodes with the
            highest scores are added to the graph. """
        matches = {}
        for product_info in infos:  # type: ProductInfo
            match = self.find_node(product_info.product_name, matcher)
            if match == ():
                continue
            score, node = match
            m = matches.get(node)
            if m is None:
                # found a new match for a node
                matches[node] = [(score, product_info)]
                continue

            # there is at least one existing match
            other_score = m[0][0]
            if abs(score - other_score) < 1e-6:
                # we have an equal score
                m.append((score, product_info))
                continue

            if score < other_score:
                # there are already better matching products
                # assigned to that node
                continue

            if score > other_score:
                # the new product has a better score
                matches[node] = [(score, product_info)]
                continue

        # now add relations for the best scoring products to the
        # graph. we currently use the product names to identify
        # these new nodes : TODO: this does not work for all
        # database types
        for node, info_scores in matches.items():
            for score, info in info_scores:
                if score > 0.9999:
                    self.add_relation(Relation(
                        info.product_name, node, RelationType.same))
                else:
                    self.add_relation(Relation(
                        info.product_name, node, RelationType.broader))
                self.add_product_info(info.product_name, info)

    def find_products(self, name) -> list:
        match = self.find_node(name, symap.words_equality)
        if match == ():
            return []
        _, node = match
        queue = [(1.0, node)]
        visited = {node}
        products = []
        while len(queue) > 0:
            score, node = queue.pop(0)
            product = self.product_infos.get(node)
            if product is not None:
                products.append((score, product))
            relations = self.relations_of(node)
            relations.sort(key=lambda r: -r.factor())
            for rel in relations:  # type: Relation
                target = rel.target
                if target in visited:
                    continue
                visited.add(target)
                target_score = score * rel.factor()
                queue.append((target_score, target))

        if len(products) == 0:
            return []
        products.sort(key=lambda p: -p[0])
        max_score = products[0][0]
        infos = [products[0][1]]
        for i in range(1, len(products)):
            p = products[i]
            if abs(p[0] - max_score) > 1e-3:
                break
            infos.append(p[1])
        return infos


def parse_text(text: str) -> Graph:
    """ Reads a graph from the given text. """
    g = Graph()
    for line in text.splitlines():
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue

        in_quotes = False
        source = None
        buffer = ""
        for char in line:

            if not in_quotes:
                if char == '"':
                    in_quotes = True
                    buffer = ""
                    continue
                if char.isspace() or char == ",":
                    continue
                if char in ("=", "^", "<"):
                    if source is not None and buffer != "":
                        rtype = None
                        if char == "=":
                            rtype = RelationType.same
                        if char == "^":
                            rtype = RelationType.broader
                        if char == "<":
                            rtype = RelationType.derived
                        rel = Relation(source, buffer, rtype)
                        g.add_relation(rel)
                        buffer = ""

            if in_quotes:
                if char != '"':
                    buffer += char
                    continue
                in_quotes = False
                if source is None:
                    if buffer == "":
                        break
                    source = buffer
                    continue
    return g


def read_file(fpath: str, encoding="utf-8") -> Graph:
    with open(fpath, "r", encoding=encoding) as f:
        text = f.read()
        return parse_text(text)


def write_file(g: Graph, fpath: str, encoding="utf-8"):
    lines = set()
    for node in g.nodes:
        for r in g.relations_of(node):  # type: Relation
            lines.add(r.semapl())
    text = ''
    for line in lines:
        text += line + "\n"
    with open(fpath, "w", encoding=encoding) as f:
        f.write(text)
