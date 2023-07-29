# elevators/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Elevator, UserRequest
from .serializers import ElevatorSerializer, UserRequestSerializer

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer
    
    # Additional API for initializing the elevator system
    @action(detail=False, methods=['post'])
    def initialize_elevator_system(self, request):
        num_elevators = request.data.get('num_elevators')

        try:
            num_elevators = int(num_elevators)
        except (TypeError, ValueError):
            return Response({"error": "Invalid number of elevators provided. Please provide a positive integer."},
                            status=status.HTTP_400_BAD_REQUEST)

        if num_elevators <= 0:
            return Response({"error": "Number of elevators must be a positive integer."},
                            status=status.HTTP_400_BAD_REQUEST)

        for i in range(num_elevators):
            elevator = Elevator.objects.create(current_floor=1, direction='STOPPED', is_working=True, is_door_open=False)

        return Response({"message": f"Elevator system initialized with {num_elevators} elevators."},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def next_destination(self, request, pk=None):  # Use "pk" instead of "id"
        elevator = self.get_object()

        # Implement logic to determine the next destination floor for the elevator
        # For simplicity, let's assume the elevator just moves up and down alternatively.
        if elevator.direction == 'UP':
            next_destination_floor = elevator.current_floor + 1
            if next_destination_floor > 5:
                next_destination_floor = 5
                elevator.direction = 'DOWN'
        else:
            next_destination_floor = elevator.current_floor - 1
            if next_destination_floor < 1:
                next_destination_floor = 1
                elevator.direction = 'UP'

        elevator.current_floor = next_destination_floor
        elevator.save()

        return Response({"next_destination_floor": next_destination_floor}, status=status.HTTP_200_OK)


class UserRequestViewSet(viewsets.ModelViewSet):
    queryset = UserRequest.objects.all()
    serializer_class = UserRequestSerializer

    @action(detail=False, methods=['post'])
    def make_request(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        floor = serializer.validated_data['floor']
        direction = serializer.validated_data['direction']

        # Find the closest available elevator to the requested floor.
        available_elevators = Elevator.objects.filter(is_working=True, is_door_open=False)

        if not available_elevators:
            return Response({"error": "No elevators available at the moment. Please try again later."},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

        closest_elevator = min(available_elevators, key=lambda e: abs(e.current_floor - floor))

        # Add the user request to the assigned elevator's requests
        UserRequest.objects.create(elevator=closest_elevator, floor=floor, direction=direction)

        # Update the elevator's direction and start moving towards the requested floor
        if closest_elevator.current_floor < floor:
            closest_elevator.direction = 'UP'
        elif closest_elevator.current_floor > floor:
            closest_elevator.direction = 'DOWN'
        else:
            closest_elevator.direction = 'STOPPED'

        closest_elevator.save()

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)        
            
            
    @action(detail=True, methods=['post'])
    def mark_not_working(self, request, pk=None):
        elevator = self.get_object()

        elevator.is_working = False
        elevator.save()

        # Update the elevator's direction to 'STOPPED' only if it was previously 'UP' or 'DOWN'
        if elevator.direction in ['UP', 'DOWN']:
            elevator.direction = 'STOPPED'
            elevator.save()

        # Now set the 'is_door_open' field of the Elevator object to False
        elevator.is_door_open = False
        elevator.save()

        return Response({"message": f"Elevator {elevator.elevator_id} marked as not working."},
                        status=status.HTTP_200_OK)


    @action(detail=True, methods=['post'])
    def open_door(self, request, pk=None):
        elevator = self.get_object()

        elevator.is_door_open = True
        elevator.save()

        return Response({"message": f"Door of Elevator {elevator.elevator_id} opened."},
                        status=status.HTTP_200_OK)
        
    
    @action(detail=True, methods=['post'])
    def close_door(self, request, pk=None):
        elevator = self.get_object()

        elevator.is_door_open = False
        elevator.save()

        return Response({"message": f"Door of Elevator {elevator.elevator_id} closed."},
                        status=status.HTTP_200_OK)




