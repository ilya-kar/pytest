from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Node:
    key: int
    left: Node | None = None
    right: Node | None = None


class BST:
    def __init__(self, elements: list[int] | None = None):
        self._root: Node | None = None
        self._size: int = 0
        if elements:
            for key in elements:
                self.insert(key)

    def __len__(self):
        return self._size

    def __iter__(self):
        yield from self._inorder(self._root)

    def __str__(self):
        return " ".join(map(str, self))

    def __contains__(self, key: int):
        return bool(self._find_node(key))

    def _inorder(self, node: Node | None):
        if not node:
            return
        yield from self._inorder(node.left)
        yield node.key
        yield from self._inorder(node.right)

    def inorder(self) -> list[int]:
        return list(self)

    def _find_node(self, key: int):
        node = self._root

        while node:
            if key == node.key:
                return node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        return None

    def _insert(self, node: Node | None, key: int) -> tuple[Node, bool]:
        if not node:
            return Node(key), True
        if key < node.key:
            node.left, added = self._insert(node.left, key)
        elif key > node.key:
            node.right, added = self._insert(node.right, key)
        else:
            return node, False
        return node, added

    def insert(self, key: int):
        self._root, added = self._insert(self._root, key)
        if added:
            self._size += 1
        return added

    def min(self):
        if not self._root:
            raise ValueError("Tree is empty")
        return self._min_node(self._root).key

    def max(self):
        if not self._root:
            raise ValueError("Tree is empty")
        return self._max_node(self._root).key

    def _min_node(self, node: Node):
        current = node
        while current.left:
            current = current.left
        return current

    def _max_node(self, node: Node):
        current = node
        while current.right:
            current = current.right
        return current

    def next(self, key: int):
        current = self._root
        successor = None

        while current:
            if current.key > key:
                successor = current.key
                current = current.left
            else:
                current = current.right

        return successor

    def prev(self, key: int):
        current = self._root
        predecessor = None

        while current:
            if current.key < key:
                predecessor = current.key
                current = current.right
            else:
                current = current.left

        return predecessor

    def _extract_min(self, node: Node) -> tuple[Node, Node | None]:
        if not node.left:
            return node, node.right
        min_node, node.left = self._extract_min(node.left)
        return min_node, node

    def _remove(self, node: Node | None, key: int) -> tuple[Node | None, bool]:
        if not node:
            return None, False

        if key < node.key:
            node.left, removed = self._remove(node.left, key)
        elif key > node.key:
            node.right, removed = self._remove(node.right, key)
        else:
            removed = True
            if not node.right:
                return node.left, removed
            if not node.left:
                return node.right, removed
            min_node, node.right = self._extract_min(node.right)
            node.key = min_node.key

        return node, removed

    def remove(self, key: int):
        self._root, removed = self._remove(self._root, key)
        if removed:
            self._size -= 1
        return removed
