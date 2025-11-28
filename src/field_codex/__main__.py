from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

UNIVERSE_FILENAME = "universe.json"


SEED_UNIVERSE = {
    "nodes": [
        {
            "id": "Field",
            "title": "Shared field of consciousness / information",
            "node_type": "field",
            "summary": "The underlying informational field connecting all living systems.",
            "tags": ["field", "consciousness", "information"],
        },
        {
            "id": "Nature_primary_artifact",
            "title": "Nature as primary artifact of the field",
            "node_type": "artifact",
            "summary": "Nature manifests the patterns and outputs of the field.",
            "tags": ["nature", "artifact", "expression"],
        },
        {
            "id": "GNI_v0_1",
            "title": "General Nature Intelligence",
            "node_type": "concept",
            "summary": "A framing of intelligence emerging from natural systems and their interplay with the field.",
            "tags": ["intelligence", "concept", "nature"],
        },
        {
            "id": "Field_as_primary_reality",
            "title": "Field as primary reality",
            "node_type": "hypothesis",
            "summary": "Posits the field as the fundamental substrate from which reality emerges.",
            "tags": ["field", "reality", "hypothesis"],
        },
        {
            "id": "Consciousness_as_ocean",
            "title": "Consciousness as ocean",
            "node_type": "metaphor",
            "summary": "Imagines consciousness as a vast ocean with waves representing experiences.",
            "tags": ["consciousness", "metaphor", "imagery"],
        },
        {
            "id": "Is_intelligence_constructed_or_expressed",
            "title": "Is intelligence constructed or expressed?",
            "node_type": "question",
            "summary": "Asks whether intelligence is built by systems or expressed from a deeper field.",
            "tags": ["intelligence", "question", "origin"],
        },
        {
            "id": "When_It_Rings",
            "title": "Singularity as resonance event",
            "node_type": "concept",
            "summary": "Frames singularity as a resonance event across the field and living systems.",
            "tags": ["singularity", "resonance", "field"],
        },
    ],
    "edges": [
        {"source": "Field", "relation": "expresses_as", "target": "Nature_primary_artifact"},
        {"source": "Nature_primary_artifact", "relation": "is_artifact_of", "target": "Field"},
        {"source": "GNI_v0_1", "relation": "mirrors", "target": "Nature_primary_artifact"},
        {"source": "Field_as_primary_reality", "relation": "supports", "target": "Consciousness_as_ocean"},
        {"source": "When_It_Rings", "relation": "emerges_from", "target": "Field_as_primary_reality"},
    ],
}


@dataclass
class Universe:
    path: Path
    nodes: List[Dict[str, object]] = field(default_factory=list)
    edges: List[Dict[str, str]] = field(default_factory=list)

    def load(self) -> None:
        if self.path.exists():
            data = json.loads(self.path.read_text())
            self.nodes = data.get("nodes", [])
            self.edges = data.get("edges", [])
            return

        self.nodes = list(SEED_UNIVERSE["nodes"])
        self.edges = list(SEED_UNIVERSE["edges"])
        self.save()

    def save(self) -> None:
        payload = {"nodes": self.nodes, "edges": self.edges}
        self.path.write_text(json.dumps(payload, indent=2))

    def get_node(self, node_id: str) -> Optional[Dict[str, object]]:
        return next((node for node in self.nodes if node.get("id") == node_id), None)

    def add_node(self, node: Dict[str, object]) -> None:
        if self.get_node(node["id"]):
            raise ValueError(f"Node with id '{node['id']}' already exists.")
        self.nodes.append(node)

    def add_edge(self, edge: Dict[str, str]) -> None:
        if not self.get_node(edge["source"]):
            raise ValueError(f"Unknown source id: {edge['source']}")
        if not self.get_node(edge["target"]):
            raise ValueError(f"Unknown target id: {edge['target']}")
        self.edges.append(edge)


def format_node(node: Dict[str, object]) -> str:
    tags = ", ".join(node.get("tags", []))
    return f"{node['id']} [{node['node_type']}]: {node['title']} (tags: {tags})"


def list_nodes(universe: Universe, only_questions: bool = False) -> None:
    nodes = universe.nodes
    if only_questions:
        nodes = [node for node in nodes if node.get("node_type") == "question"]
    for node in sorted(nodes, key=lambda n: n.get("id", "")):
        print(format_node(node))


def show_node(universe: Universe, node_id: str) -> None:
    node = universe.get_node(node_id)
    if not node:
        raise ValueError(f"Node '{node_id}' not found.")

    print(format_node(node))
    print(f"Summary: {node.get('summary', '')}")

    outgoing = [edge for edge in universe.edges if edge.get("source") == node_id]
    incoming = [edge for edge in universe.edges if edge.get("target") == node_id]

    if outgoing:
        print("Outgoing links:")
        for edge in outgoing:
            print(f"  {edge['relation']} -> {edge['target']}")
    if incoming:
        print("Incoming links:")
        for edge in incoming:
            print(f"  {edge['relation']} <- {edge['source']}")


def search_nodes(universe: Universe, text: str) -> None:
    needle = text.lower()
    for node in sorted(universe.nodes, key=lambda n: n.get("id", "")):
        haystack = " ".join([
            str(node.get("id", "")),
            str(node.get("title", "")),
            str(node.get("summary", "")),
            " ".join(node.get("tags", [])),
        ]).lower()
        if needle in haystack:
            print(format_node(node))


def prompt_new_node(universe: Universe) -> Dict[str, object]:
    node_id = input("id (no spaces): ").strip()
    if " " in node_id:
        raise ValueError("Node id must not contain spaces.")
    title = input("title: ").strip()
    node_type = input("node_type: ").strip()
    summary = input("summary: ").strip()
    tags_raw = input("tags (comma-separated): ").strip()
    tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]

    return {
        "id": node_id,
        "title": title,
        "node_type": node_type,
        "summary": summary,
        "tags": tags,
    }


def prompt_new_edge(universe: Universe) -> Dict[str, str]:
    source = input("source id: ").strip()
    relation = input("relation: ").strip()
    target = input("target id: ").strip()

    if not universe.get_node(source):
        raise ValueError(f"Unknown source id: {source}")
    if not universe.get_node(target):
        raise ValueError(f"Unknown target id: {target}")

    return {"source": source, "relation": relation, "target": target}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Field Codex CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("list", help="List all nodes")
    subparsers.add_parser("list-questions", help="List nodes of type 'question'")

    show_parser = subparsers.add_parser("show", help="Show a node and its links")
    show_parser.add_argument("node_id")

    search_parser = subparsers.add_parser("search", help="Search nodes by text")
    search_parser.add_argument("text")

    subparsers.add_parser("add-node", help="Interactively add a node")
    subparsers.add_parser("add-link", help="Interactively add a link")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    universe_path = Path(__file__).resolve().parents[2] / UNIVERSE_FILENAME
    universe = Universe(path=universe_path)
    universe.load()

    changed = False
    try:
        if args.command == "list":
            list_nodes(universe)
        elif args.command == "list-questions":
            list_nodes(universe, only_questions=True)
        elif args.command == "show":
            show_node(universe, args.node_id)
        elif args.command == "search":
            search_nodes(universe, args.text)
        elif args.command == "add-node":
            node = prompt_new_node(universe)
            universe.add_node(node)
            changed = True
            print("Node added.")
        elif args.command == "add-link":
            edge = prompt_new_edge(universe)
            universe.add_edge(edge)
            changed = True
            print("Link added.")
        else:
            parser.print_help()
    except ValueError as exc:
        parser.error(str(exc))

    if changed:
        universe.save()


if __name__ == "__main__":
    main()
