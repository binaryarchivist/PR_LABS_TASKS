import threading

from Node import Node
from Cluster import Cluster
from Gateway import Gateway


def main() -> None:
    nodes: list[Node] = []

    for _ in range(10):
        node: Node = Node()
        nodes.append(node)

    for node in nodes:
        listener_thread = threading.Thread(target=node.listen)
        listener_thread.start()

    cluster: Cluster = Cluster(nodes)
    cluster.run_election()
    cluster.start_heartbeat()

    gateway = Gateway(cluster.nodes, cluster.leader_node)
    gateway_thread = threading.Thread(target=gateway.run)
    gateway_thread.start()


if __name__ == "__main__":
    main()
