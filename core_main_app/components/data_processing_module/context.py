from contextvars import ContextVar

_suppress_processing_signals = ContextVar(
    "suppress_processing_signals", default=False
)
