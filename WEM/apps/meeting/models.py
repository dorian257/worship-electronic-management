from django.db import models

from WEM.apps.core.models import TimestampedModel

class Meeting(TimestampedModel):
	DONE = "D"
	CANCELED = "C"
	REPORTED = "R"
	STATUS_CHOICES = [(DONE, "Done"), (CANCELED, "Canceled"), (REPORTED, "Reported")]

	name = models.CharField(max_length=500, null=False, blank=False, verbose_name=("Name"))
	date = models.DateTimeField(null=False, blank=False, verbose_name="Date")
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, blank=True)
	reported_date = models.DateTimeField(null=True, blank=True, verbose_name="Reported Date")

	def __str__(self):
	    return "%s " % (self.name)

class Participant(TimestampedModel):
	MALE = "M"
	FEMALE = "F"
	GENDER_CHOICES = [(MALE, "MALE"), (FEMALE, "FEMALE")]

	first_name = models.CharField(max_length=500, null=False, blank=False, verbose_name=("First Name"))
	last_name = models.CharField(max_length=500, null=False, blank=False, verbose_name=("Last Name"))
	email = models.CharField(max_length=500, null=True, blank=True)
	phone_number = models.CharField(max_length=50, null=True, blank=True)
	gender = models.CharField(choices=GENDER_CHOICES, max_length=1, null=False, blank=False)        
	nationality = models.CharField(max_length=500, null=True, blank=True, verbose_name=("Nationality"))

	def __str__(self):
		return "%s %s " % (self.first_name, self.last_name)

class MeetingParticipant(TimestampedModel):
	meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE, related_name="meeting_assisted", related_query_name="meetings_assisted", null=False, blank=False, verbose_name="Meeting")
	participant = models.ForeignKey("Participant", on_delete=models.CASCADE, related_name="participant_assisted", related_query_name="participants_assisted", null=False, blank=False, verbose_name="Participant")
	is_new = models.BooleanField(default=False, null=True, blank=True, verbose_name="First Time")

	def __str__(self):
		return "%s %s participated in the meeting %s " % (self.participant.first_name, self.participant_last_name, self.meeting.name)