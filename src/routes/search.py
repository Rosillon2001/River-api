from flask import Blueprint, request
from controllers.searchController import searchKeyword

search_bp = Blueprint('search_bp', __name__)

@search_bp.route("/search/<keyword>", methods=['GET'])
def search(keyword):
    if(request.method == 'GET'):
        return searchKeyword(keyword)