from models.change_detection.change_metrics import ChangeMetric

class UtilsForComparator:
    """Utility functions for comparators"""
    '''
    @staticmethod
    def calculate_percentage_difference(current_value: float, all_previous_value: float) -> float:
        """Calculate percentage difference between two values"""
        if all_previous_value == 0 and current_value > 0:
            # epsilon value to avoid write infinite
            #epsilon = 1e-10
            #all_previous_value = epsilon
            #res = ((current_value - all_previous_value) / all_previous_value ) * 100
            # here, calculate as absolute increase percentage instead of infinite
            res = ( current_value - all_previous_value ) * 100
        else:
            res = ((current_value - all_previous_value) / all_previous_value) * 100 if all_previous_value > 0 else 0.0
        return res
    '''
    '''
    @staticmethod
    def calculate_percentage_difference(current, previous):
        if previous == 0:
            return float("inf") if current != 0 else 0.0
        return ((current - previous) / previous) * 100
    '''
    

    '''# OLD
    @staticmethod
    def calculate_percentage_difference(current: float, previous: float) -> float:
        return ((current - previous) / previous) * 100 if previous > 0 else 0.0

    @staticmethod
    def calculate_change(current: float, previous: float) -> float:
        if previous == 0:
            return float("inf") if current != 0 else 0.0
        return ((current - previous) / previous) * 100
    '''

    @staticmethod
    def calculate_change_metric(curr_value: float, prev_value: float) -> ChangeMetric:
        """Calculate ChangeMetric between current and previous values"""
        if prev_value == 0 and curr_value > 0:
            return ChangeMetric(absolute=curr_value - prev_value, percentage=None)
        else:
            # I don't return and calculate absolute change in this case
            percentage_change = ((curr_value - prev_value) / prev_value) * 100 if prev_value > 0 else 0.0
            return ChangeMetric(absolute=None, percentage=percentage_change)