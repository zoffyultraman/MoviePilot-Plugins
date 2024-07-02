import glob
import os
import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app import schemas
from app.core.config import settings
from app.plugins import _PluginBase
from typing import Any, List, Dict, Tuple, Optional
from app.log import logger
from app.schemas import NotificationType

class ChangeTmdbHosts(_PluginBase):
    #名称
    plugin_name = "更新tmdb可用hosts"
    # 插件图标
    plugin_icon = "refresh.png"
    # 插件版本
    plugin_version = "0.1"
    # 插件作者
    plugin_author = "zoffyultraman"
    # 作者主页
    author_url = "https://github.com/zoffyultraman"
    # 插件配置项ID前缀
    plugin_config_prefix = "changetmdbhosts_"
    # 加载顺序
    plugin_order = 99
    # 可使用的用户级别
    auth_level = 1
    # 私有属性
    _plugin_id = None
    _previous_state = False
    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 9,
                                    'md': 3
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                            'hint': '开启后插件将处于激活状态',
                                            'persistent-hint': True,
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 9,
                                    'md': 3
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'onlyonce',
                                            'label': '立即运行一次',
                                            'hint': '插件将立即运行一次',
                                            'persistent-hint': True,
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VRow',
                                'content': [
                                {
                                'component': 'VCol',
                                'props': {
                                    'cols': 9,
                                    'md': 3
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'cron',
                                            'label': '执行周期',
                                            'placeholder': '5位cron表达式',
                                            'hint': '使用cron表达式指定执行周期，如 0 8 * * *',
                                            'persistent-hint': True,
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                    }
                ]
            }
        ],{
            "enabled": False,
            "notify": "on_error",
            "notify_type": "Plugin",
        }
    def get_page(self) -> List[dict]:
        pass

    def get_service(self) -> List[Dict[str, Any]]:
            """
            注册插件公共服务
            [{
                "id": "服务ID",
                "name": "服务名称",
                "trigger": "触发器：cron/interval/date/CronTrigger.from_crontab()",
                "func": self.xxx,
                "kwargs": {} # 定时器参数
                }]
            """
            if self._enabled and self._cron:
                return [{
                    "id": "changetmdbhosts",
                    "name": "自动更新hosts",
                    "trigger": CronTrigger.from_crontab(self._cron),
                    "func": self.auto_diagnosis,
                    "kwargs": {}
                }]