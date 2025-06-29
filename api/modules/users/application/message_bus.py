# Here we will implement the message bus for the auth module (if needed).
from common.abstract_unit_of_work import AbstractUnitOfWork
from common.command import Command
from common.event import Event
from common.abstract_message_bus import AbstractMessageBus

# Import commands and events for User aggregate
#from modules.auth.domain.commands.user_commands import RegisterUserCommand, LoginUserCommand
#from modules.auth.domain.events.user_events import UserCreatedEvent

# Import handlers for commands and events for User aggregate
#from modules.auth.application.handlers.commands.user_command_handlers import UserCommandHandler
#import modules.auth.application.handlers.events.user_event_handlers as user_event_handlers

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
#MessageBus.register_command_handler(RegisterUserCommand, UserCommandHandler.handle_create_user_command)
#MessageBus.register_command_handler(LoginUserCommand, UserCommandHandler.handle_login_user_command)

# Events registration