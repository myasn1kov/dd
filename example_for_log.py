import logging

# Здесь задана глобальная конфигурация для логирования
logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w'
)

#изменение формата логов
logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log', 
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

logging.debug('123')
logging.info('Сообщение отправлено')
logging.warning('Большая нагрузка!')
logging.error('Бот не смог отправить сообщение')
logging.critical('Всё упало! Зовите админа!1!111')