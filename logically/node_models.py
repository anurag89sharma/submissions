from neomodel import StructuredNode, StructuredRel, StringProperty, FloatProperty, RelationshipTo, RelationshipFrom

class WeightRel(StructuredRel):
    weight = FloatProperty()


class Document(StructuredNode):
    documentId = StringProperty(unique_index=True, required=True)
    topic = RelationshipTo('Topic', 'belongsTo', model=WeightRel)
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
    document = RelationshipFrom('Document', 'belongsTo', model=WeightRel)
    hasKeyword = RelationshipTo('Keyword', 'hasKeyword', model=WeightRel)

    @property
    def serialize(self):
        return self.__properties__


class Entity(StructuredNode):
    name = StringProperty(index=True, required=True)
    entity_type = StringProperty(required=True)
    key = StringProperty(unique_index=True, required=True)
    document = RelationshipFrom('Document', 'hasEntity')

    @property
    def serialize(self):
        return self.__properties__