import logging
from logging.handlers import RotatingFileHandler
import os
import json
from datetime import datetime

def setup_logging(app):
    """Configure structured JSON logging"""
    log_level = logging.getLevelName(app.config['LOG_LEVEL'])
    
    # Remove default handlers
    for handler in app.logger.handlers[:]:
        app.logger.removeHandler(handler)
    
    # Create logs directory if not exists
    logs_dir = os.path.join(app.root_path, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        os.path.join(logs_dir, 'farmhub.log'),
        maxBytes=1024 * 1024 * 10,  # 10 MB
        backupCount=10
    )
    
    # JSON formatter
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_record = {
                'timestamp': datetime.utcnow().isoformat(),
                'level': record.levelname,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno,
                'logger': record.name,
                'thread': record.threadName
            }
            
            # Add request context if available
            if hasattr(record, 'request_id'):
                log_record['request_id'] = record.request_id
            
            return json.dumps(log_record)
    
    file_handler.setFormatter(JSONFormatter())
    app.logger.addHandler(file_handler)
    
    # Set log level
    app.logger.setLevel(log_level)
    
    # Disable propagation to avoid duplicate logs
    app.logger.propagate = False