from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AVLNode:
    key: int
    left: AVLNode | None = None
    right: AVLNode | None = None
    height: int = 1


class AVLTree:
    def __init__(self, elements: list[int] | None = None):
        self._root: AVLNode | None = None
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

    def _inorder(self, node: AVLNode | None):
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

    def _height(self, node: AVLNode | None):
        return node.height if node else 0

    def _fix_height(self, node: AVLNode):
        l_height = self._height(node.left)
        r_height = self._height(node.right)
        node.height = max(l_height, r_height) + 1

    def _b_factor(self, node: AVLNode):
        return self._height(node.left) - self._height(node.right)

    def _rotate_left(self, a: AVLNode) -> AVLNode:
        b = a.right
        a.right = b.left
        b.left = a
        self._fix_height(a)
        self._fix_height(b)
        return b

    def _rotate_right(self, a: AVLNode) -> AVLNode:
        b = a.left
        a.left = b.right
        b.right = a
        self._fix_height(a)
        self._fix_height(b)
        return b

    def _rebalance(self, node: AVLNode):
        self._fix_height(node)
        b_factor = self._b_factor(node)

        if b_factor > 1:
            if self._b_factor(node.left) <= -1:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if b_factor < -1:
            if self._b_factor(node.right) >= 1:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def _insert(self, node: AVLNode | None, key: int) -> tuple[AVLNode, bool]:
        if not node:
            return AVLNode(key), True
        if key < node.key:
            node.left, added = self._insert(node.left, key)
        elif key > node.key:
            node.right, added = self._insert(node.right, key)
        else:
            return node, False
        return self._rebalance(node), added

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

    def _min_node(self, node: AVLNode):
        current = node
        while current.left:
            current = current.left
        return current

    def _max_node(self, node: AVLNode):
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

    def _extract_min(self, node: AVLNode) -> tuple[AVLNode, AVLNode | None]:
        if not node.left:
            return node, node.right
        min_node, node.left = self._extract_min(node.left)
        return min_node, self._rebalance(node)

    def _remove(self, node: AVLNode | None, key: int) -> tuple[AVLNode | None, bool]:
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

        return self._rebalance(node), removed

    def remove(self, key: int):
        self._root, removed = self._remove(self._root, key)
        if removed:
            self._size -= 1
        return removed
