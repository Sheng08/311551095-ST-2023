import unittest
import Students

class Test(unittest.TestCase):
    students = Students.Students()
    user_name = ['John', 'Mary','Thomas','Jane']
    user_id = []

    # test case function to check the Students.set_name function
    def test_0_set_name(self):
        print("Start set_name test\n")
        for i in range(4):
            user_id = self.students.set_name(self.user_name[i])
            self.assertIsNotNone(user_id)
            self.user_id.append(user_id)
            print(user_id, self.user_name[i])
        print("\nFinish set_name test\n")

    # test case function to check the Students.get_name function
    def test_1_get_name(self):
        print("\nStart get_name test\n")
        length = len(self.user_id)
        print(f"user_id length = {length}")
        print(f"user_name length = {len(self.user_name)}\n")
        for i in range(5):
            if i < length:
                self.assertEqual(self.user_name[i], self.students.get_name(self.user_id[i]))
                print(f'id {i} : {self.user_name[i]}')
            else:
                print(f'id {i} : There is no such user')
                self.assertEqual('There is no such user', self.students.get_name(i))
        print("\nFinish get_name test")

if __name__ == '__main__':
    unittest.main(verbosity=2) # pragma: no cover
