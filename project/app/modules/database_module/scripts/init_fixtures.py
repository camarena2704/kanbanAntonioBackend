import asyncio
import logging
import os

from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()
# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_tasks_by_board_view():
    """
    Create a database view that retrieves all column
    names associated with their corresponding board ID.
    """

    logger.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.getenv("DATABASE_URL"),
        modules={"default": ["app.modules.database_module.models.default.__main__"]},
    )

    logger.info("Generating view via Tortoise...")

    await Tortoise.get_connection("default").execute_query(
        "CREATE or replace VIEW tasks_by_board AS "
        "SELECT b.id AS board_id, b.name AS "
        "board_name, c.name AS column_name, t.id AS "
        "task_id, t.title, t.description, t.order "
        "FROM board b "
        "JOIN columns c ON b.id = c.board_id "
        "JOIN task t ON c.id = t.column_id;"
    )
    logger.info("Generating view tasks_by_board done")


if __name__ == "__main__":
    asyncio.run(create_tasks_by_board_view())
