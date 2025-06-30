# Here we will implement the message bus for the auth module (if needed).
from common.abstract_unit_of_work import AbstractUnitOfWork
from common.command import Command
from common.event import Event
from common.abstract_message_bus import AbstractMessageBus

# Import commands and events for Student aggregate
from modules.users.domain.commands.student_commands import *
from modules.users.domain.events.student_events import *

# Import handlers for commands and events for Student aggregate
from modules.users.application.handlers.commands.student_command_handlers import StudentCommandHandler
from modules.users.application.handlers.events.student_event_handlers import StudentEventHandler

# Import commands and events for Admin aggregate
from modules.users.domain.commands.admin_commands import *
from modules.users.domain.events.admin_events import *

# Import handlers for commands and events for Admin aggregate
from modules.users.application.handlers.commands.admin_command_handlers import AdminCommandHandler
from modules.users.application.handlers.events.admin_event_handlers import AdminEventHandler


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
MessageBus.register_command_handler(CreateStudentCommand, StudentCommandHandler.handle_create_student_command)
MessageBus.register_command_handler(UpdateStudentCommand, StudentCommandHandler.handle_update_student_command)
MessageBus.register_command_handler(DisableStudentCommand, StudentCommandHandler.handle_delete_student_command)

MessageBus.register_command_handler(CreateAdminCommand, AdminCommandHandler.handle_create_admin_command)
MessageBus.register_command_handler(UpdateAdminCommand, AdminCommandHandler.handle_update_admin_command)
MessageBus.register_command_handler(DisableAdminCommand, AdminCommandHandler.handle_delete_admin_command)
MessageBus.register_command_handler(DisableStudentAccountCommand, AdminCommandHandler.handle_disable_student_account_command)

# Events registration
MessageBus.register_event_handler(StudentUpdatedEvent, StudentEventHandler.handle_student_updated_event)
MessageBus.register_event_handler(StudentDisabledEvent, StudentEventHandler.handle_student_disabled_event)

MessageBus.register_event_handler(AdminUpdatedEvent, AdminEventHandler.handle_admin_updated_event)
MessageBus.register_event_handler(AdminDisabledEvent, AdminEventHandler.handle_admin_disabled_event)
MessageBus.register_event_handler(DisableStudentAccountEvent, AdminEventHandler.handle_disable_student_account_event)