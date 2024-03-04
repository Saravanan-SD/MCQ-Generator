import logging
import os
from datetime import datetime

log_file=f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}.log"

log_folder_path=os.path.join(os.getcwd(),'logs')

os.makedirs(log_folder_path,exist_ok=True)

log_file_path= os.path.join(log_folder_path,log_file)


logging.basicConfig(level=logging.INFO,
        filename=log_file_path,
        format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s'
)

