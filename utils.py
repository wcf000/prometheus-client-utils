"""
Utilities for safely accessing Prometheus metrics values.
"""
from prometheus_client import Counter, Gauge, Histogram
from typing import Union, Optional, Dict, Any

def safe_get_counter_value(counter: Counter, labels: Dict[str, str] = None) -> float:
    """
    Safely get the value of a counter, handling missing labels.
    
    Args:
        counter: The prometheus Counter
        labels: Optional dict of labels
    
    Returns:
        The counter value or 0.0 if not available
    """
    try:
        if labels:
            # Try to get labeled counter value using .labels()
            labeled_counter = counter.labels(**labels)
            if hasattr(labeled_counter, '_value'):
                # MutexValue stores the count internally
                return labeled_counter._value.get()
            else:
                # Try to get using sample values
                for sample in counter.collect()[0].samples:
                    matches = True
                    for label_name, label_value in labels.items():
                        if sample.labels.get(label_name) != label_value:
                            matches = False
                            break
                    if matches:
                        return sample.value
                return 0.0
        else:
            # For unlabeled counters
            if hasattr(counter, '_value'):
                return counter._value.get()
            return 0.0
    except Exception:
        return 0.0
        
def get_counter_labels(counter: Counter) -> Dict[str, Any]:
    """
    Safely get all labels used in a counter.
    
    Args:
        counter: The prometheus Counter
    
    Returns:
        Dict of label values by label name
    """
    labels = {}
    try:
        for sample in counter.collect()[0].samples:
            for label_name, label_value in sample.labels.items():
                if label_name not in labels:
                    labels[label_name] = set()
                labels[label_name].add(label_value)
    except Exception:
        pass
    return labels
