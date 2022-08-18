from project.dao.main_dao import FavoriteDAO


class FavoriteService:
    def __init__(self, dao: FavoriteDAO):
        self.dao = dao

    def post_new_favorite(self, user_id: int, movie_id: int):
        new_favorite: dict = self.dao.insert_item(user_id=user_id, movie_id=movie_id)
        return new_favorite

    def delete_favorite(self, user_id: int, movie_id: int) -> dict:
        favorite_to_delete_id: int = self.dao.select_unique_item_id_by_arguments(user_id=user_id, movie_id=movie_id)
        favorite_to_delete: dict = self.dao.delete_item_by_pk(favorite_to_delete_id)

        return favorite_to_delete
