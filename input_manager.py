# A pair of dictionaries mapping strings to booleans.
# Strings can be anything, but typically map to keyboard keys.

last_keys_down = {}
keys_down = {}

down = (lambda key: str(key) in keys_down and keys_down[str(key)])
pressed = (lambda key: (str(key) in keys_down and keys_down[str(key)]) and (str(key) not in last_keys_down or (str(key) in last_keys_down and not last_keys_down[str(key)])))
released = (lambda key: (str(key) in keys_down and not keys_down[str(key)]) and (str(key) in last_keys_down and last_keys_down[str(key)]))