import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d [ %(levelname)s ] [ %(module)s ] [ %(funcName)s ] %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
# filename='service.log',