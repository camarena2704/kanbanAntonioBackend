import asyncio
import logging
import os

from dotenv import load_dotenv
from tortoise import Tortoise

load_dotenv()
# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_board_columns_view():
    """
    Create a database view that retrieves all column names associated with their corresponding board ID.
    """

    logger.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.getenv("DATABASE_URL"),
        modules={"default": ["app.modules.database_module.models.default.__main__"]},
    )

    logger.info("Generating view via Tortoise...")

    await Tortoise.get_connection("default").execute_query(
        "create or replace view all_name_columns_board as "
        "select c.name, c.board_id from columns c "
        "join board b on b.id = c.board_id;"
    )
    logger.info("Generating view all_name_columns_board done")

if __name__ == '__main__':
    asyncio.run(create_board_columns_view())
