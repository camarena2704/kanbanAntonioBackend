import logging
import os

from dotenv import load_dotenv
from tortoise import Tortoise, run_async

logger = logging.getLogger(__name__)
# load env
load_dotenv()


async def generate_schema() -> None:
    logger.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.getenv("DATABASE_URL"),
        modules={"default": ["app.modules.database_module.models.default.__main__"]},
    )

    logger.info("Generating database schemas via Tortoise...")
    await Tortoise.generate_schemas()

    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
