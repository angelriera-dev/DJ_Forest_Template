import logging


class IgnoreDebugToolbarFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        try:
            return "/__debug__/" not in record.getMessage()
        except Exception:
            return True
