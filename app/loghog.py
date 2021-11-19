import logging

#Create a new logging instance
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = r"C:\Users\Spark\Desktop\projects\tradesetandforget\documentation\loghog.log", 
                            level= logging.DEBUG, format= LOG_FORMAT)
logger = logging.getLogger()
logger.debug("This is a harmless debug message.")
logger.info("Here is the output to debug the program")
logger.warning("I'm sorry, but I can't do that Leslie.")
logger.error("Error: not possible friend.")
logger.critical("Quick, get the fire extinguisher!")