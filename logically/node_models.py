from neomodel import StructuredNode, StringProperty, ArrayProperty, RelationshipTo, RelationshipFrom


class Document(StructuredNode):
    documentId = StringProperty(unique_index=True, required=True)
    topic = RelationshipTo('Topic', 'belongsTo')
    entity = RelationshipTo('Entity', 'hasEntity')

    @property
    def serialize(self):
        return self.__properties__


class Topic(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    keyword = ArrayProperty(StringProperty())
    document = RelationshipFrom('Document', 'belongsTo')

    @property
    def serialize(self):
        return self.__properties__


class Entity(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    entity_type = StringProperty()
    document = RelationshipFrom('Document', 'hasEntity')

    @property
    def serialize(self):
        return self.__properties__

