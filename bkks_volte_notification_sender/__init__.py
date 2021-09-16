import logging

# The logging levels below may need to be changed based on the logging that you want to suppress.
uamqp_logger = logging.getLogger("uamqp")
uamqp_logger.setLevel(logging.ERROR)

# or even further fine-grained control, suppressing the warnings in uamqp.connection module
uamqp_connection_logger = logging.getLogger("uamqp.connection")
uamqp_connection_logger.setLevel(logging.ERROR)
