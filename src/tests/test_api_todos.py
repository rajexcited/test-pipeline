import unittest
import json

from ..api import app, TODOS


class ToDosTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_todo_list(self):
        # Given
        # When
        response = self.app.get("/todos")
        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.is_json)
        self.assertEqual(3, len(response.json))
        self.assertEqual([k for k in TODOS.keys()], [
                         k for k in response.json.keys()])
        self.assertEqual([v for v in TODOS.values()], [
                         v for v in response.json.values()])

    def test_create_todo_item(self):
        # Given
        payload = json.dumps({
            "task": "test task"
        })

        # When
        response = self.app.post(
            '/todos', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual(True, response.is_json)
        self.assertEqual("test task", response.json["task"])

    def test_get_todo_item(self):
        # Given
        # When
        response = self.app.get("/todos/todo1")
        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.is_json)
        self.assertEqual(1, len(response.json))
        self.assertEqual("build an API", response.json["task"])

    def test_update_todo_item(self):
        path = '/todos/todo2'
        # pre check
        self.assertNotEqual("test task", self.app.get(path).json["task"])

        # Given
        payload = json.dumps({
            "task": "test task"
        })
        # When
        response = self.app.put(
            path, headers={"Content-Type": "application/json"}, data=payload)
        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, response.is_json)
        self.assertEqual("test task", response.json["task"])

    def test_delete_todo_item(self):
        path = '/todos/todo3'
        # pre check
        self.assertEqual("profit!", self.app.get(path).json["task"])
        # Given
        # When
        response = self.app.delete(path)
        # Then
        self.assertEqual(204, response.status_code)
        self.assertEqual(True, response.is_json)
        self.assertEqual(b"", response.get_data())
        response = self.app.get(path)
        self.assertEqual(404, response.status_code)
        self.assertEqual("Todo todo3 doesn't exist", response.json["message"])
