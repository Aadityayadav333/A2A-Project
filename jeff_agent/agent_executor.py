from a2a.server.agent_execution import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, TextPart
from agent import JeffAgent


class JeffAgentExecutor(AgentExecutor):

    def __init__(self):
        self.agent = JeffAgent()

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        updater = TaskUpdater(event_queue, context.task_id, context.context_id)

        try:
            # ✅ Step 1: Initialize task safely
            if not context.current_task:
                await updater.submit()

            await updater.start_work()

            # ✅ Step 2: Extract query
            query = context.get_user_input()
            context_id = context.context_id

            if not query:
                text = "No input received."
            else:
                response = None

                # ✅ Step 3: Call agent with protection
                try:
                    response = await self.agent.get_response(
                        query=query,
                        context_id=context_id
                    )
                except Exception as e:
                    print(f"[ERROR] JeffAgent failed: {e}")

                # ✅ Step 4: Normalize response (CRITICAL FIX)
                text = self._normalize_response(response)

            # ✅ Step 5: Final fallback (never empty)
            if not text or not str(text).strip():
                text = "No valid response generated."

            # ✅ Step 6: Send output
            parts = [Part(root=TextPart(text=str(text)))]
            await updater.add_artifact(parts, name="scheduling_result")

            await updater.complete()

        except Exception as e:
            # 🚨 GLOBAL FAILSAFE (no crash ever)
            print(f"[FATAL ERROR] Executor crashed: {e}")

            parts = [Part(root=TextPart(
                text="System error occurred while processing request."
            ))]

            try:
                await updater.add_artifact(parts, name="error")
                await updater.complete()
            except Exception as inner_error:
                print(f"[CRITICAL] Failed to report error: {inner_error}")

    def _normalize_response(self, response):
        """
        🔥 Centralized response handler
        Prevents ALL NoneType + format issues
        """

        if response is None:
            return "Sorry, I could not fetch availability right now."

        # If agent returns dict
        if isinstance(response, dict):
            return (
                response.get("content")
                or response.get("message")
                or response.get("text")
                or str(response)
            )

        # If string
        if isinstance(response, str):
            return response

        # If unexpected type
        return str(response)

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        return