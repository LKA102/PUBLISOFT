from common.abstract_unit_of_work import AbstractUnitOfWork
from common.command import Command
from common.event import Event
from common.abstract_message_bus import AbstractMessageBus

from modules.posts.domain.commands.post_commands import CreatePostCommand
from modules.posts.domain.commands.post_commands import UpdatePostCommand
from modules.posts.domain.commands.post_commands import DeletePostCommand
from modules.posts.domain.commands.post_commands import ScorePostCommand
from modules.posts.domain.events.post_events import ScorePostEvent

from modules.posts.application.handlers.commands.posts_command_handlers import (
    PostsCommandHandler,
)
from modules.posts.application.handlers.events.posts_events_handlers import (
    PostsEventHandler,
)


class MessageBus(AbstractMessageBus):
    def handle(self, message, uok: AbstractUnitOfWork):
        self._results = []
        self._messages_queue.append(message)
        while self._messages_queue:
            current_message = self._messages_queue.pop(0)
            if isinstance(current_message, Command):
                print(f"[Posts] Processing command: {current_message}")
                cmd_result = self._handle_command(current_message, uok)
                self._results.append(cmd_result)
            elif isinstance(current_message, Event):
                print(f"[Posts] Processing event: {current_message}")
                self._handle_event(current_message, uok)
            else:
                raise ValueError(
                    f"Unknown message type: {type(current_message)}"
                )
        return self._results

# Commands registration
MessageBus.register_command_handler(CreatePostCommand, PostsCommandHandler.handle_create_post_command)
MessageBus.register_command_handler(UpdatePostCommand, PostsCommandHandler.handle_update_post_command)
MessageBus.register_command_handler(DeletePostCommand, PostsCommandHandler.handle_delete_post_command)
MessageBus.register_command_handler(ScorePostCommand, PostsCommandHandler.handle_score_post_command)

# Events registration
MessageBus.register_event_handler(ScorePostEvent, [PostsEventHandler.handle_score_post_event])