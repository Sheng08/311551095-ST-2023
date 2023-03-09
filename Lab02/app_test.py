import unittest
from unittest.mock import patch, PropertyMock
from app import *

class FakeMailSystem(MailSystem):
    def __init__(self):
         super().__init__()

    def write(self, name):
        context = 'Congrats, ' + name + '!'
        return context

    def send(self, name, context):
        print(context)


class ApplicationTest(unittest.TestCase):
    def setUp(self):
        self.fakeMailSystem = FakeMailSystem()

        # stub
        stub_people = ["William", "Oliver", "Henry", "Liam"]
        stub_selected = ["William", "Oliver", "Henry"]

        self.stub_people =  patch.object(
            Application, "people", return_value=stub_people, new_callable=PropertyMock
        )
        self.stub_selected =  patch.object(
            Application, "selected", return_value=stub_selected, new_callable=PropertyMock
        )

    @patch.object(Application, "get_random_person")
    def test_app(self, mock_get_random_persion):
        app = Application()

        with self.stub_people as stub_people, self.stub_selected:
            # mock
            mock_get_random_persion.side_effect = stub_people.return_value
            select_result = app.select_next_person()
            self.assertEqual(select_result, 'Liam')
            print(f"{select_result} selected")

            # spy
            with patch('builtins.print'), patch.object(app, "mailSystem", wraps=app.mailSystem) as default_mailSystem:
                app.notify_selected()
                default_mailSystem_write_call_count = default_mailSystem.write.call_count
                default_mailSystem_send_call_count = default_mailSystem.send.call_count

            with patch.object(app, "mailSystem", wraps=self.fakeMailSystem ) as fakeMailSystem:
                app.notify_selected()
                print(f"\n\n{fakeMailSystem.write.call_args_list}")
                print(f"{fakeMailSystem.send.call_args_list}")

                # Examine the call count of send() and write()
                self.assertEqual(fakeMailSystem.write.call_count, default_mailSystem_write_call_count)
                self.assertEqual(fakeMailSystem.send.call_count, default_mailSystem_send_call_count)

if __name__ == "__main__":
    unittest.main()