# Удаление старой базы данных, если она существует
if os.path.exists('requests.db'):
    os.remove('requests.db')
