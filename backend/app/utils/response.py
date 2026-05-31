from flask import jsonify

def success_response(message="Success", data=None, status_code=200):
    response = {
        "success": True,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status_code

def error_response(message="An error occurred", status_code=400):
    return jsonify({
        "success": False,
        "message": message
    }), status_code


def paginated_response(message, pagination, status_code=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": pagination.items,
        "meta": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
        },
    }), status_code
