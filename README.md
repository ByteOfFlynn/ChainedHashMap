# HashMap With Chaining

This project is a custom implementation of a HashMap data structure in Python, built from scratch using a dynamic array for storage and singly linked lists for collision resolution (chaining). All standard HashMap operations are supported with an average-case time complexity of **O(1)**.

## Features

-  `put(key, value)` — Insert or update key-value pairs
-  `get(key)` — Retrieve value by key
-  `remove(key)` — Delete key-value pair
-  `contains_key(key)` — Check for key existence
-  `clear()` — Remove all entries
-  `empty_buckets()` — Count buckets with no elements
-  `resize_table(new_capacity)` — Rehash and resize the backing array
-  `table_load()` — Compute load factor
-  `get_keys()` — Return all keys in the map
-  `find_mode()` — Find the most frequently occurring element(s) in a DynamicArray

## Implementation Details

- **Collision Resolution:**  
  Uses **separate chaining** with singly linked lists to handle hash collisions.

- **Storage Structure:**  
  Backed by a custom `DynamicArray` class (provided), where each index points to a `LinkedList` of key-value pairs.

- **Performance:**  
  Designed for average-case **O(1)** operations across all methods, even under hash collisions.

- **Modularity:**  
  The implementation uses only the methods provided by the `DynamicArray` and `LinkedList` classes. No built-in Python data structures are used.

## Constraints

- No built-in Python data structures (e.g., dict, list, set)
- All work done through class methods (no direct dunder method calls)
- Compatible with up to **1,000,000 elements**
- Compatible with **multiple hash functions**

## Technologies Used

- **Python (no built-ins)**
- **Custom LinkedList and DynamicArray classes**
