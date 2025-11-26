"""Тесты для модуля planning"""
from datetime import datetime, timedelta
import pytest
from agent.planning import Planner

@pytest.fixture
def planner():
    """Создаёт экземпляр Planner с временной базой данных."""
    planner = Planner(db="sqlite:///test_planning.db")
    yield planner
    planner.cleanup_tasks()


def test_init_db(planner):
    """Тест: база данных и таблица создаются корректно."""
    assert 'plan' in planner.tables
    assert planner.tables['plan'].name == 'plan'


def test_add_task(planner):
    """Тест: добавление задачи."""
    name = "Test Task"
    desc = "Test Description"
    start = datetime.now()
    end = start + timedelta(hours=1)

    planner.add_task(name, desc, start, end)

    tasks = planner.list_tasks()
    assert len(tasks) == 1
    task = tasks[0]
    assert task['name'] == name
    assert task['description'] == desc
    assert task['status'] == 'pending'
    planner.cleanup_tasks()


def test_add_duplicate_task(planner):
    """Тест: нельзя добавить задачу с одинаковым именем."""
    name = "Unique Task"
    start = datetime.now()
    end = start + timedelta(hours=1)

    planner.add_task(name, "Desc", start, end)
    with pytest.raises(ValueError, match=f"Task with name '{name}' already exists."):
        planner.add_task(name, "Desc2", start, end)
    planner.cleanup_tasks()

def test_list_tasks_by_status(planner):
    """Тест: фильтрация задач по статусу."""
    start = datetime.now()
    end = start + timedelta(hours=1)

    planner.add_task("Task 1", "Desc", start, end)
    planner.add_task("Task 2", "Desc", start, end)
    planner.update_task_status(2, "completed")

    pending = planner.list_tasks("pending")
    completed = planner.list_tasks("completed")
    assert len(pending) == 1
    assert len(completed) == 1
    assert pending[0]['name'] == "Task 1"
    assert completed[0]['name'] == "Task 2"
    planner.cleanup_tasks()


def test_update_task_status(planner):
    """Тест: обновление статуса задачи."""
    start = datetime.now()
    end = start + timedelta(hours=1)

    planner.add_task("Update Test", "Desc", start, end)
    planner.update_task_status(1, "in_progress")

    task = planner.list_tasks("in_progress")[0]
    assert task['name'] == "Update Test"
    assert task['status'] == "in_progress"
    planner.cleanup_tasks()


def test_update_nonexistent_task(planner):
    """Тест: обновление несуществующей задачи."""
    with pytest.raises(ValueError, match="Task with id=999 not found."):
        planner.update_task_status(999, "pending")



def test_delete_task(planner):
    """Тест: удаление задачи."""
    start = datetime.now()
    end = start + timedelta(hours=1)

    planner.add_task("ToDelete", "Desc", start, end)
    planner.delete_task(1)

    tasks = planner.list_tasks()
    assert len(tasks) == 0


def test_delete_nonexistent_task(planner):
    """Тест: удаление несуществующей задачи."""
    with pytest.raises(ValueError, match="Task with id=999 not found."):
        planner.delete_task(999)
