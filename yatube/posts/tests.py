from django.test import TestCase

class TestStringMethods(TestCase):
    def test_lenght(self):
        self.assertEqual(len('yatube'), 6)

    def test_show_msg(self):
        self.assertTrue(False, msg='Важная проверка на истинность')
