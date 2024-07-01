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
    