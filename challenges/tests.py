from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status
from challenges.models import Challenge, ModeratePhysicalChallenge, IntensePhysicalChallenge, MentalChallenge, SocialChallenge, Instructor

User = get_user_model()

class ChallengeAPITests(TestCase):
    
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(email='testuser@example.com', password='testpassword')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)  # Authenticate the client
        
        # Create instances of related models
        self.instructor = Instructor.objects.create(
            name="John Doe",
            description="Fitness Instructor",
        )

        self.moderate_physical = ModeratePhysicalChallenge.objects.create(
            title="Moderate Challenge",
            description="A moderate physical challenge.",
            workout_name="Morning Routine",
            duration="30 minutes",
            required_equipments="None",
            instructor=self.instructor,
        )

        self.intense_physical = IntensePhysicalChallenge.objects.create(
            title="Intense Challenge",
            description="An intense physical challenge.",
            workout_name="Evening Routine",
            duration="1 hour",
            required_equipments="Weights",
            instructor=self.instructor,
        )

        self.mental_challenge = MentalChallenge.objects.create(
            title="Mental Challenge",
            description="A mental challenge.",
        )

        self.social_challenge = SocialChallenge.objects.create(
            title="Social Challenge",
            description="A social challenge.",
        )

        self.challenge = Challenge.objects.create(
            day="2024-08-12",
            quote="Stay strong!",
            author_name="Author Name",
            video_link="http://example.com/video",
            moderate_physical=self.moderate_physical,
            intense_physical=self.intense_physical,
            mental=self.mental_challenge,
            social=self.social_challenge,
        )

    def test_challenge_list(self):
        response = self.client.get('/challenges/list/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Attendez-vous à 1 défi dans la liste


    def test_challenge_detail(self):
        response = self.client.get(f'/challenges/detail/{self.challenge.day}/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['day'], '2024-08-12')
        self.assertEqual(response.data['quote'], 'Stay strong!')
        self.assertEqual(response.data['author_name'], 'Author Name')

    def test_challenge_detail_not_found(self):
        response = self.client.get('/challenges/detail/2024-08-13/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_challenge_list_unauthorized(self):
        self.client.force_authenticate(user=None)  # De-authenticate the client
        response = self.client.get('/challenges/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")

    def test_challenge_detail_unauthorized(self):
        self.client.force_authenticate(user=None)  # De-authenticate the client
        response = self.client.get(f'/challenges/detail/{self.challenge.day}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
