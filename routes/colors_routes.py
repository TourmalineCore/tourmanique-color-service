from flask import Blueprint

from routes.queries.get_colors_query import GetColorsQuery

results_blueprint = Blueprint('results', __name__, url_prefix='/results')


@results_blueprint.route('/<int:photo_id>', methods=['GET'])
def get_colors_by_photo_id(photo_id):
    colors = GetColorsQuery().by_photo_id(photo_id)
    colors_response = list(map(lambda color: {"red": color.red,
                                              "green": color.green,
                                              "blue": color.blue},
                               colors))

    return colors_response
