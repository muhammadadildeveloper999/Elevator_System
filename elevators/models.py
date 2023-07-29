# elevators/models.py
from django.db import models

class Elevator(models.Model):
    elevator_id = models.AutoField(primary_key=True)
    current_floor = models.PositiveIntegerField(default=1)
    direction = models.CharField(max_length=10, choices=[('UP', 'Up'), ('DOWN', 'Down'), ('STOPPED', 'Stopped')], default='STOPPED')
    is_working = models.BooleanField(default=True)
    is_door_open = models.BooleanField(default=False)


class UserRequest(models.Model):
    elevator = models.ForeignKey(Elevator, related_name='requests', on_delete=models.CASCADE)
    floor = models.PositiveIntegerField()
    direction = models.CharField(max_length=10, choices=[('UP', 'Up'), ('DOWN', 'Down')])
    request_time = models.DateTimeField(auto_now_add=True)

