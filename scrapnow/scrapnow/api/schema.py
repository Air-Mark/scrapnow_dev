from marshmallow import Schema, fields, validate

from ..db.schema import TaskHandlers


class ApiResponse(Schema):
    ok = fields.Boolean(default=True)


class DocumentField(Schema):
    name = fields.String(required=True)
    xpath = fields.String(required=True)


class ScrapperAddTaskRequest(Schema):
    url = fields.Url(required=True)
    document_fields = fields.List(fields.Nested(DocumentField()))
    handler = fields.String(validate=validate.OneOf(
        [item.value for item in TaskHandlers]
    ))


class ArticleFindNewRequest(Schema):
    url = fields.Url(required=True)
    document_fields = fields.List(fields.Nested(DocumentField()))


class ArticleRetrieveRequest(Schema):
    date = fields.DateTime(required=True)


class ArticleRetrieveResponse(Schema):
    items = fields.List(fields.Dict())
