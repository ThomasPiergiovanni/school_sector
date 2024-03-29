"""
"""
from controller.client.csv_manager import CsvManager
from config.settings.settings import (
    INPUT_DIR, INPUT_FILE, INPUT_DELIMITER, INPUT_QUOTECHAR,
    INPUT_REF_DIR, REF_FILE, REF_DELIMITER, REF_QUOTECHAR,
    OUTPUT_DIR, OUTPUT_FILE, OUTPUT_FILE_PRERUN, RUNTYPE
)


class SchoolSectorSetter:
    """
    """
    def __init__(self):
        self.sector = []
        self.address = []
        self.initial_matcher = []
        self.cleaned_sector = []
        self.cleaned_address = []
        self.csv_manager = CsvManager()
    
    def get_school_sector(self):
        self.sector = self.csv_manager.import_data(
            INPUT_DIR, INPUT_FILE, INPUT_DELIMITER, INPUT_QUOTECHAR
        )
        self.address = self.csv_manager.import_data(
            INPUT_REF_DIR, REF_FILE, REF_DELIMITER, REF_QUOTECHAR
        )
        if RUNTYPE == 'prerun': 
            self.__initial_name_matcher()
            self.csv_manager.export_pre_run_data(
                OUTPUT_DIR, OUTPUT_FILE_PRERUN, self.initial_matcher
            )
        else:
            self.__sector_normalizer()
            self.__address_normalizer()
            self.__address_sector_setter()
            self.csv_manager.export_run_data(
                OUTPUT_DIR, OUTPUT_FILE, self.cleaned_address
            )

    def __initial_name_matcher(self):
        address_list = []
        for address in self.address:
            address_list.append(address[15])
        myset = set(address_list)
        address_list_gr = []
        for item in myset:
           address_list_gr.append(item)
        
        for sector in self.sector:
            if sector[28] in address_list_gr:
                item = [sector[0], sector[28], sector[28], True]
                self.initial_matcher.append(item)
            else:
                item = [sector[0], sector[28], '', False]
                self.initial_matcher.append(item)

    def __list_checker(self, lists):
        for item in lists:
            print(item)
    
    def __sector_normalizer(self):
        """
        """
        for sector in self.sector:
            sector_dict = {}
            sector_dict['id'] = sector[0]
            sector_dict['sector_mat'] = self.__set_sector_mat(sector)
            sector_dict['sector_ele'] = self.__set_sector_ele(sector)
            sector_dict['street_name'] = sector[28]
            sector_dict['parity_odd'] = sector[24]
            sector_dict['parity_even'] = sector[21]
            sector_dict['odd_start_number'] = self.__get_number(sector[25])
            sector_dict['odd_end_number'] = self.__get_number(sector[26])
            sector_dict['even_start_number'] =self.__get_number(sector[22])
            sector_dict['even_end_number'] = self.__get_number(sector[23])
            self.cleaned_sector.append(sector_dict)
    
    def __set_sector_mat(self, sector):
        try:
            if 'Maternelle' in sector[19]:
                return sector[19]
            else:
                None
        except:
            pass

    def __set_sector_ele(self, sector):
        try:
            if 'Elémentaire' in sector[19]:
                return sector[19]
            else:
                None
        except:
            pass
    
    def __get_number(self, attr_name):
        try:
            return int(attr_name)
        except:
            return 0


    def __address_normalizer(self):
        """
        """
        for address in self.address:
            address_dict = {}
            address_dict['id'] = address[0]
            address_dict['number'] = int(address[3])
            address_dict['street_name'] = address[15]
            address_dict['sector_mat'] = None
            address_dict['sector_ele'] = None
            address_dict['full_address'] = address[9]
            self.cleaned_address.append(address_dict)
        
    def __address_sector_setter(self):
        """
        """
        for address in self.cleaned_address:
            for sector in self.cleaned_sector:
                if address['street_name'] == sector['street_name']:
                    if (
                        sector['parity_even'] ==  'T' and
                        sector['parity_odd'] == 'T' and
                        sector['sector_mat']
                        
                    ):
                        address['sector_mat'] = sector['sector_mat']
                    elif (
                        sector['parity_even'] ==  'T' and
                        sector['parity_odd'] == 'T' and
                        sector['sector_ele']
                    ):
                        address['sector_ele'] = sector['sector_ele']

                    elif (
                        sector['parity_even'] == 'T' and
                        (sector['parity_odd'] == 'P' or  sector['parity_odd'] == 'S') and
                        address['number'] % 2 == 0 and
                        sector['sector_mat']
        
                    ):
                        address['sector_mat'] = sector['sector_mat']
                    elif (
                        sector['parity_even'] == 'T' and
                        (sector['parity_odd'] == 'P' or  sector['parity_odd'] == 'S') and
                        address['number'] % 2 == 0 and
                        sector['sector_ele']
        
                    ):
                        address['sector_ele'] = sector['sector_ele']
                    elif (
                        sector['parity_even'] == 'T' and
                        sector['parity_odd'] == 'P' and
                        address['number'] % 2 != 0 and
                        address['number'] >= sector['odd_start_number'] and
                        address['number'] <= sector['odd_end_number'] and
                        sector['sector_mat']
             
                    ):
                        address['sector_mat'] = sector['sector_mat']
                    elif (
                        sector['parity_even'] == 'T' and
                        sector['parity_odd'] == 'P' and
                        address['number'] % 2 != 0 and
                        address['number'] >= sector['odd_start_number'] and
                        address['number'] <= sector['odd_end_number'] and
                        sector['sector_ele']
             
                    ):
                        address['sector_ele'] = sector['sector_ele']

                    elif (
                        sector['parity_even'] == 'P' and
                        sector['parity_odd'] == 'T' and
                        address['number'] % 2 == 0 and
                        address['number'] >= sector['even_start_number'] and
                        address['number'] <= sector['even_end_number'] and
                        sector['sector_mat']
             
                    ):
                        address['sector_mat'] = sector['sector_mat']
                    elif (
                        sector['parity_even'] == 'P' and
                        sector['parity_odd'] == 'T' and
                        address['number'] % 2 == 0 and
                        address['number'] >= sector['even_start_number'] and
                        address['number'] <= sector['even_end_number'] and
                        sector['sector_ele']
                    ):
                        address['sector_ele'] = sector['sector_ele']
                    elif (
                            (
                                sector['parity_even'] == 'P' or  
                                sector['parity_even'] == 'S'
                        ) and
                        sector['parity_odd'] == 'T' and
                        address['number'] % 2 != 0 and
                        sector['sector_mat']
                    ):
                        address['sector_mat'] = sector['sector_mat']
                    elif (
                            (
                                sector['parity_even'] == 'P' or  
                                sector['parity_even'] == 'S'
                        ) and
                        sector['parity_odd'] == 'T' and
                        address['number'] % 2 != 0 and
                        sector['sector_ele']
                    ):
                        address['sector_ele'] = sector['sector_ele']
                    elif (
                        sector['parity_even'] == 'P' and
                        (sector['parity_odd'] == 'P' or sector['parity_odd'] == 'S') and
                        address['number'] % 2 == 0 and
                        address['number'] >= sector['even_start_number'] and
                        address['number'] <= sector['even_end_number'] and
                        sector['sector_mat']
                    ):
                        address['sector_mat'] = sector['sector_mat']
                    elif (
                        sector['parity_even'] == 'P' and
                        (sector['parity_odd'] == 'P' or sector['parity_odd'] == 'S') and
                        address['number'] % 2 == 0 and
                        address['number'] >= sector['even_start_number'] and
                        address['number'] <= sector['even_end_number'] and
                        sector['sector_ele']
                    ):
                        address['sector_ele'] = sector['sector_ele']
                    elif (
                        (sector['parity_even'] == 'P' or sector['parity_even'] == 'S')
                        and
                        sector['parity_odd'] == 'P' and
                        address['number'] % 2 != 0 and
                        address['number'] >= sector['odd_start_number'] and
                        address['number'] <= sector['odd_end_number'] and
                        sector['sector_mat']
                    ):
                        address['sector_mat'] = sector['sector_mat']
                    elif (
                        (sector['parity_even'] == 'P' or sector['parity_even'] == 'S')
                        and
                        sector['parity_odd'] == 'P' and
                        address['number'] % 2 != 0 and
                        address['number'] >= sector['odd_start_number'] and
                        address['number'] <= sector['odd_end_number'] and
                        sector['sector_ele']
                    ):
                        address['sector_ele'] = sector['sector_ele']
                    else:
                        print(address['full_address'],'-', address['sector_ele'],'-', address['sector_mat'] )
