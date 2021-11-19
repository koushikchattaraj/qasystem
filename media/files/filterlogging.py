import sys


def test_logging_filters(sentry_init, capture_events):
    sentry_init(integrations=[LoggingIntegration()], default_integrations=False)
    events = capture_events()

    should_log = False

    class MyFilter(logging.Filter):
        def filter(self, record):
            return should_log

    logger.addFilter(MyFilter())
    logger.error("hi")

    assert not events

    should_log = True
    logger.error("hi")

    (event,) = events
    assert event["logentry"]["message"] == "hi" 