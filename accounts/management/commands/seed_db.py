from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

from accounts.models import Student
from organisations.models import Organization, TrainingOpportunity, OrganizationVetting
from placements.models import PlacementRequest, Placement
from assesments.models import SupervisorAssessment, OrganizationRating, OrganizationReview, BlacklistRecord
from assesments.services import RatingAggregationService, LowRatingDetectorService

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed database with realistic initial data for BUK Software Engineering SIWES QOVRS'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding BUK-SIWES QOVRS database..."))

        # 1. Create SIWES Coordinator
        coord, _ = User.objects.get_or_create(
            username='coordinator',
            defaults={
                'email': 'coordinator@buk.edu.ng',
                'first_name': 'Dr. Aliyu',
                'last_name': 'Kabiru',
                'role': User.Role.COORDINATOR,
                'is_staff': True,
                'is_superuser': True,
            }
        )
        coord.set_password('password123')
        coord.save()

        # 2. Create Academic Supervisors
        sup1, _ = User.objects.get_or_create(
            username='dr_usman',
            defaults={
                'email': 'usman.swe@buk.edu.ng',
                'first_name': 'Dr. Usman',
                'last_name': 'Suleiman',
                'role': User.Role.SUPERVISOR,
                'is_staff': True,
            }
        )
        sup1.set_password('password123')
        sup1.save()

        sup2, _ = User.objects.get_or_create(
            username='dr_aminu',
            defaults={
                'email': 'aminu.swe@buk.edu.ng',
                'first_name': 'Dr. Aminu',
                'last_name': 'Bala',
                'role': User.Role.SUPERVISOR,
                'is_staff': True,
            }
        )
        sup2.set_password('password123')
        sup2.save()

        # 3. Create Students
        stud1_user, _ = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'cst20swe00101@student.buk.edu.ng',
                'first_name': 'Fatima',
                'last_name': 'Ibrahim',
                'role': User.Role.STUDENT,
            }
        )
        stud1_user.set_password('password123')
        stud1_user.save()

        student1, _ = Student.objects.get_or_create(
            user=stud1_user,
            defaults={
                'registration_number': 'CST/20/SWE/00101',
                'faculty': 'Faculty of Computing',
                'department': 'Software Engineering',
                'course_of_study': 'B.Sc. Software Engineering',
                'level': '400L',
                'session': '2025/2026',
            }
        )

        stud2_user, _ = User.objects.get_or_create(
            username='student2',
            defaults={
                'email': 'cst20swe00102@student.buk.edu.ng',
                'first_name': 'Abubakar',
                'last_name': 'Sani',
                'role': User.Role.STUDENT,
            }
        )
        stud2_user.set_password('password123')
        stud2_user.save()

        student2, _ = Student.objects.get_or_create(
            user=stud2_user,
            defaults={
                'registration_number': 'CST/20/SWE/00102',
                'faculty': 'Faculty of Computing',
                'department': 'Software Engineering',
                'course_of_study': 'B.Sc. Software Engineering',
                'level': '400L',
                'session': '2025/2026',
            }
        )

        # 4. Create Host Organizations & Opportunities
        # Org 1: High quality approved org
        org1, _ = Organization.objects.get_or_create(
            name='Kano Tech Hub Ltd',
            defaults={
                'registration_number': 'CAC RC-882341',
                'industry_sector': 'Software Development & FinTech',
                'services_provided': 'Enterprise web application development, Cloud infrastructure management, REST API integration, and Mobile banking systems.',
                'address': 'No. 14 Zoo Road, Technology Complex',
                'city': 'Kano',
                'state': 'Kano',
                'website': 'https://kanotechhub.ng',
                'contact_person_name': 'Musa Garba',
                'contact_person_email': 'info@kanotechhub.ng',
                'contact_person_phone': '+234 803 111 2233',
                'status': Organization.Status.APPROVED,
            }
        )
        opp1, _ = TrainingOpportunity.objects.get_or_create(
            organization=org1,
            role_title='Junior Full-Stack Software Engineering Intern',
            defaults={
                'role_description': 'Assisting in developing Python/Django backend API endpoints, PostgreSQL database schema design, and Git code versioning.',
                'expected_skills': 'Python, Django, PostgreSQL, Git, HTML/Tailwind CSS',
                'curriculum_relevance_notes': 'Directly aligns with Software Engineering web design and database modules.',
                'slots_available': 3,
            }
        )

        # Org 2: High quality approved org
        org2, _ = Organization.objects.get_or_create(
            name='Galaxy Backbone Kano Operations',
            defaults={
                'registration_number': 'CAC RC-102938',
                'industry_sector': 'Public Sector IT & Cloud Infrastructure',
                'services_provided': 'National data center management, cloud hosting solutions, fiber network operations, and cyber security oversight.',
                'address': 'Federal Secretariat Complex, Katsina Road',
                'city': 'Kano',
                'state': 'Kano',
                'website': 'https://galaxybackbone.com.ng',
                'contact_person_name': 'Engr. Bello Ahmed',
                'contact_person_email': 'kano.desk@galaxybackbone.com.ng',
                'contact_person_phone': '+234 802 333 4455',
                'status': Organization.Status.APPROVED,
            }
        )
        opp2, _ = TrainingOpportunity.objects.get_or_create(
            organization=org2,
            role_title='Cloud Systems & DevOps Intern',
            defaults={
                'role_description': 'Monitoring cloud server deployments, Linux shell scripting, network packet analysis, and server virtualization.',
                'expected_skills': 'Linux, Bash, Docker, Network Protocols, Cyber Security basics',
                'curriculum_relevance_notes': 'Applies computer networking and system administration curriculum skills.',
                'slots_available': 2,
            }
        )

        # Org 3: Low-rated organization (Flagged!)
        org3, _ = Organization.objects.get_or_create(
            name='Northern Web Systems Ltd',
            defaults={
                'registration_number': 'CAC RC-449102',
                'industry_sector': 'General IT Support',
                'services_provided': 'Computer maintenance and retail office hardware supplies.',
                'address': 'No. 5 Bayero University Road, Kano',
                'city': 'Kano',
                'state': 'Kano',
                'contact_person_name': 'Haruna Usman',
                'contact_person_email': 'contact@nwebsystems.ng',
                'contact_person_phone': '+234 805 777 8899',
                'status': Organization.Status.FLAGGED,
            }
        )
        opp3, _ = TrainingOpportunity.objects.get_or_create(
            organization=org3,
            role_title='IT Intern',
            defaults={
                'role_description': 'Assisting with office clerical work and basic hardware installation.',
                'expected_skills': 'Word processing, basic PC setup',
                'slots_available': 1,
            }
        )

        # Org 4: Newly submitted org awaiting vetting
        org4, _ = Organization.objects.get_or_create(
            name='Kano Data Solutions Hub',
            defaults={
                'registration_number': 'CAC RC-991204',
                'industry_sector': 'Data Engineering & AI',
                'services_provided': 'Data analytics pipeline development, ETL process automation, and business intelligence dashboards.',
                'address': 'No. 8 Zaria Road, Kano',
                'city': 'Kano',
                'state': 'Kano',
                'contact_person_name': 'Zainab Kabir',
                'contact_person_email': 'info@kanodata.ng',
                'contact_person_phone': '+234 806 999 0011',
                'status': Organization.Status.SUBMITTED,
            }
        )
        TrainingOpportunity.objects.get_or_create(
            organization=org4,
            role_title='Junior Data Engineer Intern',
            defaults={
                'role_description': 'Building automated Python ETL pipelines using Pandas and SQL database query optimization.',
                'expected_skills': 'Python, SQL, Pandas, PowerBI',
                'slots_available': 2,
            }
        )

        # 5. Create Vetting Records
        OrganizationVetting.objects.get_or_create(
            organization=org1,
            defaults={
                'vetted_by': coord,
                'decision': OrganizationVetting.Decision.APPROVED,
                'core_business_match_score': 5,
                'training_role_suitability_score': 5,
                'capacity_assessment': 'Excellent modern software laboratory, dedicated senior technical mentors, robust infrastructure.',
                'coordinator_comments': 'Approved for full placement directory inclusion.',
            }
        )

        OrganizationVetting.objects.get_or_create(
            organization=org2,
            defaults={
                'vetted_by': coord,
                'decision': OrganizationVetting.Decision.APPROVED,
                'core_business_match_score': 4,
                'training_role_suitability_score': 5,
                'capacity_assessment': 'Tier-3 data center infrastructure with committed technical staff.',
                'coordinator_comments': 'Highly recommended for infrastructure and cloud software roles.',
            }
        )

        # 6. Create Placements & Assessments for Ratings
        today = timezone.now().date()
        start_date = today - datetime.timedelta(days=180)
        end_date = today - datetime.timedelta(days=10)

        # Placement 1: Completed at Kano Tech Hub
        req1, _ = PlacementRequest.objects.get_or_create(
            student=student1,
            organization=org1,
            defaults={
                'training_opportunity': opp1,
                'proposed_start_date': start_date,
                'proposed_end_date': end_date,
                'status': PlacementRequest.Status.ACCEPTED,
                'cover_note': 'Seeking hands-on web application development experience.',
            }
        )
        plc1, _ = Placement.objects.get_or_create(
            placement_request=req1,
            defaults={
                'student': student1,
                'organization': org1,
                'academic_supervisor': sup1,
                'start_date': start_date,
                'end_date': end_date,
                'status': Placement.Status.COMPLETED,
                'completion_date': end_date,
                'marked_completed_by': coord,
            }
        )
        if not hasattr(plc1, 'assessment'):
            SupervisorAssessment.objects.create(
                placement=plc1,
                organization=org1,
                academic_supervisor=sup1,
                q1_skill_relevance=5,
                q2_supervision_adequacy=5,
                q3_curriculum_alignment=5,
                q4_recommend_future=4,
                qualitative_feedback='Student gained extensive hands-on experience building Django REST APIs and writing unit tests. Outstanding mentorship.',
                observed_student_tasks='Developed user authentication API, integrated PostgreSQL database, wrote Git documentation.'
            )

        # Placement 2: Completed at Northern Web Systems (Low Rating Assessment!)
        req2, _ = PlacementRequest.objects.get_or_create(
            student=student2,
            organization=org3,
            defaults={
                'training_opportunity': opp3,
                'proposed_start_date': start_date,
                'proposed_end_date': end_date,
                'status': PlacementRequest.Status.ACCEPTED,
            }
        )
        plc2, _ = Placement.objects.get_or_create(
            placement_request=req2,
            defaults={
                'student': student2,
                'organization': org3,
                'academic_supervisor': sup2,
                'start_date': start_date,
                'end_date': end_date,
                'status': Placement.Status.COMPLETED,
                'completion_date': end_date,
                'marked_completed_by': coord,
            }
        )
        if not hasattr(plc2, 'assessment'):
            SupervisorAssessment.objects.create(
                placement=plc2,
                organization=org3,
                academic_supervisor=sup2,
                q1_skill_relevance=2,
                q2_supervision_adequacy=2,
                q3_curriculum_alignment=2,
                q4_recommend_future=1,
                qualitative_feedback='Student spent most of the internship running office errands, doing photocopying, and setting up retail printer hardware. Minimal software development exposure.',
                observed_student_tasks='Photocopying office documents, running errands, dusting desktop PCs.'
            )

        # Recalculate ratings and check low-rating detector for all orgs
        for org in [org1, org2, org3]:
            LowRatingDetectorService.check_and_flag(org)

        self.stdout.write(self.style.SUCCESS("Database successfully seeded with realistic BUK-SIWES QOVRS data!"))
        self.stdout.write(self.style.SUCCESS("Credentials:\n- Coordinator: coordinator / password123\n- Supervisor: dr_usman / password123\n- Student: student1 / password123"))
