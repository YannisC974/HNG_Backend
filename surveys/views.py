from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from random import choice
from .models import Survey, UserSurvey
from prizes.models import Medal, UserMedal
from .serializers import SurveySerializer, UserSurveySerializer
from challenges.models import Challenge  # Assurez-vous d'importer votre modèle Challenge
from django.db.models import IntegerField, Case, When, Value, Sum


# class SurveyCreateView(generics.CreateAPIView):
#     queryset = Survey.objects.all()
#     serializer_class = SurveySerializer
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={"user": request.user})
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         return Response(serializer.data, status=201)

#     def perform_create(self, serializer):
#         serializer.save()
#         user = self.request.user
#         total_completed_number = Survey.objects.filter(user=user).aggregate(
#             total = Sum("number_of_completed")
#         )["total"]
#         # here we identify which medal the user get
#         # first we find total_completed_number
#         # (how many challenges the user completed after submiting the survey form)
#         # then granting the user with a medal he/she deserves according to the total_completed_number
#         if total_completed_number >= 37:
#             user.medals.add(Medal.objects.get(name="Bronze"))
#         if total_completed_number >= 47:
#             user.medals.add(Medal.objects.get(name="Silver"))
#         if total_completed_number >= 57:
#             user.medals.add(Medal.objects.get(name="Gold"))
#         user.save()
#         return super().perform_create(serializer)
    

class UserSurveyViewSet(viewsets.ModelViewSet):
    queryset = UserSurvey.objects.all()
    serializer_class = UserSurveySerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        
        challenge_id = self.request.data.get('challenge')
        physical_done = self.request.data.get('physical_done')
        mental_done = self.request.data.get('mental_done')
        social_done = self.request.data.get('social_done')
        video_link = self.request.data.get('video_link')

        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except Challenge.DoesNotExist:
            return Response({"detail": "Challenge not found."}, status=status.HTTP_400_BAD_REQUEST)

        survey = Survey.objects.create(
            challenge=challenge,
            physical_done=physical_done,
            mental_done=mental_done,
            social_done=social_done,
            video_link=video_link,
            number_of_completed = Survey.objects.filter(
                challenge=challenge
            ).annotate(
                total_done=Sum(
                    Case(
                        When(physical_done=True, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField()
                    ) +
                    Case(
                        When(mental_done=True, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField()
                    ) +
                    Case(
                        When(social_done=True, then=Value(1)),
                        default=Value(0),
                        output_field=IntegerField()
                    )
                )
            ).filter(
                total_done=3
            ).count()
        )

        user_survey = serializer.save(user=user, survey=survey)
        user_surveys = UserSurvey.objects.filter(user=user)
        surveys = Survey.objects.filter(usersurvey__in=user_surveys)

        total_completed_number = surveys.aggregate(
            total=Sum("number_of_completed")
        )["total"] or 0

        if total_completed_number >= 57:
            medal_name = "Gold"
        elif total_completed_number >= 47:
            medal_name = "Silver"
        elif total_completed_number >= 37:
            medal_name = "Bronze"
        else:
            medal_name = None

        if medal_name:
            medal = Medal.objects.get(name=medal_name)
            UserMedal.objects.create(
                user=user,
                medal=medal
            )

        return super().perform_create(serializer)

class RandomUserSurveyChooseView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request, day):
        challenges = Challenge.objects.filter(day=day)

        surveys = Survey.objects.filter(challenge__in=challenges)
        
        user_surveys = UserSurvey.objects.filter(survey__in=surveys, is_choosed=False)

        if not user_surveys.exists():
            return Response({"detail": "No UserSurvey found for the given day."}, status=status.HTTP_404_NOT_FOUND)

        # Sélectionner un UserSurvey au hasard
        random_user_survey = choice(user_surveys)

        # Mettre à jour l'option is_choosed
        random_user_survey.is_choosed = True
        random_user_survey.save()

        return Response({
            "detail": "UserSurvey updated successfully.",
            "user_survey_id": random_user_survey.id
        }, status=status.HTTP_200_OK)
    
class UpdateUserSurveyValidationView(APIView):
    permission_classes = [IsAdminUser] 

    def patch(self, request, pk):
        try:
            user_survey = UserSurvey.objects.get(pk=pk)
        except UserSurvey.DoesNotExist:
            raise NotFound(detail="UserSurvey not found.")
        
        is_validated = request.data.get('is_validated')
        if is_validated is not None:
            user_survey.is_validated = is_validated
            user_survey.save()
            return Response({
                "detail": "UserSurvey updated successfully.",
                "user_survey_id": user_survey.id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "Please provide the 'is_validated' field in the request data."
            }, status=status.HTTP_400_BAD_REQUEST)