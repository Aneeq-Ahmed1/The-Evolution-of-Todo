"""
AI Agent for the Todo Chatbot
Handles natural language commands and executes task actions correctly.
"""

from typing import Dict, Any
import re
from sqlmodel import Session, select

from ..mcp.server import mcp_server
from ..services.ordinal_resolver import ordinal_resolver
from ..services.mapping_service import mapping_service
from ..models.chat_task import ChatTask


class TodoAgent:
    def __init__(self, session: Session):
        self.session = session
        self.mcp_server = mcp_server
        self.ordinal_resolver = ordinal_resolver
        self.mapping_service = mapping_service

    # =========================
    # PUBLIC ENTRY POINT
    # =========================

    def process_message(self, user_id: str, message: str) -> str:
        intent, params = self._parse_intent(message, user_id)

        handlers = {
            "add_task": self._handle_add_task,
            "list_tasks": self._handle_list_tasks,
            "complete_task": self._handle_complete_task,
            "delete_task": self._handle_delete_task,
            "mark_incomplete": self._handle_mark_incomplete,
            "edit_prompt": self._handle_edit_prompt,
            "update_task_content": self._handle_update_task_content,
            "unknown": self._handle_unknown,
        }

        return handlers.get(intent, self._handle_unknown)(params)

    # =========================
    # INTENT PARSING
    # =========================

    def _parse_intent(self, message: str, user_id: str) -> tuple:
        text = message.lower().strip()

        # ---------- ORDINAL COMMANDS (task 1, task 2 etc.)
        ordinal = self.ordinal_resolver.parse_ordinal_command(text)
        if ordinal:
            display_index = ordinal["display_index"]
            action = ordinal["action"]

            tasks = self._get_user_tasks(user_id)
            valid, error = self.mapping_service.validate_display_index(
                user_id, display_index, tasks
            )
            if not valid:
                return "unknown", {"message": error}

            task_id = self.mapping_service.resolve_display_index(
                user_id, display_index
            )
            if not task_id:
                return "unknown", {"message": "Please list tasks first."}

            if action == "complete":
                return "complete_task", {"user_id": user_id, "task_id": task_id}

            if action in ["uncomplete", "incomplete"]:
                return "mark_incomplete", {"user_id": user_id, "task_id": task_id}

            if action in ["edit", "update"]:
                # Refined content extraction for one-shot edit
                # Strategy: remove the entire ordinal command prefix to get the rest
                cleaned_text = text
                # 1. Remove action verb (edit/update/change/rename)
                cleaned_text = re.sub(r"^(edit|update|change|rename)\s+", "", cleaned_text).strip()
                # 2. Remove "task N" or "task #N" or just "N" if it was identified
                cleaned_text = re.sub(r"task\s*#?\s*" + str(display_index), "", cleaned_text).strip()
                # 3. Remove "to" or "as" (e.g., "edit task 1 to New Title")
                cleaned_text = re.sub(r"^(to|as|title|content)\s+", "", cleaned_text).strip()
                
                if cleaned_text:
                    return "update_task_content", {
                        "user_id": user_id,
                        "task_id": task_id,
                        "title": cleaned_text
                    }
                
                return "edit_prompt", {
                    "display_index": display_index,
                    "task_id": task_id,
                }

            if action == "delete":
                return "delete_task", {"user_id": user_id, "task_id": task_id}

        # ---------- ADD TASK
        match = re.search(r"(add|create|remember)\s+(.*)", text)
        if match:
            raw_content = match.group(2).strip()
            
            # Check for description separator
            # Separators: " description ", " desc ", " with description ", " details "
            desc_match = re.search(r"\s+(description|desc|details|with description|with details)\s+(.*)", raw_content, re.IGNORECASE)
            
            if desc_match:
                # Calculate where the description starts to slice the title
                separator_start = desc_match.start()
                title = raw_content[:separator_start].strip()
                description = desc_match.group(2).strip()
            else:
                title = raw_content
                description = None

            return "add_task", {
                "user_id": user_id,
                "title": title,
                "description": description
            }

        # ---------- LIST TASKS
        # Catch variations like "show tasks", "list my pending tasks", "what are my done tasks"
        if re.search(r"(list|show|get|what|display).*task", text):
            status = "all"
            if any(word in text for word in ["pending", "incomplete", "todo", "active", "not done"]):
                status = "pending"
            elif any(word in text for word in ["completed", "done", "finished", "archived"]):
                status = "completed"
            
            return "list_tasks", {"user_id": user_id, "status": status}

        return "unknown", {"message": None}

    # =========================
    # HANDLERS
    # =========================

    def _handle_add_task(self, params: Dict[str, Any]) -> str:
        tool = self.mcp_server.get_tool("add_task")
        result = tool(self.session, **params)
        msg = f"✅ Task added: {result['title']}"
        if params.get("description"):
            msg += f"\nDescription: {params['description']}"
        return msg

    def _handle_list_tasks(self, params: Dict[str, Any]) -> str:
        tool = self.mcp_server.get_tool("list_tasks")
        result = tool(self.session, **params)
        tasks = result["tasks"]

        if not tasks:
            return "You have no tasks."

        # 🔥 IMPORTANT: build mapping here
        self.mapping_service.clear_user_mapping(params["user_id"])

        lines = []
        for i, task in enumerate(tasks, 1):
            self.mapping_service.set_mapping(
                params["user_id"], i, task["id"]
            )
            status = "[x]" if task["completed"] else "[ ]"
            lines.append(f"{i}. {status} **{task['title']}**")
            if task.get("description"):
                lines.append(f"   |- {task['description']}")
            lines.append("") # Add a blank line between tasks

        return "Here are your tasks:\n\n" + "\n".join(lines)

    def _handle_complete_task(self, params: Dict[str, Any]) -> str:
        tool = self.mcp_server.get_tool("complete_task")
        result = tool(self.session, **params)
        return f"✅ Marked as completed: {result['title']}"

    def _handle_delete_task(self, params: Dict[str, Any]) -> str:
        tool = self.mcp_server.get_tool("delete_task")
        result = tool(self.session, **params)
        return f"🗑️ Deleted: {result['title']}"

    def _handle_mark_incomplete(self, params: Dict[str, Any]) -> str:
        task = self.session.get(ChatTask, params["task_id"])
        if not task:
            return "Task not found."

        task.completed = False
        self.session.add(task)
        self.session.commit()
        return f"↩️ Marked as incomplete: {task.title}"

    def _handle_edit_prompt(self, params: Dict[str, Any]) -> str:
        task = self.session.get(ChatTask, params["task_id"])
        return (
            f"You selected task #{params['display_index']}.\n"
            f"Current title: '{task.title}'.\n"
            f"Please provide the new title."
        )

    def _handle_update_task_content(self, params: Dict[str, Any]) -> str:
        tool = self.mcp_server.get_tool("update_task")
        # We assume the content provided is the new title
        result = tool(self.session, user_id=params["user_id"], task_id=params["task_id"], title=params["title"])
        return f"✅ Task updated: {result['title']}"

    def _handle_unknown(self, params: Dict[str, Any]) -> str:
        return (
            params.get("message")
            or "I can add, list, complete, edit, or delete tasks. Try again."
        )

    # =========================
    # HELPERS
    # =========================

    def _get_user_tasks(self, user_id: str):
        return self.session.exec(
            select(ChatTask).where(ChatTask.user_id == user_id).order_by(ChatTask.created_at)
        ).all()
