# Here we will implement the message bus for the auth module (if needed).
from app.common.abstract_unit_of_work import AbstractUnitOfWork
from app.modules.auth.domain.commands.command import Command
from app.modules.auth.domain.events.event import Event
from app.common.abstract_message_bus import AbstractMessageBus

# Commands imports

# Commands handlers imports

# Events imports

# Events handlers imports

class MessageBus(AbstractMessageBus):
    def handle(self, message, uok: AbstractUnitOfWork):
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