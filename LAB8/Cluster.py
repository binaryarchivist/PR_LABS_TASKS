import random

from Node import Node


class Cluster:
    def __init__(self, nodes: list[Node]):
        self.leader_node: Node | None = None
        self.nodes: list[Node] = nodes
        self.current_term = 0
        self.votes_received = 0

    def run_election(self):
        self.current_term += 1
        votes_dict: dict = {node.port: 0 for node in self.nodes}

        for _ in self.nodes:
            self.votes_received += 1

            candidate = self.nodes[random.randint(0, len(self.nodes) - 1)]
            votes_dict[candidate.port] += 1

        if self.votes_received > len(self.nodes) / 2:
            leader_node_port = max(votes_dict, key=votes_dict.get)
            for node in self.nodes:
                node.role = 'follower'
                if node.port == leader_node_port:
                    self.leader_node = node
                    node.role = 'leader'
                    print(f"A new leader has been elected: {node.host}:{node.port}")

            self.broadcast_leader_info()

        else:
            print("Election failed, starting a new election.")
            self.run_election()

    def start_heartbeat(self):
        pass

    def broadcast_leader_info(self) -> None:
        for node in self.nodes:
            if node == self.leader_node:
                continue
            print('node.port: ', node.port)
            self.leader_node.send_message(node.host, node.port, {
                'type': 'leader_credentials',
                'leader_host': self.leader_node.host,
                'leader_port': self.leader_node.port
            })
