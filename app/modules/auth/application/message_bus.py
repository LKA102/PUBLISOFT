# Here we will implement the message bus for the auth module (if needed).
from asyncio import Event
from app.modules.auth.application.unit_of_work import AbstractUnitOfWork
from app.modules.auth.domain.commands.command import Command

# Commands imports

# Commands handlers imports

# Events imports

# Events handlers imports

class MessageBus:
    """
    Message bus for handling commands and events.
    """
    
    _event_handlers = {}
    _command_handlers = {}

    def __init__(self):
        self._results = []
        self.__messages_queue = []

    @classmethod
    def register_command_handler(cls, command_name, handler):
        cls._command_handlers[command_name] = handler

    def _handle_command(self, command, uok: AbstractUnitOfWork):
        handler = self._command_handlers.get(type(command))
        result = handler(command, uok)
        self.__messages_queue.extend(uok.collect_events())
        return result

    @classmethod
    def register_event_handler(cls, event_name, handler):
        cls._event_handlers[event_name] = handler

    def _handle_event(self, event, uok: AbstractUnitOfWork):
        handlers = self._event_handlers.get(type(event), [])
        for handler in handlers:
            handler(event, uok)
            self.__messages_queue.extend(uok.collect_events())
            
    def handle(self, message, uok: AbstractUnitOfWork):
        """
        Handle a message (command or event).
        """
        self.__messages_queue = [message]
        while self.__messages_queue:
            current_message = self.__messages_queue.pop(0)
            if isinstance(current_message, Command):
                cmd_result = self._handle_command(current_message, uok)
                self._results.append(cmd_result)
            elif isinstance(current_message, Event):
                self._handle_event(current_message, uok)
            else:
                raise ValueError(f"Unknown message type: {type(current_message)}")
        return self._results

# Commands registration


# Events registration