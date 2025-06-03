import time
from functools import wraps

# Decorator to measure execution time - simplified implementation
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        wrapper.last_execution_time = time.time() - start_time
        return result
    wrapper.last_execution_time = 0
    return wrapper

# Logical operations for secondary sorting
def logical_and(p, q): return p and q
def logical_or(p, q): return p or q
def logical_implies(p, q): return (not p) or q

# More efficient attribute access
def evaluate_logical_expression(item, expression_func, p_key, q_key):
    """Evaluate a logical expression on an object's attributes"""
    try:
        p_value = getattr(item, p_key)
        q_value = getattr(item, q_key)
        return expression_func(p_value, q_value)
    except AttributeError:
        return False

@measure_time
def insertion_sort(items, primary_key, secondary_keys=None):
    """
    Insertion sort with primary and secondary key support
    Time complexity: O(n²)
    Space complexity: O(1)
    """
    if not items:
        return items
        
    for i in range(1, len(items)):
        key_item = items[i]
        j = i - 1
        
        # Compare with primary key
        primary_key_value = getattr(key_item, primary_key)
        
        while j >= 0 and getattr(items[j], primary_key) > primary_key_value:
            items[j + 1] = items[j]
            j -= 1
        
        # When primary keys are equal, check secondary keys
        if j >= 0 and getattr(items[j], primary_key) == primary_key_value and secondary_keys:
            # Check all secondary conditions
            should_swap = any(
                not evaluate_logical_expression(items[j], logic, p, q) and 
                evaluate_logical_expression(key_item, logic, p, q)
                for logic, p, q in secondary_keys
            )
            
            if should_swap:
                items[j + 1] = items[j]
                j -= 1
        
        items[j + 1] = key_item
    
    return items

@measure_time
def merge_sort(items, primary_key, secondary_keys=None):
    """
    Merge sort with primary and secondary key support
    Time complexity: O(n log n)
    Space complexity: O(n)
    """
    if len(items) <= 1:
        return items
    
    # Divide the array into two halves
    mid = len(items) // 2
    left = merge_sort(items[:mid], primary_key, secondary_keys)
    right = merge_sort(items[mid:], primary_key, secondary_keys)
    
    # Merge the sorted halves
    return merge(left, right, primary_key, secondary_keys)

def merge(left, right, primary_key, secondary_keys=None):
    """Efficiently merge two sorted arrays with comparison logic"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        # Cache attribute access for efficiency
        left_val = getattr(left[i], primary_key)
        right_val = getattr(right[j], primary_key)
        
        # Simple cases: one value is clearly less than the other
        if left_val < right_val:
            result.append(left[i])
            i += 1
        elif left_val > right_val:
            result.append(right[j])
            j += 1
        else:
            # Equal primary keys - use secondary keys if provided
            if not secondary_keys:
                result.append(left[i])  # Default to left when equal
                i += 1
            else:
                # Compare using secondary keys
                use_left = True
                
                for logic_func, p_key, q_key in secondary_keys:
                    left_result = evaluate_logical_expression(left[i], logic_func, p_key, q_key)
                    right_result = evaluate_logical_expression(right[j], logic_func, p_key, q_key)
                    
                    if left_result != right_result:
                        # True comes before False in sort order
                        use_left = left_result
                        break
                
                if use_left:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
    
    # Add any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def get_sorting_algorithms():
    """Return available sorting algorithms with descriptive names"""
    return {
        "Insertion Sort (Loop-based)": insertion_sort,
        "Merge Sort (Recursive)": merge_sort
    }
