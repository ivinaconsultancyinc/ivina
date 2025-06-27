import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def scheduled_task():
    logging.info("Scheduled task executed.")
    # Perform a dummy calculation
    result = 42  # Replace with actual task logic
    logging.info(f"Dummy calculation result: {result}")

if __name__ == "__main__":
    while True:
        scheduled_task()
        time.sleep(3600)  # Run every hour
