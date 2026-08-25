import unittest
from src.app import add_task, remove_task, toggle_task


class TaskTests(unittest.TestCase):
    def setUp(self):
        self.tasks = [{"id": 1, "title": "Ship it", "done": False}]

    def test_add_task_trims_title(self):
        add_task(self.tasks, "  Test the workflow  ")
        self.assertEqual(self.tasks[-1]["title"], "Test the workflow")

    def test_add_task_assigns_next_id(self):
        add_task(self.tasks, "Review the workflow")
        self.assertEqual(self.tasks[-1], {
            "id": 2,
            "title": "Review the workflow",
            "done": False,
        })

    def test_blank_task_is_ignored(self):
        add_task(self.tasks, "   ")
        self.assertEqual(len(self.tasks), 1)

    def test_toggle_task(self):
        toggle_task(self.tasks, 1)
        self.assertTrue(self.tasks[0]["done"])

    def test_remove_task(self):
        remove_task(self.tasks, 1)
        self.assertEqual(self.tasks, [])


if __name__ == "__main__":
    unittest.main()
