import numpy as np

from core.entity import Entity


class Descriptor(Entity):

    def __init__(self, 
            feature_vec, 
            represent_entity,
            owner_set=None,
            **property):
        """Vector representation of Entity.
        
        Args:
            feature_vec: one-dimension numpy array, tensor vector feature.
            represent_entity: Entity, the descriptor represent the entity.
            owner_set: DescriptorSet, the DescriptorSet this descriptor belong to.
                If not specified, it belongs to Defaut Set.
            property: dict, other metadata of descriptor.
        """
        super().__init__(property)
        self.feature_vec = feature_vec
        self.represent_entity = represent_entity
        self.owner_set = owner_set

