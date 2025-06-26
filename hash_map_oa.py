from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Update a key/value pair in the hash map.
        """
        index = self._hash_function(key) % self._capacity
        i = 0
        # Quadratic probe
        while i < self._capacity:
            probe_index = (index + i ** 2) % self._capacity
            entry = self._buckets[probe_index]
            # Check for tombstone or empty, then insert and increment
            if entry is None or entry.is_tombstone:
                self._buckets[probe_index] = HashEntry(key, value)
                self._size += 1
                # Load factor verifier
                if self.table_load() >= 0.5:
                    self.resize_table(self._capacity * 2)
                return
            # Update
            elif entry.key == key:
                entry.value = value
                return
            i += 1

    def table_load(self) -> float:
        """
        Returns current load factor for hash
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Return number of empty buckets in hash
        """
        empty_count = 0
        # Increment count for every empty bucket
        for i in range(self._buckets.length()):
            if self._buckets[i] is None:
                empty_count += 1
        return empty_count

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the hash table
        """
        if new_capacity < self._size:
            return
        # Adjust capacity
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        new_buckets = DynamicArray([None] * new_capacity)
        old_buckets = self._buckets
        self._buckets = new_buckets
        # Store old and reset when reinserting
        old_size = self._size
        self._size = 0
        # Determine non-None and non-tombstone, Quadratic probe
        for i in range(old_buckets.length()):
            entry = old_buckets.get_at_index(i)
            if entry and not entry.is_tombstone:
                index = self._hash_function(entry.key) % new_capacity
                i = 0
                while i < new_capacity:
                    probe_index = (index + i ** 2) % new_capacity
                    new_entry = new_buckets.get_at_index(probe_index)
                    # Increment for each reinsertion
                    if new_entry is None:
                        new_buckets.set_at_index(probe_index, entry)
                        self._size += 1 
                        i = new_capacity
                    i += 1
        # Update hash and new value
        self._capacity = new_capacity
        self._buckets = new_buckets

    def get(self, key: str) -> object:
        """
        Returns value associated with a given key
        """
        index = self._hash_function(key) % self._capacity
        i = 0
        # Quadratic probe
        while i < self._capacity:
            probe_index = (index + i ** 2) % self._capacity
            entry = self._buckets[probe_index]
            # Return none if not found, return matching if found
            if entry is None:
                return None
            if entry.key == key and not entry.is_tombstone:
                return entry.value
            i += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns whether a key is in the hash map
        """
        return self.get(key) is not None

    def remove(self, key: str) -> None:
        """
        Remove the given key and its value from the hash map 
        """
        index = self._hash_function(key) % self._capacity
        i = 0
        # Quadratic probe
        while i < self._capacity:
            probe_index = (index + i ** 2) % self._capacity
            entry = self._buckets[probe_index]
            # Mark as tombstone, decrement size, and move to next
            if entry is None:
                return
            if entry.key == key and not entry.is_tombstone:
                entry.is_tombstone = True
                self._size -= 1
                return
            i += 1

    def clear(self) -> None:
        """
        Clears the contents of the hash map
        """
        self._buckets = DynamicArray([None] * self._capacity)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Generates an array that contains each key/value pair store in hash
        """
        result = DynamicArray()
        # Get entry at current, check for non-tombstone, append to array
        for i in range(self._buckets.length()):
            entry = self._buckets.get_at_index(i)
            if entry and not entry.is_tombstone:
                result.append((entry.key, entry.value))
        return result

    def __iter__(self):
        """
        Iterates itself over the hash map
        """
        self._iter_index = 0
        return self

    def __next__(self):
        """
        Returns next item in the hash map
        """
        # Get entry, move to next, checking for non-tombstone
        while self._iter_index < self._capacity:
            entry = self._buckets.get_at_index(self._iter_index)
            self._iter_index += 1
            if entry and not entry.is_tombstone:
                return entry
        raise StopIteration

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
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
