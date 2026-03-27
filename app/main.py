from app.bst.bst import BST


def test_bst_advanced():
    # --- Создание дерева и вставка 10 элементов ---
    tree = BST()
    elements = [50, 30, 70, 20, 40, 60, 80, 10, 35, 45]
    for e in elements:
        assert tree.insert(e), f"Failed to insert {e}"
    print(tree)
    # Проверка размера
    assert len(tree) == 10

    # Проверка inorder
    expected_inorder = [10, 20, 30, 35, 40, 45, 50, 60, 70, 80]
    assert tree.inorder() == expected_inorder, f"inorder mismatch: {tree.inorder()}"

    # Проверка min/max
    assert tree.min() == 10
    assert tree.max() == 80

    # Проверка next/prev для нескольких элементов
    assert tree.next(35) == 40
    assert tree.prev(35) == 30
    assert tree.next(80) is None
    assert tree.prev(10) is None

    # --- Удаление узла с двумя детьми (30 имеет детей 20 и 40) ---
    assert tree.remove(30), "Failed to remove 30"
    assert len(tree) == 9
    expected_inorder_after_removal = [10, 20, 35, 40, 45, 50, 60, 70, 80]
    assert tree.inorder() == expected_inorder_after_removal, (
        f"inorder after removal mismatch: {tree.inorder()}"
    )

    # --- Удаление узла с двумя детьми (50 имеет детей 35 и 60) ---
    assert tree.remove(50), "Failed to remove 50"
    assert len(tree) == 8
    expected_inorder_after_removal2 = [10, 20, 35, 40, 45, 60, 70, 80]
    assert tree.inorder() == expected_inorder_after_removal2, (
        f"inorder after removal mismatch: {tree.inorder()}"
    )

    # --- Удаление листьев ---
    for leaf in [10, 20, 45, 80]:
        assert tree.remove(leaf), f"Failed to remove leaf {leaf}"
    expected_inorder_final = [35, 40, 60, 70]
    assert tree.inorder() == expected_inorder_final
    assert len(tree) == 4

    print("Все сложные тесты пройдены!")


# Запуск
test_bst_advanced()
