import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from os_actions.system_ops import system_ops
from os_actions.settings_ops import settings_ops
from os_actions.window_ops import window_ops
from os_actions.media_ops import media_ops
from os_actions.network_ops import network_ops
from os_actions.device_ops import device_ops
from os_actions.notification_ops import notification_ops
from os_actions.search_ops import search_ops
from os_actions.time_ops import time_ops
from os_actions.screen_ops import screen_ops

def os_action_router(intent: dict):
    intent_type = intent.get('cluster', '')
    user_msg = intent.get("user_input")

    if intent_type == "system_ops":
        system_ops(user_msg)
    elif intent_type == "settings_ops":
        settings_ops(user_msg)
    elif intent_type == "window_ops":
        window_ops(user_msg)
    elif intent_type == "media_ops":
        media_ops(user_msg)
    elif intent_type == "network_ops":
        network_ops(user_msg)
    elif intent_type == "device_ops":
        device_ops(user_msg)
    elif intent_type == "notification_ops":
        notification_ops(user_msg)
    elif intent_type == "search_ops":
        search_ops(user_msg)
    elif intent_type == "time_ops":
        time_ops(user_msg)
    elif intent_type == "screen_ops":
        screen_ops(user_msg)
    elif intent_type == "unknown":
        print("unknown")
    else:
        print(f"Unhandled cluster: {intent_type}")
