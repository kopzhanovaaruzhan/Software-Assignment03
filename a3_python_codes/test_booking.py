import unittest
from booking_v1 import can_book

class TestBookingAvailability(unittest.TestCase):

    def setUp(self):
        # Establish common global mock states
        self.now = 570  # Fictional "now": 09:30 AM
        self.existing_bookings = [
            (600, 660),  # 10:00 AM - 11:00 AM
            (720, 780)   # 12:00 PM - 01:00 PM
        ]

    def test_base_success(self):
        """1. Base success case (room is available and duration is valid)."""
        # 11:10 AM to 11:50 AM (40 mins duration, after now, no overlaps)
        result = can_book(670, 710, self.now, blocked=False, existing=self.existing_bookings)
        self.assertTrue(result["available"])
        self.assertEqual(result["message"], "This time slot is completely open!")

    def test_room_blocked(self):
        """2. Rejection when the room is blocked."""
        result = can_book(670, 710, self.now, blocked=True, existing=self.existing_bookings)
        self.assertFalse(result["available"])
        self.assertIn("blocked for maintenance", result["message"])

    def test_duration_exceeded(self):
        """3. Rejection when the duration is strictly greater than 120 minutes."""
        # 121 minutes duration (670 to 791)
        result = can_book(670, 791, self.now, blocked=False, existing=self.existing_bookings)
        self.assertFalse(result["available"])
        self.assertIn("cannot exceed 120 minutes", result["message"])
        
        # Verify exactly 120 minutes is permitted (AC2 boundary check)
        boundary_result = can_book(670, 790, self.now, blocked=False, existing=[])
        self.assertTrue(boundary_result["available"])

    def test_start_not_in_future(self):
        """4. Rejection when the booking starts now or in the past."""
        # Starts exactly now (570)
        result_now = can_book(570, 630, self.now, blocked=False, existing=[])
        self.assertFalse(result_now["available"])
        self.assertIn("strictly in the future", result_now["message"])

        # Starts in the past (560)
        result_past = can_book(560, 620, self.now, blocked=False, existing=[])
        self.assertFalse(result_past["available"])
        self.assertIn("strictly in the future", result_past["message"])

    def test_touching_intervals(self):
        """5. Verification that touching intervals are allowed."""
        # Candidate ends exactly when an existing booking starts (600)
        result_touch_start = can_book(580, 600, self.now, blocked=False, existing=self.existing_bookings)
        self.assertTrue(result_touch_start["available"])

        # Candidate starts exactly when an existing booking ends (660)
        result_touch_end = can_book(660, 700, self.now, blocked=False, existing=self.existing_bookings)
        self.assertTrue(result_touch_end["available"])

    def test_overlapping_intervals(self):
        """6. Verification that overlapping intervals are rejected."""
        # Partial overlap at the beginning of an existing reservation (590 to 610 overlaps 600 to 660)
        result_partial = can_book(590, 610, self.now, blocked=False, existing=self.existing_bookings)
        self.assertFalse(result_partial["available"])
        self.assertIn("overlaps with an existing reservation", result_partial["message"])

        # Fully enveloped inside an existing reservation (610 to 640 is inside 600 to 660)
        result_enveloped = can_book(610, 640, self.now, blocked=False, existing=self.existing_bookings)
        self.assertFalse(result_enveloped["available"])

if __name__ == "__main__":
    unittest.main()
