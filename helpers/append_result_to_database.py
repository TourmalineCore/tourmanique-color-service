import logging
from config.model_config import model_type

from domain import Color
from pydantic import BaseModel

from domain.data_access_layer.session import session



class NewColorCommand:
    def __init__(self):
        pass

    @staticmethod
    def create(color_entity: Color) -> int:
        current_session = session()
        try:
            current_session.add(color_entity)
            current_session.commit()
            return color_entity.id
        finally:
            current_session.close()


class ColorSchema(BaseModel):
    photo_id: int
    red: int
    green: int
    blue: int

    class Config:
        orm_mode = True


insert_to_db_commands = {
    'colors-model': NewColorCommand,
}

map_result_to_entity = {
    'colors-model': Color,
}

validate_result_with_schema = {
    'colors-model': ColorSchema,
}

class AppendResultsCommand:
    @staticmethod
    def execute(result_message):
        for result in result_message['result']:
            try:
                result['photo_id'] = result_message['photo_id']
                valid_result = validate_result_with_schema[model_type](**result)
                result_entity = map_result_to_entity[model_type](**valid_result.dict())


                insert_to_db_command = insert_to_db_commands[model_type]
                insert_to_db_command().create(result_entity)

            except Exception as e:
                logging.error('Something went wrong! ' + str(e))