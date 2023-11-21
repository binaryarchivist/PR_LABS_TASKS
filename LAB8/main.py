import threading

from Node import Node
from Orchestrator import Orchestrator


def main() -> None:
    nodes: list[Node] = []

    for _ in range(10):
        node: Node = Node()
        print(node.host, node.port)
        nodes.append(node)

    for node in nodes:
        listener_thread = threading.Thread(target=node.listen)
        listener_thread.start()

    orchestrator: Orchestrator = Orchestrator(nodes)

    orchestrator.run_election()

    orchestrator.start_heartbeat()


# TODO: Raise HTTP servers on each Node, make Leader act as a Gateway for all requests, implement re-election

if __name__ == "__main__":
    main()

