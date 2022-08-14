import uuid


class Entity(object):

    def __init__(self, id=None, **property):
        """Elements can be managed by vidualDB.
        
        Args:
            id: object, unique identify of entity. 
                If not specified, it will be generated automatically.
            property: dict, metadata of entity.
        """
        if id is None:
            self.id = uuid.uuid4()
        else:
            self.id = id
        self.property = property

    def get_property(self, key):
        """Get propert value by key.

        Args:
            key: object.
        
        Raise:
            KeyError: raise if ``key`` is not recoreded in the entity.
        """
        return self.property[key]
