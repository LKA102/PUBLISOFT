# Here we will implement the message bus for the auth module (if needed).# Here we will implement the message bus for the auth module (if needed).
from common.abstract_unit_of_work import AbstractUnitOfWork
from common.command import Command
from common.event import Event
from common.abstract_message_bus import AbstractMessageBus

# Import commands and events for Notifications aggregate
#from modules.notifications.domain.commands.user_commands import *
#from modules.auth.domain.events.user_events import *

# Import handlers for commands and events for User aggregate
#from modules.auth.application.handlers.commands.user_command_handlers import UserCommandHandler
#from modules.auth.application.handlers.events.user_event_handlers import UserEventHandler

class MessageBus(AbstractMessageBus):
    def handle(self, message, uok: AbstractUnitOfWork):
        self._results = []
        self._messages_queue.append(message)
        while self._messages_queue:
            current_message = self._messages_queue.pop(0)
            if isinstance(current_message, Command):
                print(f"Processing command: {current_message}")
                cmd_result = self._handle_command(current_message, uok)
                self._results.append(cmd_result)
            elif isinstance(current_message, Event):
                print(f"Processing event: {current_message}")
                self._handle_event(current_message, uok)
            else:
                raise ValueError(f"Unknown message type: {type(current_message)}")
        return self._results

# Commands registration
'''MessageBus.register_command_handler(RegisterUserCommand, UserCommandHandler.handle_create_user_command)
MessageBus.register_command_handler(LoginUserCommand, UserCommandHandler.handle_login_user_command)
MessageBus.register_command_handler(UpdateUserCommand, UserCommandHandler.handle_update_user_command)
MessageBus.register_command_handler(DisableUserCommand, UserCommandHandler.handle_disable_user_command)'''

# Events registration
# MessageBus.register_event_handler(UserCreatedEvent, [UserEventHandler.handle_user_created_event])