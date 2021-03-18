def dropdown_tree(settings_list, serializer_class, model_class, parent_id=None, path=""):
    separator = "$#$"
    if len(settings_list) == 0:
        return []
    else:
        data = []
        for i in range(len(settings_list)):
            child = {
                **settings_list[i],
                'parent': parent_id,
                'path': path + separator + settings_list[i]['title'] if path else settings_list[i]['title'],
                'value': settings_list[i]['title'] + "-" + str(parent_id) if 'title' in settings_list[i] else ""
            }
            if len(child['children']) > 0:
                children = child['children']
                child['children'] = []
                queryset = model_class.objects.filter(name=child['title'], is_active=True)
                if parent_id:
                    queryset = queryset.filter(parent=parent_id)
                for item in queryset:
                    item_path = path + separator + child['path'] + separator + item.value if path else \
                        child['path'] + separator + item.value
                    child['children'].append({
                        'id': item.id,
                        'title': item.value,
                        'value': item.value + "-" + str(parent_id),
                        'path': item_path.split(separator),
                        'disabled': True,
                        'children': dropdown_tree(children, serializer_class, model_class, item.id, item_path)
                    })
            child['path'] = child['path'].split(separator)
            data.append(child)
        return data
