from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        node = bucket.contains(key)
        # Insert value and update
        if node:
            node.value = value
        else:
            bucket.insert(key, value)
            self._size += 1
        # Resize the table
        if self.table_load() > 1.0:
            self.resize_table(self._capacity * 2)

    def empty_buckets(self) -> int:
        """
        Returns value of empty buckets in hash
        """
        empty_count = 0
        # Increment counter for each empty bucket
        for i in range(self._buckets.length()):
            if self._buckets[i].length() == 0:
                empty_count += 1
        return empty_count

    def table_load(self) -> float:
        """
        Returns current load factor
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears content of hash map
        """
        # Get current bucket and start from head
        for i in range(self._buckets.length()):
            bucket = self._buckets._data[i]
            current_node = bucket._head
            # Store next node, remove current, and move to the next
            while current_node:
                next_node = current_node.next
                bucket.remove(current_node.key)
                current_node = next_node
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes capacity of internal hash table
        """
        if new_capacity < 1:
            return
        # Check prime and create new array
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        new_buckets = DynamicArray()
        # Initalize linked list
        for _ in range(new_capacity):
            new_buckets.append(LinkedList())
        # Start at head, get new index, insert, and move to next
        for i in range(self._buckets.length()):
            bucket = self._buckets._data[i]
            current_node = bucket._head
            while current_node:
                new_index = self._hash_function(current_node.key) % new_capacity
                new_buckets[new_index].insert(current_node.key, current_node.value)
                current_node = current_node.next
        # Update capacity
        self._capacity = new_capacity
        self._buckets = new_buckets

    def get(self, key: str):
        """
        Returns value associated with given key
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        # Find node and return if found
        node = bucket.contains(key)
        if node:
            return node.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Determines if a given key is in the hash map
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        return bucket.contains(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes a value from the hash map using its key
        """
        index = self._hash_function(key) % self._capacity
        linked_list = self._buckets[index]
        if linked_list.remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns array that contains each key/value pair in the hash map
        """
        keys_and_values = DynamicArray()
        # Start at head, append the pair, move to next
        for i in range(self._capacity):
            bucket = self._buckets._data[i]
            current_node = bucket._head
            while current_node:
                keys_and_values.append((current_node.key, current_node.value))
                current_node = current_node.next
        return keys_and_values

def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Returns mode and frequency within an array
    """
    frequency_map = HashMap()
    # Convert to str for key
    for i in range(da.length()):
        key = str(da[i])
        # Increment frequency if exists, if not initialize to 1
        if frequency_map.contains_key(key):
            frequency_map.put(key, frequency_map.get(key) + 1)
        else:
            frequency_map.put(key, 1)
    # Create array with frequenecy and get pairs
    mode_values = DynamicArray()
    highest_frequency = 0
    keys_and_values = frequency_map.get_keys_and_values()
    for i in range(keys_and_values.length()):
        key, value = keys_and_values[i]
        # If higher, update, reset, and add to mode
        if value > highest_frequency:
            highest_frequency = value
            mode_values = DynamicArray()
            mode_values.append(key)
        # Add to mode if matches as well
        elif value == highest_frequency:
            mode_values.append(key)
    return mode_values, highest_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
