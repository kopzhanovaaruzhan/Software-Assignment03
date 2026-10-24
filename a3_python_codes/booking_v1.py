from typing import List, Tuple, Dict, Any

def can_book(
    start: int, 
    end: int, 
    now: int, 
    blocked: bool, 
    existing: List[Tuple[int, int]]
) -> Dict[str, Any]:
    """
    Checks if a room can be booked based on specific temporal and state constraints.
    
    Parameters:
        start (int): Candidate booking start time in minutes after midnight (0 <= start < 1440).
        end (int): Candidate booking end time in minutes after midnight (0 < end <= 1440).
        now (int): Current fictional time in minutes after midnight (0 <= now <= 1439).
        blocked (bool): Global toggle indicating if the room is blocked for maintenance.
        existing (List[Tuple[int, int]]): List of existing bookings as (start, end) tuples.
        
    Returns:
        dict: A dictionary containing 'available' (bool) and 'message' (str).
    """
    # AC3: Reject every request when the selected room is blocked
    if blocked:
        return {"available": False, "message": "The room is completely blocked for maintenance."}
        
    # AC1: Temporal bounds check
    if not (0 <= start < end <= 1440):
        return {"available": False, "message": "Invalid time window boundaries (must be between 0 and 1440, and start before end)."}
        
    # AC1: Start time must be strictly after now
    if start <= now:
        return {"available": False, "message": "Start time must be strictly in the future."}
        
    # AC2: Duration must not exceed 120 minutes
    if (end - start) > 120:
        return {"available": False, "message": "Booking duration cannot exceed 120 minutes (2 hours)."}
        
    # AC4: Reject overlap with any existing booking (intervals touching at endpoints do NOT overlap)
    for existing_start, existing_end in existing:
        if start < existing_end and end > existing_start:
            return {"available": False, "message": "This window overlaps with an existing reservation."}
            
    # AC5: Success Case
    return {"available": True, "message": "This time slot is completely open!"}
