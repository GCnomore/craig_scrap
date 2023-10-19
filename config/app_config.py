import sys

class AppConfig:   
    def __init__(self) -> None:
        self.filter = ''
        self.hide_dup = False
        self.has_image = False
        self.is_location_filter = False
        self.zip_code = ''
        self.miles_from_location = '0'
        self.page =  '1'
    
        if len(sys.argv) > 1 and sys.argv[1].rstrip() == 'skip':
            self.filter = 'skip'
        else:
            self.__set_filter()
    
    def __set_filter(self):
        while True:
            user_filter = input('Set filters? (Y/N) ')

            if(user_filter.rstrip() == 'Y' or user_filter.rstrip() == 'y'):
                self.filter = 'filter'
                self.__set_dup_filter()
                break
            elif(user_filter.rstrip() == 'N' or user_filter.rstrip() == 'n'):
                self.filter = 'skip'
                break
            else:
                continue
    
    def __set_dup_filter(self):
        while True:
            user_filter = input('Hide duplicates? (Y/N) ')

            if(user_filter.rstrip() == 'Y' or user_filter.rstrip() == 'y'):
                self.hide_dup = True
                break
            elif(user_filter.rstrip() == 'N' or user_filter.rstrip() == 'n'):
                self.hide_dup = False
                break
            else:
                continue
        
        self.__set_only_image()
        
            
    def __set_only_image(self):
        while True:
            user_filter = input('Only show listings with image? (Y/N) ')

            if(user_filter.rstrip() == 'Y' or user_filter.rstrip() == 'y'):
                self.has_image = True
                break
            elif(user_filter.rstrip() == 'N' or user_filter.rstrip() == 'n'):
                self.has_image = False
                break
            else:
                continue

        self.__set_page()
        
            
    def __set_page(self): 
        while True:
            user_filter = input('How many pages? ("all" for all) ')
            
            if(user_filter.rstrip() == 'all' or user_filter.rstrip() == 'All'):
                self.page = 'all'
                break
            elif(user_filter.rstrip() != ''):
                self.page = user_filter.rstrip()
                break
            else:
                continue
            
        self.__set_location_filter()
            
    
    def __set_location_filter(self):
        while True:
            user_filter = input('Use location filter? (Y/N) ')

            if(user_filter.rstrip() == 'Y' or user_filter.rstrip() == 'y'):
                self.is_location_filter = True
                self.__set_zipcode()
                break
            elif(user_filter.rstrip() == 'N' or user_filter.rstrip() == 'n'):
                self.is_location_filter = False
                break
            else:
                continue
            
    def __set_zipcode(self):
        self.zip_code = input('Enter zip code: ')
        self.__set_miles()
        
    def __set_miles(self):
        self.miles_from_location = input('Miles from location: ')
        
    def get_config(self):
        return {
            'filter': self.filter,
            'hide_dup': self.hide_dup,
            'has_image': self.has_image,
            'is_location_filter': self.is_location_filter,
            'zip_code': self.zip_code,
            'miles_from_location': self.miles_from_location,
            'page': self.page
        }