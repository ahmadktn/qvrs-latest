from django.db.models import Avg, Count
from django.utils import timezone
from django.db import transaction
from organisations.models import Organization
from assesments.models import SupervisorAssessment, OrganizationRating, OrganizationReview

class RatingAggregationService:
    @staticmethod
    @transaction.atomic
    def recalculate_rating(organization):
        assessments = SupervisorAssessment.objects.filter(organization=organization)
        total_count = assessments.count()

        if total_count == 0:
            rating_summary, _ = OrganizationRating.objects.get_or_create(
                organization=organization,
                defaults={
                    'total_assessments': 0,
                    'average_rating': 0.00,
                    'avg_skill_relevance': 0.00,
                    'avg_supervision_adequacy': 0.00,
                    'avg_curriculum_alignment': 0.00,
                    'avg_recommendation': 0.00,
                }
            )
            return rating_summary

        aggregates = assessments.aggregate(
            avg_overall=Avg('overall_rating'),
            avg_q1=Avg('q1_skill_relevance'),
            avg_q2=Avg('q2_supervision_adequacy'),
            avg_q3=Avg('q3_curriculum_alignment'),
            avg_q4=Avg('q4_recommend_future')
        )

        rating_summary, _ = OrganizationRating.objects.get_or_create(organization=organization)
        rating_summary.total_assessments = total_count
        rating_summary.average_rating = round(aggregates['avg_overall'] or 0, 2)
        rating_summary.avg_skill_relevance = round(aggregates['avg_q1'] or 0, 2)
        rating_summary.avg_supervision_adequacy = round(aggregates['avg_q2'] or 0, 2)
        rating_summary.avg_curriculum_alignment = round(aggregates['avg_q3'] or 0, 2)
        rating_summary.avg_recommendation = round(aggregates['avg_q4'] or 0, 2)
        rating_summary.save()

        return rating_summary


class LowRatingDetectorService:
    THRESHOLD = 3.00

    @staticmethod
    @transaction.atomic
    def check_and_flag(organization):
        rating_summary = RatingAggregationService.recalculate_rating(organization)

        # Check if organization rating fell below departmental threshold
        if (rating_summary.total_assessments > 0 and 
            rating_summary.average_rating < LowRatingDetectorService.THRESHOLD and 
            organization.status != Organization.Status.BLACKLISTED):
            
            # Transition status to FLAGGED if not already flagged
            if organization.status != Organization.Status.FLAGGED:
                organization.status = Organization.Status.FLAGGED
                organization.save(update_fields=['status', 'updated_at'])

            # Create an un-resolved review entry if none is pending
            pending_review = OrganizationReview.objects.filter(
                organization=organization,
                status=OrganizationReview.Status.PENDING
            ).exists()

            if not pending_review:
                OrganizationReview.objects.create(
                    organization=organization,
                    triggered_by_rating=rating_summary.average_rating,
                    flag_reason=f"Average supervisor assessment score ({rating_summary.average_rating}/5.00) fell below departmental threshold of {LowRatingDetectorService.THRESHOLD}/5.00.",
                    status=OrganizationReview.Status.PENDING
                )
            return True, rating_summary

        return False, rating_summary
