import io
import time

from dev_toolkit.cli_spinner import Spinner


def test_spinner_context_manager():
    stream = io.StringIO()
    with Spinner(text="Working", delay=0.01, stream=stream):
        time.sleep(0.05)

    output = stream.getvalue()
    assert "✔ Done!" in output


def test_spinner_manual_control():
    stream = io.StringIO()
    spinner = Spinner(text="Loading", delay=0.01, stream=stream)
    spinner.start()
    assert spinner._thread is not None
    spinner.update_text("Processing")
    assert spinner.text == "Processing"
    spinner.stop("Finished!")

    output = stream.getvalue()
    assert "Finished!" in output
