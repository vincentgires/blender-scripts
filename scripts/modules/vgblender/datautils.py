def get_enum_values(obj, prop_name):
    return [
        item.identifier
        for item in obj.bl_rna.properties[prop_name].enum_items]


def remove_item_from_collection(collection, properties, index_name):
    if index_name in properties:
        index = properties[index_name]
        # Adapt index of note collection's items
        if (len(collection) - 1) >= index:
            if properties[index_name] > 0:
                properties[index_name] -= 1
        # Remove item
        collection.remove(index)
