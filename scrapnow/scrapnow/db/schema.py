from enum import Enum

from sqlalchemy import (
    Column, ForeignKey, Integer,
    MetaData, Table, Text, JSON, DateTime
)

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)


class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'
    ERROR = 'error'


class TaskHandlers(Enum):
    REUTERS_ARTICLE = 'reuters_article'


scrap_task = Table(
    'scrap_task',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False,
           autoincrement=True),
    Column('handler', Text),
    Column('url', Text, nullable=False),
    Column('status', Text, default=TaskStatus.PENDING.value, nullable=False),
    Column('result', JSON),
    Column('error', Text),
)

scrap_document_fields = Table(
    'scrap_document_fields',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False,
           autoincrement=True),
    Column('scrap_task_id', Integer, ForeignKey('scrap_task.id'),
           nullable=False),
    Column('name', Text, nullable=False),
    Column('xpath', Text, nullable=False)
)


class ArticleStatus(Enum):
    LISTED = 'listed'
    PROCESSED = 'processed'
    ERROR = 'error'


article = Table(
    'article',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False,
           autoincrement=True),
    Column('url', Text, nullable=False, unique=True),
    Column('title', Text, nullable=False),
    Column('short_description', Text, nullable=False),
    Column('datetime', DateTime, nullable=False),
    Column('body', Text),
    Column('status', Text, default=ArticleStatus.LISTED.value, nullable=False),
    Column('error', Text),
)
