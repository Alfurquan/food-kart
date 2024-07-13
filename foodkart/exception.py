class RestaurantNotFoundException(Exception):
    pass

class CustomerNotFoundException(Exception):
    pass

class OrderNotFoundException(Exception):
    pass

class MenuItemNotFoundException(Exception):
    pass

class OrderAlreadyDelivered(Exception):
    pass

class CustomerNameMissingException(Exception):
    pass

class CustomerPhoneMissingException(Exception):
    pass

class RestaurantNameMissingException(Exception):
    pass

class RestaurantCapacityLessThanZeroException(Exception):
    pass

class MenuNameMissingException(Exception):
    pass

class MenuPriceNegativeException(Exception):
    pass