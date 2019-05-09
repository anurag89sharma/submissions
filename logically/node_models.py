from neomodel import StructuredNode, StructuredRel, StringProperty, FloatProperty, RelationshipTo, RelationshipFrom

class WeightRel(StructuredRel):
    weight = FloatProperty()


class Document(StructuredNode):
    documentId = StringProperty(unique_index=True, required=True)
    topic = RelationshipTo('Topic', 'belongsTo')
    entity = RelationshipTo('Entity', 'hasEntity')

    @property
    def serialize(self):
        return self.__properties__


class Keyword(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    topic = RelationshipFrom('Topic', 'hasKeyword', model=WeightRel)

    @property
    def serialize(self):
        return self.__properties__


class Topic(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    document = RelationshipFrom('Document', 'belongsTo')
    hasKeyword = RelationshipTo('Keyword', 'hasKeyword', model=WeightRel)

    @property
    def serialize(self):
        return self.__properties__


class Entity(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    document = RelationshipFrom('Document', 'hasEntity')
    hasType = RelationshipTo('EntityType', 'hasType')

    @property
    def serialize(self):
        return self.__properties__


class EntityType(StructuredNode):
    name = StringProperty(unique_index=True, required=True)
    entity = RelationshipFrom('Entity', 'hasType')

    @property
    def serialize(self):
        return self.__properties__
