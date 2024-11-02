import json
import os
import sys
from helpers.say_hello import say_hello
import numpy as np

def main():
    say_hello()
    arr = np.array([1, 2, 3, 4, 5])
    print("Sum:", np.sum(arr))
    TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
    print('TASK_INDEX', TASK_INDEX)

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        message = (
            f"Task failed: {str(err)}"
        )
        print(json.dumps({"message":message, "severity":"ERROR"}))
        sys.exit(1)  # Retry Job Task by exiting the process