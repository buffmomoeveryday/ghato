# chat/components.py
from django_unicorn.components import UnicornView
from django.contrib.auth.mixins import LoginRequiredMixin
from pprint import pprint as ic
from django.contrib import messages
from dashboard.sqlutils import process_natural_language_query


class ChatComponentView(LoginRequiredMixin, UnicornView):

    template_name = "chat_component.html"

    query = ""
    conversation = []
    my_message = []
    is_processing = False
    is_finished = False

    def submit_query(self):
        if not self.query.strip():
            return messages.error(self.request, message="The Message is empty")

        self.is_processing = True
        self.is_finished = False
        tenant_id = self.request.tenant.id

        try:
            result = process_natural_language_query(self.query, tenant_id)
            ic(result)
            if "error" in result:
                self.conversation.append(
                    {
                        "type": "error",
                        "content": f"Error: {result['error']}",
                    }
                )
                self.request.session["chat_conversation"] = self.conversation
                self.is_processing = False
                self.is_finished = True
                self.call("goto")
                return
            else:
                self.conversation.append(
                    {
                        "type": "user",
                        "content": self.query,
                    }
                )
                self.conversation.append(
                    {
                        "type": "assistant",
                        "content": result["explanation"],
                        "sql_query": result["query"],
                    }
                )
        except Exception as e:
            self.conversation.append(
                {
                    "type": "error",
                    "content": f"An unexpected error occurred: {str(e)}",
                }
            )
            self.request.session["chat_conversation"] = self.conversation
            self.is_processing = False
            self.is_finished = True
            self.call("goto")

        # Store the conversation in the session
        self.request.session["chat_conversation"] = self.conversation
        self.query = ""
        self.is_processing = False
        self.is_finished = True
        self.call("goto")
        self.call("initFlowbite")

    def mount(self):
        if "chat_conversation" in self.request.session:
            self.conversation = self.request.session["chat_conversation"]
        self.call("initFlowbite")

    def clear_chat(self):
        del self.request.session["chat_conversation"]
        messages.success(self.request, "Cleared")
        self.conversation = []
        self.call("initFlowbite")

    class Meta:
        js_exclude = (
            "query",
            "conversation",
        )
