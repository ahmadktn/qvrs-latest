from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User, Student
from organisations.models import Organization, TrainingOpportunity
from placements.models import Placement, PlacementRequest
from datetime import date, timedelta

class RequirementsVerificationTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Coordinator
        self.coord = User.objects.create_superuser(
            username='coordinator',
            email='coord@buk.edu.ng',
            password='password123',
            first_name='Coordinator Head',
            role=User.Role.COORDINATOR
        )

        # Supervisor
        self.sup = User.objects.create_user(
            username='usman.swe@buk.edu.ng',
            email='usman.swe@buk.edu.ng',
            password='password123',
            first_name='Dr. Usman Suleiman',
            state='Kano',
            role=User.Role.SUPERVISOR,
            is_staff=True
        )

        # Student User & Profile
        self.student_user = User.objects.create_user(
            username='CST/20/SWE/00001',
            email='student1@student.buk.edu.ng',
            password='password123',
            first_name='Aliyu Haruna',
            role=User.Role.STUDENT
        )
        self.student = Student.objects.create(
            user=self.student_user,
            registration_number='CST/20/SWE/00001',
            faculty='Faculty of Computing',
            department='Software Engineering'
        )

        # Approved Org
        self.org = Organization.objects.create(
            name='Kano Software Lab',
            registration_number='RC-101010',
            industry_sector='Software Development',
            services_provided='Software engineering and cloud deployment',
            address='12 BUK Road, Kano',
            city='Kano',
            local_government='Kano Municipal',
            state='Kano',
            contact_person_name='Musa Ibrahim',
            contact_person_email='musa@kanosoft.com',
            contact_person_phone='08012345678',
            status=Organization.Status.APPROVED
        )

        # Placement Request & Placement
        self.placement_req = PlacementRequest.objects.create(
            student=self.student,
            organization=self.org,
            proposed_start_date=date.today(),
            proposed_end_date=date.today() + timedelta(days=90),
            status=PlacementRequest.Status.ACCEPTED
        )
        self.placement = Placement.objects.create(
            placement_request=self.placement_req,
            student=self.student,
            organization=self.org,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=90),
            status=Placement.Status.ONGOING
        )

    # 1. Academic supervisor registry page: view details on a new page, see list of students & placement modal
    def test_supervisor_registry_and_student_assignment(self):
        self.client.force_login(self.coord)
        res = self.client.get(reverse('coordinator_supervisors_list'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Dr. Usman Suleiman')
        self.assertContains(res, 'Kano')
        self.assertContains(res, reverse('coordinator_supervisor_detail', args=[self.sup.id]))

        # Assign placement to supervisor
        assign_res = self.client.post(reverse('coordinator_assign_supervisor'), {
            'supervisor_id': self.sup.id,
            'placement_id': self.placement.id,
        })
        self.assertEqual(assign_res.status_code, 302)
        self.placement.refresh_from_db()
        self.assertEqual(self.placement.academic_supervisor, self.sup)

        # Visit the dedicated supervisor detail page
        detail_res = self.client.get(reverse('coordinator_supervisor_detail', args=[self.sup.id]))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, 'Aliyu Haruna')
        self.assertContains(detail_res, 'CST/20/SWE/00001')
        self.assertContains(detail_res, 'Kano Software Lab')
        self.assertContains(detail_res, 'In Supervisor\'s State')
        self.assertContains(detail_res, 'placementDetailsModal')

        # Unassign placement
        unassign_res = self.client.post(reverse('coordinator_unassign_supervisor', args=[self.placement.id]), {
            'next': reverse('coordinator_supervisor_detail', args=[self.sup.id])
        })
        self.assertEqual(unassign_res.status_code, 302)
        self.assertIn(reverse('coordinator_supervisor_detail', args=[self.sup.id]), unassign_res.url)
        self.placement.refresh_from_db()
        self.assertIsNone(self.placement.academic_supervisor)

    # Supervisor Portal dedicated layout and clear workflow tests
    def test_supervisor_portal_workflow(self):
        self.placement.academic_supervisor = self.sup
        self.placement.save()

        self.client.force_login(self.sup)
        res = self.client.get(reverse('supervisor_assessments'))
        self.assertEqual(res.status_code, 200)

        # Dedicated Supervisor Portal Shell verification
        self.assertContains(res, 'Supervisor Portal')
        self.assertContains(res, 'Kano State')
        self.assertContains(res, 'Academic Supervisor Workflow')
        self.assertContains(res, 'Field Supervision')
        self.assertContains(res, 'Conclude Placement')
        self.assertContains(res, '4-Dimension Evaluation')

        # Active student placement is visible
        self.assertContains(res, 'Aliyu Haruna')
        self.assertContains(res, 'Kano Software Lab')
        self.assertContains(res, 'Conclude & Evaluate')

        # Conclude placement to transition to Pending Evaluations queue
        conclude_res = self.client.post(reverse('mark_placement_complete', args=[self.placement.id]))
        self.assertEqual(conclude_res.status_code, 302)
        self.placement.refresh_from_db()
        self.assertEqual(self.placement.status, Placement.Status.COMPLETED)

        # Check that it appears in Pending Evaluations with "Complete Assessment" link
        res2 = self.client.get(reverse('supervisor_assessments'))
        self.assertContains(res2, 'Complete Assessment')
        self.assertContains(res2, reverse('submit_supervisor_assessment', args=[self.placement.id]))

    # 2. Auth: student registration with full name, reg num, email, readonly faculty & department, password
    def test_student_registration_form_and_view(self):
        res = self.client.post(reverse('register_student'), {
            'full_name': 'Fatima Aminu',
            'registration_number': 'CST/20/SWE/00099',
            'email': 'fatima@student.buk.edu.ng',
            'faculty': 'Faculty of Computing',
            'department': 'Software Engineering',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!',
        })
        self.assertEqual(res.status_code, 302)
        student_obj = Student.objects.get(registration_number='CST/20/SWE/00099')
        self.assertEqual(student_obj.user.first_name, 'Fatima Aminu')
        self.assertEqual(student_obj.faculty, 'Faculty of Computing')
        self.assertEqual(student_obj.department, 'Software Engineering')

        # Login using email or reg number
        login_res = self.client.post(reverse('login'), {
            'login_id': 'fatima@student.buk.edu.ng',
            'password': 'StrongPassword123!',
        })
        self.assertEqual(login_res.status_code, 302)

        login_res2 = self.client.post(reverse('login'), {
            'login_id': 'CST/20/SWE/00099',
            'password': 'StrongPassword123!',
        })
        self.assertEqual(login_res2.status_code, 302)

    # 2b. Supervisor creation by coordinator
    def test_supervisor_creation(self):
        self.client.force_login(self.coord)
        res = self.client.post(reverse('coordinator_create_supervisor'), {
            'full_name': 'Dr. Mansur Babangida',
            'email': 'mansur.swe@buk.edu.ng',
            'state': 'Lagos',
            'password': 'SupervisorPass123!',
            'confirm_password': 'SupervisorPass123!',
        })
        self.assertEqual(res.status_code, 302)
        new_sup = User.objects.get(email='mansur.swe@buk.edu.ng')
        self.assertEqual(new_sup.first_name, 'Dr. Mansur Babangida')
        self.assertEqual(new_sup.state, 'Lagos')
        self.assertEqual(new_sup.role, User.Role.SUPERVISOR)

    # 2c. Public Supervisor Registration on registration page
    def test_public_supervisor_registration(self):
        # Registration page has link/tab to supervisor signup
        student_page = self.client.get(reverse('register_student'))
        self.assertContains(student_page, reverse('register_supervisor'))

        # GET supervisor registration page
        res_get = self.client.get(reverse('register_supervisor'))
        self.assertEqual(res_get.status_code, 200)
        self.assertContains(res_get, 'Academic Supervisor Registration')

        # POST valid supervisor registration
        res_post = self.client.post(reverse('register_supervisor'), {
            'full_name': 'Dr. Jamila Bello',
            'email': 'jamila.swe@buk.edu.ng',
            'state': 'Kano',
            'password': 'SupervisorSecret456!',
            'confirm_password': 'SupervisorSecret456!',
        })
        self.assertEqual(res_post.status_code, 302)
        self.assertIn(reverse('login'), res_post.url)

        # Verify supervisor user created with role SUPERVISOR
        created_sup = User.objects.get(email='jamila.swe@buk.edu.ng')
        self.assertEqual(created_sup.first_name, 'Dr. Jamila Bello')
        self.assertEqual(created_sup.state, 'Kano')
        self.assertEqual(created_sup.role, User.Role.SUPERVISOR)
        self.assertTrue(created_sup.is_staff)

        # Login with newly created supervisor credentials
        login_res = self.client.post(reverse('login'), {
            'login_id': 'jamila.swe@buk.edu.ng',
            'password': 'SupervisorSecret456!',
        })
        self.assertEqual(login_res.status_code, 302)

    # 3. Prevent duplicate organization registration
    def test_duplicate_organization_registration_prevented(self):
        self.client.force_login(self.student_user)
        # Attempt to register organization with same name
        res = self.client.post(reverse('organization_submit'), {
            'name': 'kano software lab', # case-insensitive duplicate
            'registration_number': 'RC-999999',
            'industry_sector': 'Fintech',
            'services_provided': 'Payment services',
            'address': 'Kano',
            'city': 'Kano',
            'local_government': 'Kano Municipal',
            'state': 'Kano',
            'contact_person_name': 'Test',
            'contact_person_email': 'test@test.com',
            'contact_person_phone': '08000000000',
            'role_title': 'Backend Developer',
            'role_description': 'API testing',
            'expected_skills': 'Django',
            'curriculum_relevance_notes': 'SWE curriculum',
        })
        self.assertEqual(res.status_code, 200)
        self.assertFormError(res.context['org_form'], 'name', "The organization 'kano software lab' is already registered in the system. Re-registration is not allowed.")

        # Attempt to register organization with same CAC RC number
        res2 = self.client.post(reverse('organization_submit'), {
            'name': 'Different Name Tech',
            'registration_number': 'RC-101010', # Duplicate RC
            'industry_sector': 'Fintech',
            'services_provided': 'Payment services',
            'address': 'Kano',
            'city': 'Kano',
            'local_government': 'Kano Municipal',
            'state': 'Kano',
            'contact_person_name': 'Test',
            'contact_person_email': 'test@test.com',
            'contact_person_phone': '08000000000',
            'role_title': 'Backend Developer',
            'role_description': 'API testing',
            'expected_skills': 'Django',
            'curriculum_relevance_notes': 'SWE curriculum',
        })
        self.assertEqual(res2.status_code, 200)
        self.assertFormError(res2.context['org_form'], 'registration_number', "An organization with CAC RC number 'RC-101010' is already registered in the system.")

    # 4. Remove available positions when registering org or applying
    def test_no_available_positions_in_forms(self):
        self.client.force_login(self.student_user)
        # Org submit page form has no slots_available
        res = self.client.get(reverse('organization_submit'))
        self.assertNotContains(res, 'Placement Slots Available')
        self.assertNotIn('slots_available', res.context['role_form'].fields)

        # Student placement request form has no training_opportunity / available position
        req_res = self.client.get(reverse('student_request_placement', args=[self.org.id]))
        self.assertEqual(req_res.status_code, 200)
        self.assertNotIn('training_opportunity', req_res.context['form'].fields)
        self.assertNotContains(req_res, 'Select Approved Training Role')

    # 5. Adding org and approved directory only visible to logged-in users
    def test_visibility_for_authenticated_users_only(self):
        unauth_client = Client()

        # Anonymous cannot access organization_submit
        res_sub = unauth_client.get(reverse('organization_submit'))
        self.assertEqual(res_sub.status_code, 302)
        self.assertIn(reverse('login'), res_sub.url)

        # Anonymous cannot access approved_directory
        res_dir = unauth_client.get(reverse('approved_directory'))
        self.assertEqual(res_dir.status_code, 302)
        self.assertIn(reverse('login'), res_dir.url)

        # Anonymous cannot access org_detail
        res_det = unauth_client.get(reverse('org_detail', args=[self.org.id]))
        self.assertEqual(res_det.status_code, 302)
        self.assertIn(reverse('login'), res_det.url)

        # Home page for unauthenticated user does not show submit or directory links
        home_res = unauth_client.get(reverse('home'))
        self.assertNotContains(home_res, 'Browse Approved Organizations')
        self.assertNotContains(home_res, 'Register / Submit Organization')
        self.assertContains(home_res, 'Sign In to Portal')

    # 6. Organization registration restricted to students only & buttons removed from admin/supervisor pages
    def test_only_student_can_register_organization(self):
        # Coordinator is blocked
        self.client.force_login(self.coord)
        coord_res = self.client.get(reverse('organization_submit'), follow=True)
        self.assertRedirects(coord_res, reverse('coordinator_dashboard'))
        self.assertContains(coord_res, "Only registered students are permitted to submit host organizations")

        # Supervisor is blocked
        self.client.force_login(self.sup)
        sup_res = self.client.get(reverse('organization_submit'), follow=True)
        self.assertRedirects(sup_res, reverse('supervisor_assessments'))
        self.assertContains(sup_res, "Only registered students are permitted to submit host organizations")

        # Supervisor pages do not contain submit firm button
        sup_dash = self.client.get(reverse('supervisor_assessments'))
        self.assertNotContains(sup_dash, '+ Submit Firm')
        self.assertNotContains(sup_dash, reverse('organization_submit'))

        # Coordinator layout does not contain + Submit Organization button
        self.client.force_login(self.coord)
        coord_dash = self.client.get(reverse('coordinator_dashboard'))
        self.assertNotContains(coord_dash, '+ Submit Organization')
        self.assertNotContains(coord_dash, reverse('organization_submit'))

        # Student CAN access organization_submit
        self.client.force_login(self.student_user)
        student_res = self.client.get(reverse('organization_submit'))
        self.assertEqual(student_res.status_code, 200)
        self.assertContains(student_res, 'Host Organization & Training Role Submission')

    # 7. Additional field: local government when registering an organization
    def test_local_government_in_organization_submission(self):
        self.client.force_login(self.student_user)
        res = self.client.get(reverse('organization_submit'))
        self.assertContains(res, 'Local Government')
        self.assertIn('local_government', res.context['org_form'].fields)

        # Successful submission with local_government
        post_res = self.client.post(reverse('organization_submit'), {
            'name': 'Brand New Tech Hub',
            'registration_number': 'RC-555123',
            'industry_sector': 'Cloud Computing',
            'services_provided': 'Cloud solutions and API development',
            'address': 'No. 20 Airport Road',
            'city': 'Kano',
            'local_government': 'Nassarawa',
            'state': 'Kano',
            'contact_person_name': 'Aliyu Sanusi',
            'contact_person_email': 'aliyu@brandnewtech.ng',
            'contact_person_phone': '08099887766',
            'role_title': 'Junior Cloud Engineer',
            'role_description': 'Deploying microservices and monitoring Kubernetes clusters',
            'expected_skills': 'Docker, Kubernetes, AWS',
            'curriculum_relevance_notes': 'Relevant to software engineering systems modules',
        }, follow=True)
        self.assertEqual(post_res.status_code, 200)

        created_org = Organization.objects.get(name='Brand New Tech Hub')
        self.assertEqual(created_org.local_government, 'Nassarawa')
        self.assertEqual(created_org.created_by, self.student_user)

    # 8. Registration pages should not use 'BUK EMAIL', only 'Email'
    def test_registration_pages_no_buk_email(self):
        # Student registration page
        res_student = self.client.get(reverse('register_student'))
        self.assertEqual(res_student.status_code, 200)
        self.assertNotContains(res_student, 'BUK Email')
        self.assertNotContains(res_student, 'BUK EMAIL')
        self.assertContains(res_student, 'Email *')

        # Supervisor registration page
        res_supervisor = self.client.get(reverse('register_supervisor'))
        self.assertEqual(res_supervisor.status_code, 200)
        self.assertNotContains(res_supervisor, 'BUK Email')
        self.assertNotContains(res_supervisor, 'BUK EMAIL')
        self.assertContains(res_supervisor, 'Email *')

