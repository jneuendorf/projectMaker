def table_name_for_model(model_name, model_config, remove_plural_entry=True):
    for item in model_config:
        if "plural" in item:
            table_name = item["plural"]
            if remove_plural_entry:
                model_config.remove(item)
            return table_name

    return model_name + "s"
