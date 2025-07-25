def detect_list_datatype( variable: str | list | list[str], datatype=str):
    '''
    Detecta lista de tipo de dato:
    datatype, list[datatype], list[ list[datatype] ]
    Returns:
        None, datatype, list[datatype], list[ list[datatype] ]
    '''
    # datatype
    if isinstance(variable, datatype):
        return datatype
    elif isinstance(variable, list):
        # list[datatype]
        if all(isinstance(value, datatype) for value in variable):
            return list[datatype]

        # list[ list[datatype] ]
        elif all(isinstance(value, list) for value in variable):
            if all(isinstance(value_value, datatype) for value in variable for value_value in value):
                return list[list[datatype]]
    # None
    return None




def from_list_to_string( variable: list, space="" ):
    data_type = detect_list_datatype( variable, str )

    final_text = ""
    
    # El string
    if data_type == str:
        final_text = variable

    elif data_type == list[str]:
        # Modo lista de string
        final_text += space
        for text in variable:
            final_text += f"{text}, "
        final_text = final_text[:-2]

    elif data_type == list[list[str]]:
        # Lista de lista de string
        for text in variable:
            final_text += space
            for x in text:
                final_text += f"{x} "
            final_text = final_text[:-1]
            final_text += ",\n"
        final_text = final_text[:-2]
    
    return final_text