from domain import Color
from domain.data_access_layer.session import session


class GetColorsQuery:
    def __init__(self):
        pass

    def by_photo_id(self, photo_id):
        current_session = session()
        try:

            return current_session \
                .query(Color) \
                .filter(Color.photo_id == photo_id) \
                .all()

        finally:
            current_session.close()
            