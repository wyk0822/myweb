# manage.py
# 将迁移相关的命令集添加到脚本命令中
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api

from flask_script import Manager
from apps import create_app
from apps import db
app = create_app()
manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
