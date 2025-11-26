"""Planning module."""

from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, MetaData
from langchain.tools import tool

class Planner:
    """Planner class."""
    def __init__(self, db="sqlite:///planning.db"):
        self.db = db
        self.engine = sa.create_engine(db)
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.engine)
        self.tables = self.metadata.tables
        self.init_db()

    def init_db(self):
        """Create database and table plan if not exists.
        Plan table schema:
            task_id: int, primary key
            name: str, unique
            description: str
            start_time: datetime
            end_time: datetime
            status: str, default "pending"
        """
        if 'plan' not in self.metadata.tables:
            Table(
                'plan', self.metadata,
                Column('task_id', Integer, primary_key=True),
                Column('name', String(255), unique=True, nullable=False),
                Column('description', Text),
                Column('start_time', DateTime),
                Column('end_time', DateTime),
                Column('status', String(50), default="pending", nullable=False)
            )
            self.metadata.create_all(self.engine)
        else:
            # Обновляем метаданные, если таблица уже существует
            self.metadata = MetaData()
            self.metadata.reflect(bind=self.engine)
            self.tables = self.metadata.tables

    def list_tasks(self, status="pending"):
        """List tasks with specified status."""
        if 'plan' not in self.tables:
            self.init_db()

        table = self.tables['plan']
        with self.engine.connect() as conn:
            stmt = sa.select(table).where(table.c.status == status)
            result = conn.execute(stmt)
            res=result.mappings().fetchall()
            return res

    def list_all_tasks(self):
        """List tasks."""
        if 'plan' not in self.tables:
            self.init_db()

        table = self.tables['plan']
        with self.engine.connect() as conn:
            stmt = sa.select(table)
            result = conn.execute(stmt)
            res=result.mappings().fetchall()
            return res

    def add_task(self, name, description, start_time, end_time):
        """Add a new task."""
        if 'plan' not in self.tables:
            self.init_db()

        table = self.tables['plan']
        with self.engine.connect() as conn:
            try:
                stmt = sa.insert(table).values(
                    name=name,
                    description=description,
                    start_time=start_time,
                    end_time=end_time,
                    status="pending"
                )
                conn.execute(stmt)
                conn.commit()
                return True
            except sa.exc.IntegrityError as e:
                conn.rollback()
                raise ValueError(f"Task with name '{name}' already exists.") from e
            except Exception as e:
                conn.rollback()
                raise e

    def update_task_status(self, task_id, status):
        """Update task status by task_id."""
        if 'plan' not in self.tables:
            self.init_db()

        table = self.tables['plan']
        with self.engine.connect() as conn:
            stmt = sa.update(table).where(table.c.task_id == task_id).values(status=status)
            result = conn.execute(stmt)
            conn.commit()
            if result.rowcount == 0:
                raise ValueError(f"Task with id={task_id} not found.")
            return True

    def delete_task(self, task_id):
        """Delete task by task_id."""
        if 'plan' not in self.tables:
            self.init_db()

        table = self.tables['plan']
        with self.engine.connect() as conn:
            stmt = sa.delete(table).where(table.c.task_id == task_id)
            result = conn.execute(stmt)
            conn.commit()
            if result.rowcount == 0:
                raise ValueError(f"Task with id={task_id} not found.")
            return True

    def cleanup_tasks(self):
        """Delete all tasks."""
        if 'plan' not in self.tables:
            self.init_db()

        table = self.tables['plan']
        with self.engine.connect() as conn:
            stmt = sa.delete(table)
            conn.execute(stmt)
            conn.commit()
            return True

p = Planner()
@tool
def list_tasks(status: str = "pending") -> str:
    """Получить список задач в планах с указанным статусом.
    Args: status: str - статус задач
    status может быть: pending (открытая/активная задача),
        completed (завершенная),
        in_progress (в процессе)
    """
    task_list = [str(t) for t in p.list_tasks(status)]
    s = "Задачи:" + "\n".join(task_list)
    return s

@tool
def list_all_tasks() -> str:
    """Получить список всех задач в планах.
    """
    task_list = [str(t) for t in p.list_all_tasks()]
    s = "Задачи:" + "\n".join(task_list)
    return s


@tool
def delete_task(task_id: int) -> str:
    """Удалить задачу по task_id из плана.
    Args: task_id: int - id of the task to delete
    """
    try:
        p.delete_task(task_id)
        return "Task deleted successfully."
    except ValueError as e:
        return str(e)

def add_task(name: str, description: str, start_time: datetime, end_time: datetime) -> str:
    """Добавить новую задачу в план со статусом "pending".

    Args: name: str - name of the task
          description: str - description of the task
          start_time: datetime - start time of the task
          end_time: datetime - end time of the task
          """
    try:
        p.add_task(name, description, start_time, end_time)
        return "Task added successfully."
    except ValueError as e:
        return str(e)

@tool
def update_task_status(task_id: int, status: str) -> str:
    """Обновить статус задачи по task_id в плане.
    Args: task_id: int - id of the task to update
          status: str - new status of the task
    status может быть: pending (открытая/активная задача),
        completed (завершенная),
        in_progress (в процессе)
    """
    if p.update_task_status(task_id, status):
        return "Task status updated successfully."
    return "Task status update failed."
@tool
def cleanup_tasks() -> str:
    """Очистить все задачи в плане."""
    try:
        p.cleanup_tasks()
        return "All tasks deleted successfully."
    except ValueError as e:
        return f"Tasks deletion failed.{e}"

planning_tools = [add_task, list_tasks, update_task_status,
                  delete_task, cleanup_tasks, list_all_tasks]
