# def test_delete_hall_manager_fail(self):
#     self.client.login(username="22cs30065", password="Test@123")
#     url = reverse("delete_hall_manager")

#     form = DeleteUserForm(
#         data={"stakeholderID": "22cs30021", "verify_password": "Test@123"}
#     )
#     self.assertTrue(form.is_valid())
#     response = self.client.post(url, data=form.data)
#     self.assertEqual(Student.objects.count(), 4)
#     self.assertTemplateUsed(response, "hall_manager/delete_student.html")

# def test_generate_warden_passbook(self):
#     self.client.login(username="22cs30065", password="Test@123")
#     url = reverse("warden_passbook_pdf")
#     self.assertEquals(url, "/warden/generate-passbook-pdf")
#     response = self.client.get(url)
#     self.assertEquals(response.status_code, 200)
