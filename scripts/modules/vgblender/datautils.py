def get_enum_values(property, name):
    enum_items = property.bl_rna.properties[name].enum_items
    return [item.identifier for item in enum_items]


def get_enum_index(property, name, identifier):
    enum_items = property.bl_rna.properties[name].enum_items
    result = [
        item.value for item in enum_items if item.identifier == identifier]
    if result:
        return result[0]


def remove_item_from_collection(collection, properties, index_name):
    if index_name in properties:
        index = properties[index_name]
        # Adapt index of note collection's items
        if (len(collection) - 1) >= index:
            if properties[index_name] > 0:
                properties[index_name] -= 1
        # Remove item
        collection.remove(index)
