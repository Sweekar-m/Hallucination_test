import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from create_action.file_ops import file_ops
from create_action.presentation_ops import presentation_ops
from create_action.document_ops import document_ops
from create_action.code_ops import code_ops
from create_action.data_ops import data_ops
from create_action.note_ops import note_ops
from create_action.design_ops import design_ops
from create_action.writing_ops import writing_ops
from create_action.ai_ops import ai_ops
from create_action.email_ops import email_ops

def create_router(intent: dict):
    intent_type = intent.get('cluster', '')
    user_msg = intent.get("user_input")

    if intent_type == "file_ops":
        file_ops(user_msg)
    elif intent_type == "presentation_ops":
        presentation_ops(user_msg)
    elif intent_type == "document_ops":
        document_ops(user_msg)
    elif intent_type == "code_ops":
        code_ops(user_msg)
    elif intent_type == "data_ops":
        data_ops(user_msg)
    elif intent_type == "note_ops":
        note_ops(user_msg)
    elif intent_type == "design_ops":
        design_ops(user_msg)
    elif intent_type == "writing_ops":
        writing_ops(user_msg)
    elif intent_type == "ai_ops":
        ai_ops(user_msg)
    elif intent_type == "email_ops":
        email_ops(user_msg)
    elif intent_type == "unknown":
        print("unknown")
    else:
        print(f"Unhandled cluster: {intent_type}")
