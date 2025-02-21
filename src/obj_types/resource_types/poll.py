from typing import List, TypedDict, Optional, Literal, TYPE_CHECKING
from typing_extensions import NotRequired

from .snowflake import Snowflake
from .user import User
from .emoji import PartialEmoji


LayoutType = Literal[1]  # 1 = Default


class PollMedia(TypedDict):
    text: str
    emoji: NotRequired[Optional[PartialEmoji]]


class PollAnswer(TypedDict):
    poll_media: PollMedia


class PollAnswerWithID(PollAnswer):
    answer_id: int


class PollAnswerCount(TypedDict):
    id: Snowflake
    count: int
    me_voted: bool


class PollAnswerVoters(TypedDict):
    users: List[User]


class PollResult(TypedDict):
    is_finalized: bool
    answer_counts: List[PollAnswerCount]


class PollCreate(TypedDict):
    allow_multiselect: bool
    answers: List[PollAnswer]
    duration: float
    layout_type: LayoutType
    question: PollMedia


# We don't subclass Poll as it will
# still have the duration field, which
# is converted into expiry when poll is
# fetched from a message or returned
# by a `send` method in a Messageable
class Poll(TypedDict):
    allow_multiselect: bool
    answers: List[PollAnswerWithID]
    expiry: str
    layout_type: LayoutType
    question: PollMedia
    results: PollResult