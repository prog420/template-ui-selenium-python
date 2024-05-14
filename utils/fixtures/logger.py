import logging
import os.path
from uuid import uuid4

import allure
import pytest


@pytest.fixture(scope="function", autouse=True)
def logger(base_temp_directory, request: pytest.FixtureRequest):
    failed_test_count = request.session.testsfailed
    log_formatter = logging.Formatter(
        "$(asctime)s - %(filename)s - $(levelname)s - $(message)s"
    )
    log_name = f"{request.node.name}_{uuid4()}_test.log"
    log_path = os.path.join(base_temp_directory, log_name)
    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_path, "w", "utf-8")
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger("test")
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    if request.session.testsfailed > failed_test_count:
        allure.attach(log_path, log_name, allure.attachment_type.TEXT)

    for handler in log.handlers:
        handler.close()
