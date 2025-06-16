# Here we will define the message bus for the modules.
from app.common.abstract_unit_of_work import AbstractUnitOfWork
from abc import ABC, abstractmethod

class AbstractMessageBus(ABC):
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
        
    @abstractmethod        
    def handle(self, message, uok: AbstractUnitOfWork):
        """
        Handle a message (command or event).
        """
        pass