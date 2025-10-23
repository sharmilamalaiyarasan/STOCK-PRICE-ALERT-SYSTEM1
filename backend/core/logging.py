import logging
import os

# Create logs directory if not exists
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/data_ingestion.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Logger instance
logger = logging.getLogger("data_ingestion")
