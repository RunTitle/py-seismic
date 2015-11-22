# -*- coding: utf-8 -*-
import structlog
from seismic import processors as proc

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        proc.action_normalizer,
        proc.app,
        proc.timestamp,
        proc.uid,
        proc.action_version,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
